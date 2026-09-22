#!/usr/bin/env python3
"""Normalize functional internal-link parity across 94 TadabburLife session landings.

Only navigation outside <article> is modified:
- breadcrumb gains a visible reciprocal ID/EN link;
- session navigation always has previous / language hub / next slots;
- existing previous/next anchor copy is preserved when present.

Article content is asserted byte-for-byte unchanged. Related-session choices are
not rewritten; they are validated for ID/EN target parity to avoid editorial drift.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from typing import Any

REPORT_DIR = Path("qc-internal-links-report")
REPORT_DIR.mkdir(exist_ok=True)

ID_PATHS = [Path("tadabbur") / f"{n:03d}" / "index.html" for n in range(1, 48)]
EN_PATHS = [Path("en/tadabbur") / f"{n:03d}" / "index.html" for n in range(1, 48)]
ALL_PATHS = ID_PATHS + EN_PATHS

BREAD_RE = re.compile(r'<nav\s+class=["\']breadcrumb["\'][^>]*>.*?</nav>', re.I | re.S)
SEO_NAV_RE = re.compile(r'<nav\s+class=["\']seo-nav["\'][^>]*>.*?</nav>', re.I | re.S)
RELATED_RE = re.compile(r'<aside\s+class=["\']related["\'][^>]*>.*?</aside>', re.I | re.S)
ARTICLE_RE = re.compile(r'<article\b[^>]*>.*?</article>', re.I | re.S)
CTA_RE = re.compile(r'<a\b[^>]*class=["\'][^"\']*(?:reader-cta|cta)[^"\']*["\'][^>]*>.*?</a>', re.I | re.S)
A_RE = re.compile(r'<a\b([^>]*)>(.*?)</a>', re.I | re.S)
HREF_RE = re.compile(r'\bhref=["\']([^"\']+)["\']', re.I)

def strip_tags(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()

def article_block(text: str) -> str:
    m = ARTICLE_RE.search(text)
    return m.group(0) if m else ""

def hrefs(block: str) -> list[tuple[str, str]]:
    out = []
    for attrs, inner in A_RE.findall(block):
        hm = HREF_RE.search(attrs)
        if hm:
            out.append((hm.group(1), inner))
    return out

def related_targets(text: str) -> list[int]:
    m = RELATED_RE.search(text)
    if not m:
        return []
    targets = []
    for href, _ in hrefs(m.group(0)):
        mm = re.fullmatch(r"\.\./(\d{3})/", href)
        if mm:
            targets.append(int(mm.group(1)))
    return targets

def find_nav_anchor(text: str, target_href: str) -> str | None:
    m = SEO_NAV_RE.search(text)
    if not m:
        return None
    for href, inner in hrefs(m.group(0)):
        if href == target_href:
            return f'<a href="{href}">{inner}</a>'
    return None

def normalize_one(path: Path, n: int, is_en: bool) -> dict[str, Any]:
    original = path.read_text(encoding="utf-8")
    original_article = article_block(original)
    if not original_article:
        raise RuntimeError(f"{path}: article block missing")

    # Breadcrumb: retain homepage first, add visible reciprocal language pair.
    if is_en:
        breadcrumb = (
            f'<nav class="breadcrumb" aria-label="Breadcrumb">'
            f'<a href="../../../">TadabburLife</a> › Session {n:03d} · '
            f'<a href="../../../tadabbur/{n:03d}/" hreflang="id" lang="id">Bahasa Indonesia</a>'
            f'</nav>'
        )
        hub_label = "All Reflections"
        nav_label = "Session navigation"
    else:
        breadcrumb = (
            f'<nav class="breadcrumb" aria-label="Breadcrumb">'
            f'<a href="../../">TadabburLife</a> › Sesi {n:03d} · '
            f'<a href="../../en/tadabbur/{n:03d}/" hreflang="en" lang="en">English</a>'
            f'</nav>'
        )
        hub_label = "Daftar Tadabbur"
        nav_label = "Navigasi sesi"

    updated, count = BREAD_RE.subn(breadcrumb, original, count=1)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly one breadcrumb")

    # Preserve existing prev/next anchor text if present.
    prev_href = f"../{n-1:03d}/" if n > 1 else None
    next_href = f"../{n+1:03d}/" if n < 47 else None
    prev_anchor = find_nav_anchor(original, prev_href) if prev_href else None
    next_anchor = find_nav_anchor(original, next_href) if next_href else None

    if n > 1 and not prev_anchor:
        label = f"← Session {n-1:03d}" if is_en else f"← Sesi {n-1:03d}"
        prev_anchor = f'<a href="{prev_href}">{label}</a>'
    if n < 47 and not next_anchor:
        label = f"Session {n+1:03d} →" if is_en else f"Sesi {n+1:03d} →"
        next_anchor = f'<a href="{next_href}">{label}</a>'

    prev_slot = prev_anchor or "<span></span>"
    next_slot = next_anchor or "<span></span>"
    hub_anchor = f'<a href="../">{hub_label}</a>'
    nav = f'<nav class="seo-nav" aria-label="{nav_label}">{prev_slot}{hub_anchor}{next_slot}</nav>'

    updated, count = SEO_NAV_RE.subn(nav, updated, count=1)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly one seo-nav")

    if article_block(updated) != original_article:
        raise RuntimeError(f"{path}: ARTICLE CHANGED — aborting")

    # Related block and CTA must remain byte-for-byte unchanged by this normalizer.
    old_related = RELATED_RE.search(original)
    new_related = RELATED_RE.search(updated)
    if (old_related.group(0) if old_related else "") != (new_related.group(0) if new_related else ""):
        raise RuntimeError(f"{path}: related block changed unexpectedly")
    old_cta = CTA_RE.search(original)
    new_cta = CTA_RE.search(updated)
    if (old_cta.group(0) if old_cta else "") != (new_cta.group(0) if new_cta else ""):
        raise RuntimeError(f"{path}: CTA changed unexpectedly")

    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")

    return {
        "path": str(path),
        "changed": changed,
        "article_unchanged": article_block(updated) == original_article,
        "related_targets": related_targets(updated),
    }

def qc_one(path: Path, n: int, is_en: bool) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []

    bread = BREAD_RE.search(text)
    nav = SEO_NAV_RE.search(text)
    related = RELATED_RE.search(text)
    cta = CTA_RE.search(text)

    if not bread:
        issues.append("missing_breadcrumb")
    else:
        b = bread.group(0)
        expected_home = "../../../" if is_en else "../../"
        expected_pair = f"../../../tadabbur/{n:03d}/" if is_en else f"../../en/tadabbur/{n:03d}/"
        bhrefs = [h for h, _ in hrefs(b)]
        if expected_home not in bhrefs:
            issues.append("breadcrumb_home")
        if expected_pair not in bhrefs:
            issues.append("language_pair_link")

    if not nav:
        issues.append("missing_seo_nav")
    else:
        nhrefs = [h for h, _ in hrefs(nav.group(0))]
        if "../" not in nhrefs:
            issues.append("missing_hub_link")
        if n > 1 and f"../{n-1:03d}/" not in nhrefs:
            issues.append("missing_prev")
        if n == 1 and any(re.fullmatch(r"\.\./000/", x) for x in nhrefs):
            issues.append("invalid_prev")
        if n < 47 and f"../{n+1:03d}/" not in nhrefs:
            issues.append("missing_next")
        if n == 47 and any(re.fullmatch(r"\.\./048/", x) for x in nhrefs):
            issues.append("invalid_next")

    rel_targets = related_targets(text)
    if not related:
        issues.append("missing_related")
    elif len(rel_targets) < 1:
        issues.append("related_no_session_links")
    elif n in rel_targets:
        issues.append("related_self_link")
    elif any(x < 1 or x > 47 for x in rel_targets):
        issues.append("related_out_of_range")

    if not cta:
        issues.append("missing_reader_cta")
    else:
        block = cta.group(0)
        expected_lang = "en" if is_en else "id"
        if f"session={n}" not in block or f"lang={expected_lang}" not in block:
            issues.append("reader_cta_target")

    return {
        "path": str(path),
        "pass": not issues,
        "issues": issues,
        "related_targets": rel_targets,
    }

def main() -> int:
    missing = [str(p) for p in ALL_PATHS if not p.exists()]
    if missing:
        print("Missing landing files:", missing)
        return 1

    normalization = []
    for n in range(1, 48):
        normalization.append(normalize_one(ID_PATHS[n-1], n, False))
        normalization.append(normalize_one(EN_PATHS[n-1], n, True))

    qc = []
    pair_issues = []
    for n in range(1, 48):
        id_qc = qc_one(ID_PATHS[n-1], n, False)
        en_qc = qc_one(EN_PATHS[n-1], n, True)
        qc += [id_qc, en_qc]
        if id_qc["related_targets"] != en_qc["related_targets"]:
            pair_issues.append({
                "session": n,
                "id": id_qc["related_targets"],
                "en": en_qc["related_targets"],
            })

    failures = [x for x in qc if not x["pass"]]
    summary = {
        "files_expected": 94,
        "files_checked": len(qc),
        "files_changed": sum(1 for x in normalization if x["changed"]),
        "article_unchanged_count": sum(1 for x in normalization if x["article_unchanged"]),
        "page_pass_count": sum(1 for x in qc if x["pass"]),
        "page_fail_count": len(failures),
        "related_pair_parity_count": 47 - len(pair_issues),
        "related_pair_mismatch_count": len(pair_issues),
        "overall_pass": len(qc) == 94 and not failures and not pair_issues
            and all(x["article_unchanged"] for x in normalization),
    }

    payload = {
        "summary": summary,
        "normalization": normalization,
        "qc": qc,
        "related_pair_issues": pair_issues,
    }
    (REPORT_DIR / "internal-link-parity-report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        "# TadabburLife Internal-Link Parity QC",
        "",
        f"- Landing files checked: {summary['files_checked']} / 94",
        f"- Files changed: {summary['files_changed']}",
        f"- Article content unchanged: {summary['article_unchanged_count']} / 94",
        f"- Page structural link PASS: {summary['page_pass_count']} / 94",
        f"- Related-session ID/EN target parity: {summary['related_pair_parity_count']} / 47 pairs",
        f"- Pair mismatches: {summary['related_pair_mismatch_count']}",
        f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}",
        "",
    ]
    if failures:
        lines += ["## Page failures", ""]
        lines += [f"- `{x['path']}`: {', '.join(x['issues'])}" for x in failures]
        lines.append("")
    if pair_issues:
        lines += ["## Related target mismatches", ""]
        for x in pair_issues:
            lines.append(f"- Session {x['session']:03d}: ID={x['id']} EN={x['en']}")
    (REPORT_DIR / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    if failures:
        for x in failures:
            print("PAGE FAIL", x["path"], x["issues"])
    if pair_issues:
        for x in pair_issues:
            print("PAIR FAIL", x)
    return 0 if summary["overall_pass"] else 1

if __name__ == "__main__":
    sys.exit(main())
