#!/usr/bin/env python3
"""Synchronize seo/keyword-map.json implementation signals with 94 source landings.

This does NOT invent or rewrite keyword targets. It preserves all existing
research fields and adds/refreshes a technical implementation snapshot for
both Indonesian and English landings:
canonical, reader, title, meta, H1, lang, related sessions.

The published Sessions 001–047 corpus is Deep Live SERP validated. This script only synchronizes technical implementation snapshots and must not invent or alter research evidence.
"""

from __future__ import annotations

import html
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from html.parser import HTMLParser

MAP_PATH = Path("seo/keyword-map.json")
REPORT_DIR = Path("qc-keyword-map-report")
REPORT_DIR.mkdir(exist_ok=True)

A_RE = re.compile(r'<a\b([^>]*)>(.*?)</a>', re.I | re.S)
HREF_RE = re.compile(r'\bhref=["\']([^"\']+)["\']', re.I)
RELATED_RE = re.compile(r'<aside\s+class=["\']related["\'][^>]*>.*?</aside>', re.I | re.S)
CTA_RE = re.compile(r'<a\b[^>]*class=["\'][^"\']*(?:reader-cta|cta)[^"\']*["\'][^>]*>.*?</a>', re.I | re.S)

def first(pattern: str, text: str) -> str:
    m = re.search(pattern, text, re.I | re.S)
    return html.unescape(m.group(1).strip()) if m else ""

