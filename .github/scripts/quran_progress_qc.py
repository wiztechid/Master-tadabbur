#!/usr/bin/env python3
"""Integrity QC for TadabburLife Qur'an coverage progress."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "index.html"
PROGRESS = ROOT / "data" / "quran-progress.json"
MODULE_GLOB = "sessions-*.html"


def expand_ref(ref: str) -> set[str]:
    m = re.fullmatch(r"(\d+):(\d+)(?:-(\d+))?", ref.strip())
    if not m:
        raise ValueError(f"invalid ayat ref: {ref}")
    surah = int(m.group(1))
    start = int(m.group(2))
    end = int(m.group(3) or start)
    if not (1 <= surah <= 114) or start < 1 or end < start:
        raise ValueError(f"invalid ayat range: {ref}")
    return {f"{surah}:{v}" for v in range(start, end + 1)}


def main() -> int:
    issues: list[str] = []
    html = INDEX.read_text(encoding="utf-8")
    data = json.loads(PROGRESS.read_text(encoding="utf-8"))

    m_total = re.search(r"const TOTAL=(\d+)", html)
    if not m_total:
        issues.append("index_TOTAL_missing")
        published_total = 0
    else:
        published_total = int(m_total.group(1))

    expected_ids = set(range(1, published_total + 1))

    published_ids: set[int] = set()
    for path in sorted((ROOT / "data").glob(MODULE_GLOB)):
        text = path.read_text(encoding="utf-8")
        published_ids.update(int(n) for n in re.findall(r"<small>SESI\s+(\d{3})\b", text))
    published_ids = {n for n in published_ids if n <= published_total}
    if published_ids != expected_ids:
        issues.append(
            f"published_session_ids_mismatch:{sorted(expected_ids - published_ids)}"
            f":extra={sorted(published_ids - expected_ids)}"
        )

    sessions = data.get("sessions", [])
    ids = [int(s.get("id", 0)) for s in sessions]
    if len(ids) != len(set(ids)):
        issues.append("metadata_duplicate_session_ids")
    if set(ids) != expected_ids:
        issues.append(
            f"metadata_session_ids_mismatch:{sorted(expected_ids - set(ids))}"
            f":extra={sorted(set(ids) - expected_ids)}"
        )

    quran_total = int(data.get("quranTotalAyat", 0))
    if quran_total != 6236:
        issues.append(f"quran_total_{quran_total}_expected_6236")
    if data.get("countMode") != "unique_owned_ayat":
        issues.append("count_mode_must_be_unique_owned_ayat")

    unique: set[str] = set()
    mentions = 0
    try:
        for session in sessions:
            for ref in session.get("ayat", []):
                expanded = expand_ref(ref)
                mentions += len(expanded)
                unique.update(expanded)
    except ValueError as exc:
        issues.append(str(exc))

    discussed = len(unique)
    pct = (discussed / quran_total * 100) if quran_total else 0.0

    static_checks = {
        "stat_ayat": (r'id="stat-ayat">([^<]+)</b>', str(discussed)),
        "stat_total": (r'id="stat-total">([^<]+)</b>', f"{quran_total:,}".replace(",", ".")),
        "stat_sessions": (r'id="stat-sessions">([^<]+)</b>', str(published_total)),
    }
    for name, (pattern, expected) in static_checks.items():
        m = re.search(pattern, html)
        got = m.group(1).strip() if m else ""
        if got != expected:
            issues.append(f"{name}_static_mismatch:{got!r}_expected_{expected!r}")

    pct_id = f"{pct:.1f}".replace(".", ",")
    hero_expected = f"{discussed} dari {quran_total:,} ayat • {pct_id}% cakupan Al-Qur'an".replace(",", ".")
    m_hero = re.search(r'id="quran-progress-text">([^<]+)</small>', html)
    hero_got = m_hero.group(1).strip() if m_hero else ""
    if hero_got != hero_expected:
        issues.append(f"hero_static_mismatch:{hero_got!r}_expected_{hero_expected!r}")

    if "±1.000" in html or "approximately 1,000 sessions" in html:
        issues.append("legacy_session_target_progress_copy_present")

    summary = {
        "published_sessions": published_total,
        "metadata_sessions": len(sessions),
        "quran_total_ayat": quran_total,
        "unique_ayat_discussed": discussed,
        "owned_ayat_mentions": mentions,
        "coverage_percent": round(pct, 4),
        "issues": issues,
        "pass": not issues,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
