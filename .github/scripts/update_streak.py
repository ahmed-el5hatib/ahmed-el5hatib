#!/usr/bin/env python3
"""Auto-update the contribution streak card in README.md.

Runs daily via GitHub Actions. The current streak grows by 1 each day
and the total contributions grow by a fixed per-day amount.
Only the values between the HTML-comment markers are replaced, so the
rest of the README is never touched.
"""
import re
from datetime import date, timezone, datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration — tweak these freely.
# ---------------------------------------------------------------------------
STREAK_START = date(2026, 6, 13)      # day the current streak began
CONTRIB_BASE = 1200                   # contributions as of CONTRIB_BASE_DATE
CONTRIB_BASE_DATE = date(2026, 7, 14) # reference date for the base count
CONTRIB_PER_DAY = 3                   # contributions added per day
# ---------------------------------------------------------------------------

README = Path(__file__).resolve().parents[2] / "README.md"


def fmt(d: date) -> str:
    # e.g. "Jun 13, 2026" (strip leading zero on the day, cross-platform)
    return f"{d.strftime('%b')} {d.day}, {d.year}"


def replace(text: str, tag: str, value: str) -> str:
    pattern = re.compile(f"(<!--{tag}_START-->).*?(<!--{tag}_END-->)", re.DOTALL)
    return pattern.sub(lambda m: m.group(1) + value + m.group(2), text)


def main() -> None:
    today = datetime.now(timezone.utc).date()

    current_days = (today - STREAK_START).days + 1
    total = CONTRIB_BASE + max(0, (today - CONTRIB_BASE_DATE).days) * CONTRIB_PER_DAY
    date_range = f"{fmt(STREAK_START)} — {fmt(today)}"

    text = README.read_text(encoding="utf-8")
    text = replace(text, "TOTAL", f"{total:,}+")
    text = replace(text, "CURR", f"{current_days} Days")
    text = replace(text, "CURR_RANGE", date_range)
    text = replace(text, "LONG", f"{current_days} Days")
    text = replace(text, "LONG_RANGE", date_range)
    README.write_text(text, encoding="utf-8")

    print(f"Updated: current streak = {current_days} days, total = {total:,}+")


if __name__ == "__main__":
    main()
