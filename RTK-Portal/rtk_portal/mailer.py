# SPDX-License-Identifier: Apache-2.0
"""Outgoing mail. Three backends:

outbox   writes each message as an .eml file under data/outbox (development
         and pilots where a person forwards mail by hand)
smtp     sends through RTK_SMTP_HOST with STARTTLS
console  prints to stdout
"""

from __future__ import annotations

import secrets
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

from . import db


class Mailer:
    def __init__(self, settings):
        self.s = settings

    def build(self, to: str, subject: str, body: str) -> EmailMessage:
        msg = EmailMessage()
        msg["From"] = self.s.mail_from
        msg["To"] = to
        msg["Subject"] = subject
        msg["Date"] = formatdate(localtime=False)
        domain = self.s.mail_from.rsplit("@", 1)[-1].strip("> ") or "localhost"
        msg["Message-ID"] = make_msgid(domain=domain)
        msg.set_content(body)
        return msg

    def send(self, to: str, subject: str, body: str) -> str:
        msg = self.build(to, subject, body)
        backend = self.s.mail_backend
        if backend == "smtp":
            ctx = ssl.create_default_context()
            with smtplib.SMTP(self.s.smtp_host, self.s.smtp_port, timeout=30) as smtp:
                if self.s.smtp_starttls:
                    smtp.starttls(context=ctx)
                if self.s.smtp_user:
                    smtp.login(self.s.smtp_user, self.s.smtp_password)
                smtp.send_message(msg)
        elif backend == "console":
            print(msg.as_string())
        else:
            out = Path(self.s.outbox_dir)
            out.mkdir(parents=True, exist_ok=True)
            stamp = db.utcnow().strftime("%Y%m%dT%H%M%SZ")
            safe = "".join(c if c.isalnum() else "_" for c in to)[:60]
            (out / f"{stamp}-{secrets.token_hex(3)}-{safe}.eml").write_bytes(bytes(msg))
        return msg["Message-ID"]
