# SPDX-License-Identifier: Apache-2.0
"""SQLite store for requests, one-time codes, the public event log and the
private audit trail.

The public event log is hash-chained: each event's hash covers the previous
event's hash and the event's own canonical JSON, so anyone who downloads
/log/events.json can recompute the chain and detect an edited or deleted entry.
Only public events are chained; the private audit table holds what must not be
published (email addresses, draft revisions, code sends).
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

GENESIS = "0" * 64

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS requests (
    pk              INTEGER PRIMARY KEY AUTOINCREMENT,
    public_id       TEXT UNIQUE,
    pending_token   TEXT UNIQUE,
    requester_email TEXT NOT NULL,
    requester_key   TEXT,
    requester_name  TEXT,
    publish_name    INTEGER NOT NULL DEFAULT 0,
    text            TEXT NOT NULL,
    public_text     TEXT,
    text_held       INTEGER NOT NULL DEFAULT 0,
    held_reasons    TEXT,
    status          TEXT NOT NULL,
    close_reason    TEXT,
    created_at      TEXT NOT NULL,
    received_at     TEXT,
    due_date        TEXT,
    queue_round     INTEGER,
    triage_started_at TEXT,
    triaged_at      TEXT,
    category        TEXT,
    triage_json     TEXT,
    draft_subject   TEXT,
    draft_body      TEXT,
    sent_subject    TEXT,
    sent_body       TEXT,
    sent_at         TEXT,
    ack_sent_at     TEXT,
    closed_at       TEXT,
    reviewer        TEXT,
    client_ip       TEXT
);
CREATE INDEX IF NOT EXISTS ix_requests_status ON requests(status);
CREATE INDEX IF NOT EXISTS ix_requests_email ON requests(requester_email);

CREATE TABLE IF NOT EXISTS otp (
    pk          INTEGER PRIMARY KEY AUTOINCREMENT,
    email       TEXT NOT NULL,
    purpose     TEXT NOT NULL,
    ref         TEXT NOT NULL,
    salt        TEXT NOT NULL,
    code_hash   TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    expires_at  TEXT NOT NULL,
    attempts    INTEGER NOT NULL DEFAULT 0,
    used_at     TEXT,
    ip          TEXT
);
CREATE INDEX IF NOT EXISTS ix_otp_email ON otp(email, created_at);

CREATE TABLE IF NOT EXISTS events (
    seq         INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id  TEXT,
    at          TEXT NOT NULL,
    type        TEXT NOT NULL,
    actor       TEXT NOT NULL,
    data        TEXT NOT NULL,
    prev_hash   TEXT NOT NULL,
    hash        TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_events_request ON events(request_id);

CREATE TABLE IF NOT EXISTS audit (
    pk          INTEGER PRIMARY KEY AUTOINCREMENT,
    request_pk  INTEGER,
    at          TEXT NOT NULL,
    type        TEXT NOT NULL,
    actor       TEXT NOT NULL,
    data        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS calendar (
    day         TEXT PRIMARY KEY,
    is_open     INTEGER NOT NULL,
    note        TEXT
);

CREATE TABLE IF NOT EXISTS counters (
    name        TEXT PRIMARY KEY,
    value       INTEGER NOT NULL
);
"""


def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def connect(path: Path | str) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path), timeout=15, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=15000")
    return conn


def init(path: Path | str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = connect(path)
    try:
        conn.executescript(SCHEMA)
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(requests)")}
        if "requester_key" not in cols:  # databases created by 0.1.0 before this column
            conn.execute("ALTER TABLE requests ADD COLUMN requester_key TEXT")
            conn.execute("UPDATE requests SET requester_key=lower(requester_email)")
        conn.execute("CREATE INDEX IF NOT EXISTS ix_requests_key ON requests(requester_key)")
    finally:
        conn.close()


@contextmanager
def transaction(conn: sqlite3.Connection, immediate: bool = True):
    """BEGIN IMMEDIATE takes the write lock up front, so two workers cannot
    both see an empty active slot and claim different requests."""
    conn.execute("BEGIN IMMEDIATE" if immediate else "BEGIN")
    try:
        yield conn
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    else:
        conn.execute("COMMIT")


def next_counter(conn: sqlite3.Connection, name: str) -> int:
    row = conn.execute("SELECT value FROM counters WHERE name=?", (name,)).fetchone()
    value = (row["value"] if row else 0) + 1
    conn.execute(
        "INSERT INTO counters(name, value) VALUES(?, ?) "
        "ON CONFLICT(name) DO UPDATE SET value=excluded.value",
        (name, value),
    )
    return value


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def event_hash(prev_hash: str, request_id, at: str, type_: str, actor: str, data: dict) -> str:
    body = _canonical({"request_id": request_id, "at": at, "type": type_, "actor": actor, "data": data})
    return hashlib.sha256((prev_hash + body).encode("utf-8")).hexdigest()


def log_event(conn, request_id: str | None, type_: str, actor: str, data: dict, at: str | None = None) -> int:
    """Append a public event. Call inside a transaction. Never put an email
    address or other private detail in data: it is published as is."""
    at = at or iso(utcnow())
    row = conn.execute("SELECT hash FROM events ORDER BY seq DESC LIMIT 1").fetchone()
    prev = row["hash"] if row else GENESIS
    h = event_hash(prev, request_id, at, type_, actor, data)
    cur = conn.execute(
        "INSERT INTO events(request_id, at, type, actor, data, prev_hash, hash) VALUES(?,?,?,?,?,?,?)",
        (request_id, at, type_, actor, _canonical(data), prev, h),
    )
    return cur.lastrowid


def audit(conn, request_pk: int | None, type_: str, actor: str, data: dict) -> None:
    conn.execute(
        "INSERT INTO audit(request_pk, at, type, actor, data) VALUES(?,?,?,?,?)",
        (request_pk, iso(utcnow()), type_, actor, _canonical(data)),
    )


def verify_chain(rows) -> tuple[bool, int | None]:
    """Recompute the chain over event rows (dicts or sqlite rows, ascending seq).
    Returns (ok, first_bad_seq)."""
    prev = GENESIS
    for r in rows:
        data = r["data"]
        if isinstance(data, str):
            data = json.loads(data)
        if r["prev_hash"] != prev:
            return False, r["seq"]
        h = event_hash(prev, r["request_id"], r["at"], r["type"], r["actor"], data)
        if h != r["hash"]:
            return False, r["seq"]
        prev = h
    return True, None
