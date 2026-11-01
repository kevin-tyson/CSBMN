# SPDX-License-Identifier: Apache-2.0
"""Runtime settings. Every value comes from an RTK_* environment variable so
the same code runs on a laptop, in tests and on the CCTV/CCMC host."""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass, field, replace
from pathlib import Path


def _bool(value: str | None, default: bool) -> bool:
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int(value: str | None, default: int) -> int:
    try:
        return int(value) if value not in (None, "") else default
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    secret_key: str
    base_url: str = "http://127.0.0.1:8091"
    navigator_url: str = "https://csbmn.claremontv.org/"
    repo_path: Path | None = None
    timezone: str = "America/New_York"

    # Mail
    mail_backend: str = "outbox"  # outbox | smtp | console
    mail_from: str = "RTK Portal <rtk-portal@localhost>"
    smtp_host: str = "localhost"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_starttls: bool = True

    # People
    staff_emails: tuple[str, ...] = ()
    district_name: str = "Claremont School District"
    # Per the October 2026 proposal; confirm once the CCTV/CCMC board approves the pilot.
    operator: str = "Claremont Community Television (CCTV) / Claremont Community Media Center (CCMC)"
    custodian_signature: str = (
        "Office of the Superintendent, SAU 6\n"
        "Records custodian under Claremont School Board Policy EH"
    )

    # Triage
    claude_api_key: str = ""
    claude_model: str = "claude-sonnet-5-5"
    claude_max_turns: int = 6
    min_cell_size: int = 10

    # Limits
    otp_ttl_minutes: int = 10
    otp_max_attempts: int = 5
    max_request_chars: int = 5000
    pending_ttl_hours: int = 24
    contact_retention_days: int = 0  # 0 keeps requester emails; set by the operator's retention decision

    # HTTP
    https_only: bool = False
    staff_allowed_ips: tuple[str, ...] = ()  # CIDR list; empty allows staff sign-in from anywhere
    trust_proxy: bool = False
    start_worker: bool = True

    extra: dict = field(default_factory=dict)

    @property
    def db_path(self) -> Path:
        return self.data_dir / "rtk.db"

    @property
    def kg_path(self) -> Path:
        return self.data_dir / "kg.db"

    @property
    def outbox_dir(self) -> Path:
        return self.data_dir / "outbox"

    @property
    def triage_engine(self) -> str:
        return "claude" if self.claude_api_key else "rules"

    def with_(self, **kw) -> "Settings":
        return replace(self, **kw)

    @classmethod
    def from_env(cls, env: dict | None = None) -> "Settings":
        e = os.environ if env is None else env
        data_dir = Path(e.get("RTK_DATA_DIR", "data")).resolve()
        secret = e.get("RTK_SECRET_KEY", "")
        if not secret:
            # A random key works for a dev run but logs everyone out on restart.
            secret = secrets.token_hex(32)
        repo = e.get("RTK_REPO_PATH")
        staff = tuple(
            s.strip().lower() for s in e.get("RTK_STAFF_EMAILS", "").split(",") if s.strip()
        )
        return cls(
            data_dir=data_dir,
            secret_key=secret,
            base_url=e.get("RTK_BASE_URL", cls.base_url).rstrip("/"),
            navigator_url=e.get("RTK_NAVIGATOR_URL", cls.navigator_url),
            repo_path=Path(repo).resolve() if repo else None,
            timezone=e.get("RTK_TIMEZONE", cls.timezone),
            mail_backend=e.get("RTK_MAIL_BACKEND", cls.mail_backend),
            mail_from=e.get("RTK_MAIL_FROM", cls.mail_from),
            smtp_host=e.get("RTK_SMTP_HOST", cls.smtp_host),
            smtp_port=_int(e.get("RTK_SMTP_PORT"), cls.smtp_port),
            smtp_user=e.get("RTK_SMTP_USER", ""),
            smtp_password=e.get("RTK_SMTP_PASSWORD", ""),
            smtp_starttls=_bool(e.get("RTK_SMTP_STARTTLS"), True),
            staff_emails=staff,
            district_name=e.get("RTK_DISTRICT_NAME", cls.district_name),
            operator=e.get("RTK_OPERATOR", cls.operator),
            custodian_signature=e.get("RTK_SIGNATURE", cls.custodian_signature).replace("\\n", "\n"),
            claude_api_key=e.get("RTK_ANTHROPIC_API_KEY", e.get("ANTHROPIC_API_KEY", "")),
            claude_model=e.get("RTK_CLAUDE_MODEL", cls.claude_model),
            claude_max_turns=_int(e.get("RTK_CLAUDE_MAX_TURNS"), cls.claude_max_turns),
            min_cell_size=_int(e.get("RTK_MIN_CELL_SIZE"), cls.min_cell_size),
            otp_ttl_minutes=_int(e.get("RTK_OTP_TTL_MINUTES"), cls.otp_ttl_minutes),
            otp_max_attempts=_int(e.get("RTK_OTP_MAX_ATTEMPTS"), cls.otp_max_attempts),
            max_request_chars=_int(e.get("RTK_MAX_REQUEST_CHARS"), cls.max_request_chars),
            pending_ttl_hours=_int(e.get("RTK_PENDING_TTL_HOURS"), cls.pending_ttl_hours),
            contact_retention_days=_int(e.get("RTK_CONTACT_RETENTION_DAYS"), cls.contact_retention_days),
            https_only=_bool(e.get("RTK_HTTPS_ONLY"), False),
            staff_allowed_ips=tuple(x.strip() for x in e.get("RTK_STAFF_ALLOWED_IPS", "").split(",") if x.strip()),
            trust_proxy=_bool(e.get("RTK_TRUST_PROXY"), False),
            start_worker=_bool(e.get("RTK_START_WORKER"), True),
        )
