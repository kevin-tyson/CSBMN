# SPDX-License-Identifier: Apache-2.0
import re
from pathlib import Path

import pytest

from rtk_portal import kg as kgmod
from rtk_portal.config import Settings
from rtk_portal.service import Portal

FIXTURE_REPO = Path(__file__).parent / "fixtures" / "repo"


class CaptureMailer:
    def __init__(self):
        self.sent = []

    def send(self, to, subject, body):
        self.sent.append({"to": to, "subject": subject, "body": body})
        return f"<{len(self.sent)}@test>"

    def last_code(self, to=None):
        for m in reversed(self.sent):
            if to is None or m["to"] == to:
                hit = re.search(r"\b(\d{6})\b", m["body"])
                if hit:
                    return hit.group(1)
        raise AssertionError("no code sent")


@pytest.fixture(scope="session")
def kg_path(tmp_path_factory):
    out = tmp_path_factory.mktemp("kg") / "kg.db"
    kgmod.build(FIXTURE_REPO, out, "https://csbmn.claremontv.org/", log=lambda *a: None)
    return out


@pytest.fixture
def settings(tmp_path, kg_path):
    s = Settings(data_dir=tmp_path, secret_key="test-secret", base_url="http://portal.test",
                 staff_emails=("clerk@sau6.test",), start_worker=False, mail_backend="console")
    # Point the KG at the session-built fixture index.
    (tmp_path / "kg.db").symlink_to(kg_path)
    return s


@pytest.fixture
def mailer():
    return CaptureMailer()


@pytest.fixture
def portal(settings, mailer):
    return Portal(settings, mailer=mailer)


def file_and_verify(portal, mailer, email, text, name="", publish=False):
    token = portal.file_request(email, name, publish, text)
    code = mailer.last_code(email)
    return portal.verify_request(token, code)
