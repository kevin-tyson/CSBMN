# SPDX-License-Identifier: Apache-2.0
"""Business-day arithmetic for the RSA 91-A:4, IV(b) five-day clock.

A business day is a weekday that is not a New Hampshire legal holiday under
RSA 288:1 and is not a day the custodian has marked closed. The custodian can
also mark a date open, which overrides a holiday (for an office that works on,
say, Columbus Day). Observed-day shifts for holidays that fall on a weekend are
not assumed: RSA 288:1 does not state them, so the custodian enters them as
closures when the office actually closes.
"""

from __future__ import annotations

from datetime import date, timedelta


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    """n-th (1-based) weekday (Mon=0) of a month."""
    d = date(year, month, 1)
    offset = (weekday - d.weekday()) % 7
    return d + timedelta(days=offset + 7 * (n - 1))


def _last_weekday(year: int, month: int, weekday: int) -> date:
    d = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
    return d - timedelta(days=(d.weekday() - weekday) % 7)


def nh_legal_holidays(year: int) -> dict[date, str]:
    """Legal holidays named in RSA 288:1 for one year."""
    h = {
        date(year, 1, 1): "New Year's Day",
        _nth_weekday(year, 1, 0, 3): "Martin Luther King, Jr. Civil Rights Day",
        _nth_weekday(year, 2, 0, 3): "Washington's Birthday",
        _last_weekday(year, 5, 0): "Memorial Day",
        date(year, 7, 4): "Independence Day",
        _nth_weekday(year, 9, 0, 1): "Labor Day",
        _nth_weekday(year, 10, 0, 2): "Columbus Day",
        date(year, 11, 11): "Veterans Day",
        _nth_weekday(year, 11, 3, 4): "Thanksgiving Day",
        date(year, 12, 25): "Christmas Day",
    }
    if year % 2 == 0:
        # Biennial state general election: Tuesday after the first Monday in November.
        h[_nth_weekday(year, 11, 0, 1) + timedelta(days=1)] = "Election Day"
    return h


class Calendar:
    """overrides maps a date to True (open) or False (closed)."""

    def __init__(self, overrides: dict[date, bool] | None = None):
        self.overrides = dict(overrides or {})
        self._holidays: dict[int, dict[date, str]] = {}

    def holiday(self, d: date) -> str | None:
        if d.year not in self._holidays:
            self._holidays[d.year] = nh_legal_holidays(d.year)
        return self._holidays[d.year].get(d)

    def is_business_day(self, d: date) -> bool:
        if d in self.overrides:
            return self.overrides[d]
        if d.weekday() >= 5:
            return False
        return self.holiday(d) is None

    def add_business_days(self, start: date, n: int) -> date:
        """The n-th business day after start (start itself is not counted)."""
        d = start
        counted = 0
        while counted < n:
            d += timedelta(days=1)
            if self.is_business_day(d):
                counted += 1
        return d

    def business_days_elapsed(self, start: date, today: date) -> int:
        """Business days after start, up to and including today."""
        if today <= start:
            return 0
        n, d = 0, start
        while d < today:
            d += timedelta(days=1)
            if self.is_business_day(d):
                n += 1
        return n