def strip_tags(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()

class HeadSignalParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.canonical = ""
        self.meta_description = ""
        self.html_lang = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        d = {k.lower(): (v or "") for k, v in attrs}
        t = tag.lower()
        if t == "html" and not self.html_lang:
            self.html_lang = d.get("lang", "")
        elif t == "link" and not self.canonical:
            rel = {x.strip().lower() for x in d.get("rel", "").split()}
            if "canonical" in rel:
                self.canonical = d.get("href", "")
        elif t == "meta" and not self.meta_description:
            if d.get("name", "").lower() == "description":
                self.meta_description = d.get("content", "")


def head_signals(text: str) -> HeadSignalParser:
    p = HeadSignalParser()
    p.feed(text)
    return p


def canonical(text: str) -> str:
    return head_signals(text).canonical


def meta_description(text: str) -> str:
    return head_signals(text).meta_description


def page_title(text: str) -> str:
    return strip_tags(first(r"<title\b[^>]*>(.*?)</title>", text))


def h1(text: str) -> str:
    return strip_tags(first(r"<h1\b[^>]*>(.*?)</h1>", text))


def html_lang(text: str) -> str:
    return head_signals(text).html_lang


def links(block: str) -> list[str]:
    out = []
    for attrs, _ in A_RE.findall(block):
        m = HREF_RE.search(attrs)
        if m:
            out.append(html.unescape(m.group(1)))
    return out

def related_sessions(text: str) -> list[str]:
    m = RELATED_RE.search(text)
    if not m:
        return []
    out = []
    for href in links(m.group(0)):
        mm = re.fullmatch(r"\.\./(\d{3})/", href)
        if mm:
            out.append(mm.group(1))
    return out

def reader_url(text: str, n: int, is_en: bool) -> str:
    m = CTA_RE.search(text)
    if not m:
        return ""
    href = first(r'\bhref=["\']([^"\']+)["\']', m.group(0))
    if not href:
        return ""
    # Normalize relative and absolute CTA hrefs to canonical absolute URL.
    if href.startswith("https://"):
        return href
    prefix = "https://tadabburlife.com/"
    # Known reader links point to ../../../?... or ../../?...
    q = href.split("?", 1)[1] if "?" in href else ""
    return prefix + ("?" + q if q else "")

def landing_path(n: int, is_en: bool) -> Path:
    return Path("en/tadabbur" if is_en else "tadabbur") / f"{n:03d}" / "index.html"

def expected_canonical(n: int, is_en: bool) -> str:
    if is_en:
        return f"https://tadabburlife.com/en/tadabbur/{n:03d}/"
    return f"https://tadabburlife.com/tadabbur/{n:03d}/"

def expected_reader(n: int, is_en: bool) -> str:
    return f"https://tadabburlife.com/?session={n}&lang={'en' if is_en else 'id'}"

def snapshot(n: int, is_en: bool) -> dict[str, Any]:
    path = landing_path(n, is_en)
    text = path.read_text(encoding="utf-8")
    return {
        "canonical": canonical(text),
        "reader": reader_url(text, n, is_en),
        "seo_title": page_title(text),
        "meta_description": meta_description(text),
        "h1": h1(text),
        "html_lang": html_lang(text),
        "related_sessions": related_sessions(text),
    }

def validate_snapshot(n: int, is_en: bool, snap: dict[str, Any]) -> list[str]:
    issues = []
    lang = "en" if is_en else "id"
    if snap["canonical"] != expected_canonical(n, is_en):
        issues.append("canonical")
    if snap["reader"] != expected_reader(n, is_en):
        issues.append("reader")
    if not snap["seo_title"]:
        issues.append("seo_title")
    if not snap["meta_description"]:
        issues.append("meta_description")
    if not snap["h1"]:
        issues.append("h1")
    if snap["html_lang"] != lang:
        issues.append("html_lang")
    if not snap["related_sessions"]:
        issues.append("related_sessions_missing")
    if f"{n:03d}" in snap["related_sessions"]:
        issues.append("related_self")
    if any(int(x) < 1 or int(x) > 47 for x in snap["related_sessions"]):
        issues.append("related_out_of_range")
    return issues

def main() -> int:
    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    sessions = data.get("sessions", [])
    if len(sessions) != 47:
        print(f"Expected 47 keyword-map sessions, found {len(sessions)}", file=sys.stderr)
        return 1

    ids = [s.get("session") for s in sessions]
    expected_ids = [f"{n:03d}" for n in range(1, 48)]
    if ids != expected_ids:
        print("Keyword-map session IDs/order are not exactly 001–047", file=sys.stderr)
        return 1

    rows = []
    map_changes = 0
    deep_ok = 0
    directional_ok = 0
    research_boundary_issues = []

    for n, entry in enumerate(sessions, 1):
        sid = f"{n:03d}"
        id_snap = snapshot(n, False)
        en_snap = snapshot(n, True)

        id_issues = validate_snapshot(n, False, id_snap)
        en_issues = validate_snapshot(n, True, en_snap)

        # Existing top-level fields are the established Indonesian implementation registry.
        top_mismatches = []
        top_expected = {
            "canonical": id_snap["canonical"],
            "reader": id_snap["reader"],
            "seo_title": id_snap["seo_title"],
            "meta_description": id_snap["meta_description"],
            "h1": id_snap["h1"],
            "related_sessions": id_snap["related_sessions"],
        }
        for key, value in top_expected.items():
            if entry.get(key) != value:
                top_mismatches.append({
                    "field": key,
                    "map": entry.get(key),
                    "source": value,
                })

        # Safe technical sync: established map top-level ID implementation follows source.
        # This does not touch locked_title, search targets, intent, cluster, or evidence.
        for key, value in top_expected.items():
            if entry.get(key) != value:
                entry[key] = value
                map_changes += 1

        implementation = {
            "synced_from": "source-landings",
            "synced_on": "2026-09-23",
            "id": id_snap,
            "en": en_snap,
        }
        if entry.get("implementation") != implementation:
            entry["implementation"] = implementation
            map_changes += 1

        # Research/evidence guardrail: all published Sessions 001–047 must remain Deep validated.
        id_ev = (entry.get("seo", {}).get("id", {}) or {}).get("demand_evidence", "")
        en_ev = (entry.get("seo", {}).get("en", {}) or {}).get("demand_evidence", "")
        ok = id_ev.startswith("deep-live-serp-validated") and en_ev.startswith("deep-live-serp-validated")
        if ok:
            deep_ok += 1
        else:
            research_boundary_issues.append({"session": sid, "expected": "deep-live-serp-validated", "id": id_ev, "en": en_ev})

        # Related graph is now intentionally paired across ID/EN.
        related_pair_match = id_snap["related_sessions"] == en_snap["related_sessions"]
        if not related_pair_match:
            en_issues.append("related_pair_mismatch")

        rows.append({
            "session": sid,
            "id_issues": id_issues,
            "en_issues": en_issues,
            "top_level_mismatches_before_sync": top_mismatches,
            "related_pair_match": related_pair_match,
            "id": id_snap,
            "en": en_snap,
        })

    data["generated"] = "2026-09-23"
    data["implementation_sync"] = {
        "status": "source-synced",
        "synced_on": "2026-09-23",
        "scope": "47 sessions x ID+EN = 94 landing implementations",
        "note": "Technical implementation snapshot only. It does not upgrade Deep SERP evidence or change keyword/search-intent research status.",
    }

    MAP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Re-read and assert implementation registry matches source after sync.
    final = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    final_issues = []
    for n, entry in enumerate(final["sessions"], 1):
        id_snap = snapshot(n, False)
        en_snap = snapshot(n, True)
        impl = entry.get("implementation", {})
        if impl.get("id") != id_snap:
            final_issues.append({"session": f"{n:03d}", "language": "id", "issue": "implementation_snapshot_mismatch"})
        if impl.get("en") != en_snap:
            final_issues.append({"session": f"{n:03d}", "language": "en", "issue": "implementation_snapshot_mismatch"})
        for key in ("canonical", "reader", "seo_title", "meta_description", "h1", "related_sessions"):
            if entry.get(key) != id_snap[key]:
                final_issues.append({"session": f"{n:03d}", "language": "id", "issue": f"top_level_{key}_mismatch"})

    source_failures = [
        {"session": r["session"], "id": r["id_issues"], "en": r["en_issues"]}
        for r in rows if r["id_issues"] or r["en_issues"]
    ]

    summary = {
        "sessions_expected": 47,
        "sessions_checked": len(rows),
        "landing_implementations_checked": len(rows) * 2,
        "source_implementation_pass_count": (len(rows) * 2) - sum(bool(r["id_issues"]) + bool(r["en_issues"]) for r in rows),
        "source_failure_count": len(source_failures),
        "related_pair_parity_count": sum(1 for r in rows if r["related_pair_match"]),
        "top_level_id_sessions_with_drift_before_sync": sum(1 for r in rows if r["top_level_mismatches_before_sync"]),
        "technical_map_changes": map_changes,
        "deep_serp_boundary_pass_count": deep_ok,
        "directional_boundary_pass_count": directional_ok,
        "research_boundary_issue_count": len(research_boundary_issues),
        "post_sync_registry_issue_count": len(final_issues),
        "overall_pass": (
            len(rows) == 47
            and not source_failures
            and all(r["related_pair_match"] for r in rows)
            and deep_ok == 47
            and directional_ok == 0
            and not research_boundary_issues
            and not final_issues
        ),
    }

    payload = {
        "summary": summary,
        "rows": rows,
        "research_boundary_issues": research_boundary_issues,
        "post_sync_registry_issues": final_issues,
    }
    (REPORT_DIR / "keyword-map-sync-report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = [
        "# TadabburLife Keyword-Map ↔ Landing Sync QC",
        "",
        f"- Sessions checked: {summary['sessions_checked']} / 47",
        f"- Landing implementations checked: {summary['landing_implementations_checked']} / 94",
        f"- Source implementation PASS: {summary['source_implementation_pass_count']} / 94",
        f"- Related-session pair parity: {summary['related_pair_parity_count']} / 47",
        f"- ID sessions with registry drift before safe sync: {summary['top_level_id_sessions_with_drift_before_sync']}",
        f"- Technical registry changes: {summary['technical_map_changes']}",
        f"- Deep SERP boundary (001–047): {summary['deep_serp_boundary_pass_count']} / 47",
        f"- Directional-only boundary remaining: {summary['directional_boundary_pass_count']} / 0",
        f"- Research-boundary issues: {summary['research_boundary_issue_count']}",
        f"- Post-sync registry issues: {summary['post_sync_registry_issue_count']}",
        f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}",
        "",
    ]
    if source_failures:
        lines += ["## Source implementation failures", ""]
        for row in source_failures:
            lines.append(f"- Session {row['session']}: ID={row['id']} EN={row['en']}")
    if research_boundary_issues:
        lines += ["", "## Research boundary issues", ""]
        for row in research_boundary_issues:
            lines.append(f"- Session {row['session']}: expected {row['expected']}; ID={row['id']} EN={row['en']}")
    if final_issues:
        lines += ["", "## Post-sync registry issues", ""]
        for row in final_issues:
            lines.append(f"- Session {row['session']} {row['language']}: {row['issue']}")

    (REPORT_DIR / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, indent=2))

    if not summary["overall_pass"]:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
