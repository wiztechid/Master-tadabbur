#!/usr/bin/env python3
"""Ayat ownership + anti-duplicate guard for TadabburLife."""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROGRESS = ROOT / "data" / "quran-progress.json"
REGISTRY = ROOT / "data" / "ayat-ownership.json"
INDEX = ROOT / "index.html"


def expand_ref(ref: str) -> list[str]:
    m = re.fullmatch(r"(\d+):(\d+)(?:-(\d+))?", ref.strip())
    if not m:
        raise ValueError(f"invalid_ref:{ref}")
    s, a, b = int(m.group(1)), int(m.group(2)), int(m.group(3) or m.group(2))
    if not (1 <= s <= 114) or a < 1 or b < a:
        raise ValueError(f"invalid_range:{ref}")
    return [f"{s}:{v}" for v in range(a, b + 1)]


def article(text: str, session: int, lang: str) -> str:
    cls = "session" if lang == "id" else "en-session"
    m = re.search(
        rf'<article class="{cls}"[^>]*data-session-number="{session}"[^>]*>(.*?)</article>',
        text,
        re.S,
    )
    return m.group(0) if m else ""


def source_blob() -> str:
    return "\n".join(
        p.read_text(encoding="utf-8")
        for p in sorted((ROOT / "data").glob("sessions-*.html"))
    )


def norm_arabic(value: str) -> str:
    value = html.unescape(re.sub(r"<[^>]+>", "", value))
    return re.sub(r"\s+", "", value)


def main() -> int:
    issues: list[str] = []
    data = json.loads(PROGRESS.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    source = source_blob()

    m_total = re.search(r"const TOTAL=(\d+)", INDEX.read_text(encoding="utf-8"))
    total = int(m_total.group(1)) if m_total else 0
    expected_ids = set(range(1, total + 1))
    sessions = data.get("sessions", [])
    ids = {int(s.get("id", 0)) for s in sessions}
    if ids != expected_ids:
        issues.append(f"session_inventory_mismatch:missing={sorted(expected_ids-ids)}:extra={sorted(ids-expected_ids)}")

    derived: dict[str, int] = {}
    session_map = {int(s["id"]): s for s in sessions}

    # Pass 1: build the full primary-owner map before validating cross-references.
    for s in sessions:
        sid = int(s["id"])
        mode = s.get("mode", "owner")
        owned = s.get("ayat", [])
        cross = s.get("crossReferences", [])

        if mode == "companion":
            if owned:
                issues.append(f"companion_has_owned_ayat:{sid}")
            if not cross:
                issues.append(f"companion_missing_crossref:{sid}")
        elif mode == "owner" and not owned:
            issues.append(f"owner_without_ayat:{sid}")

        for ref in owned:
            try:
                ayat = expand_ref(ref)
            except ValueError as exc:
                issues.append(str(exc))
                continue
            for a in ayat:
                if a in derived:
                    issues.append(f"duplicate_primary_owner:{a}:sessions={derived[a]},{sid}")
                else:
                    derived[a] = sid

    # Pass 2: every cross-reference must point to the already-established owner,
    # and both reader + public landing must carry an explicit owner link.
    for s in sessions:
        sid = int(s["id"])
        cross = s.get("crossReferences", [])
        id_article = article(source, sid, "id")
        en_article = article(source, sid, "en")
        if not id_article or not en_article:
            issues.append(f"missing_reader_article:{sid}")
            continue

        for x in cross:
            ref = str(x.get("ayat", ""))
            owner = int(x.get("ownerSession", 0))
            if owner == sid:
                issues.append(f"crossref_points_to_self:{sid}:{ref}")
            if owner not in session_map:
                issues.append(f"crossref_owner_missing_session:{sid}:{ref}:owner={owner}")
            try:
                ayat = expand_ref(ref)
            except ValueError as exc:
                issues.append(str(exc))
                continue

            for a in ayat:
                actual = derived.get(a)
                if actual is None:
                    issues.append(f"crossref_unowned_ayat:{sid}:{a}:declared={owner}")
                elif actual != owner:
                    issues.append(f"crossref_wrong_owner:{sid}:{a}:declared={owner}:actual={actual}")

            for lang, art in (("id", id_article), ("en", en_article)):
                marker = rf'data-owner-session="{owner}"'
                if marker not in art:
                    issues.append(f"missing_crossref_marker:{sid}:{lang}:{ref}:owner={owner}")
                expected_path = (
                    f'/tadabbur/{owner:03d}/'
                    if lang == "id"
                    else f'/en/tadabbur/{owner:03d}/'
                )
                if expected_path not in art:
                    issues.append(f"missing_crossref_link:{sid}:{lang}:{ref}:owner={owner}")

                landing = ROOT / (f"tadabbur/{sid:03d}/index.html" if lang == "id" else f"en/tadabbur/{sid:03d}/index.html")
                if not landing.exists():
                    issues.append(f"missing_landing:{sid}:{lang}")
                else:
                    lt = landing.read_text(encoding="utf-8")
                    if marker not in lt or expected_path not in lt:
                        issues.append(f"landing_crossref_missing:{sid}:{lang}:{ref}:owner={owner}")

    registry_owners = {str(k): int(v) for k, v in registry.get("owners", {}).items()}
    if registry_owners != {k: int(v) for k, v in sorted(derived.items())}:
        missing = sorted(set(derived) - set(registry_owners))
        extra = sorted(set(registry_owners) - set(derived))
        wrong = sorted(k for k in set(derived) & set(registry_owners) if derived[k] != registry_owners[k])
        issues.append(f"registry_drift:missing={missing}:extra={extra}:wrong={wrong}")
    if int(registry.get("ownerCount", -1)) != len(derived):
        issues.append(f"registry_owner_count:{registry.get('ownerCount')}:expected={len(derived)}")

    # Secondary safety net: the same Arabic verse segment should not be rendered
    # as a verse block in two different Indonesian reader sessions.
    arabic_owner: dict[str, int] = {}
    for sid in sorted(expected_ids):
        art = article(source, sid, "id")
        for block in re.findall(r'<div class="ayah">(.*?)</div>', art, re.S):
            for segment in re.split(r"\s*۝\s*", block):
                key = norm_arabic(segment)
                if len(key) < 12:
                    continue
                if key in arabic_owner and arabic_owner[key] != sid:
                    issues.append(f"duplicate_arabic_verse_block:sessions={arabic_owner[key]},{sid}")
                else:
                    arabic_owner[key] = sid

    summary = {
        "published_sessions": total,
        "owned_unique_ayat": len(derived),
        "companion_sessions": [s["id"] for s in sessions if s.get("mode") == "companion"],
        "cross_reference_count": sum(len(s.get("crossReferences", [])) for s in sessions),
        "issues": issues,
        "pass": not issues,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
