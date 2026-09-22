#!/usr/bin/env python3
"""Verify seo/keyword-map.json implementation snapshots against 94 live landings."""

from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

BASE = "https://tadabburlife.com"
MAP_PATH = Path("seo/keyword-map.json")
OUT = Path("qc-live-keyword-map-report")
OUT.mkdir(exist_ok=True)
WORKERS = 12
TIMEOUT = 20
USER_AGENT = "Mozilla/5.0 (compatible; TadabburLifeKeywordMapQC/1.0; +https://tadabburlife.com/)"

A_RE = re.compile(r'<a\b([^>]*)>(.*?)</a>', re.I | re.S)
HREF_RE = re.compile(r'\bhref=["\']([^"\']+)["\']', re.I)
RELATED_RE = re.compile(r'<aside\s+class=["\']related["\'][^>]*>.*?</aside>', re.I | re.S)
CTA_RE = re.compile(r'<a\b[^>]*class=["\'][^"\']*(?:reader-cta|cta)[^"\']*["\'][^>]*>.*?</a>', re.I | re.S)

def first(pattern: str, text: str) -> str:
    m = re.search(pattern, text, re.I | re.S)
    return html.unescape(m.group(1).strip()) if m else ""

def strip_tags(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()

class SignalParser(HTMLParser):
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

def signals(text: str) -> SignalParser:
    p = SignalParser()
    p.feed(text)
    return p

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

def reader_url(text: str) -> str:
    m = CTA_RE.search(text)
    if not m:
        return ""
    href = first(r'\bhref=["\']([^"\']+)["\']', m.group(0))
    if href.startswith("https://"):
        return href
    q = href.split("?", 1)[1] if "?" in href else ""
    return BASE + "/" + ("?" + q if q else "")

def fetch(url: str) -> tuple[int | None, str, str, str]:
    last = ""
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                },
            )
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return (
                    r.status,
                    r.geturl(),
                    r.read().decode(r.headers.get_content_charset() or "utf-8", errors="replace"),
                    "",
                )
        except Exception as exc:
            last = repr(exc)
            if attempt < 2:
                time.sleep(1 + attempt)
    return None, "", "", last

def live_snapshot(url: str) -> tuple[dict[str, Any], dict[str, Any]]:
    status, final, text, error = fetch(url)
    sig = signals(text)
    snap = {
        "canonical": sig.canonical,
        "reader": reader_url(text),
        "seo_title": strip_tags(first(r"<title\b[^>]*>(.*?)</title>", text)),
        "meta_description": sig.meta_description,
        "h1": strip_tags(first(r"<h1\b[^>]*>(.*?)</h1>", text)),
        "html_lang": sig.html_lang,
        "related_sessions": related_sessions(text),
    }
    transport = {
        "status": status,
        "final_url": final,
        "error": error,
    }
    return snap, transport

def check_one(session: dict[str, Any], lang: str) -> dict[str, Any]:
    sid = session["session"]
    n = int(sid)
    url = (
        f"{BASE}/en/tadabbur/{sid}/"
        if lang == "en"
        else f"{BASE}/tadabbur/{sid}/"
    )
    expected = (session.get("implementation", {}) or {}).get(lang, {})
    live, transport = live_snapshot(url)
    issues = []
    if transport["status"] != 200:
        issues.append(f"http_{transport['status']}")
    if transport["final_url"] != url:
        issues.append("final_url_mismatch")
    if not expected:
        issues.append("missing_map_implementation")
    else:
        for key in (
            "canonical", "reader", "seo_title", "meta_description",
            "h1", "html_lang", "related_sessions"
        ):
            if expected.get(key) != live.get(key):
                issues.append(f"{key}_mismatch")
    return {
        "session": sid,
        "language": lang,
        "url": url,
        "pass": not issues,
        "issues": issues,
        "expected": expected,
        "live": live,
        **transport,
    }

def main() -> int:
    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    sessions = data.get("sessions", [])
    if len(sessions) != 47:
        print(f"Expected 47 sessions, found {len(sessions)}", file=sys.stderr)
        return 1

    rows = []
    specs = [(s, lang) for s in sessions for lang in ("id", "en")]
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(check_one, s, lang): (s["session"], lang) for s, lang in specs}
        for i, fut in enumerate(as_completed(futs), 1):
            row = fut.result()
            rows.append(row)
            print(
                f"[{i:02d}/94] {'PASS' if row['pass'] else 'FAIL'} "
                f"{row['url']}"
                + (f" :: {','.join(row['issues'])}" if row["issues"] else "")
            )

    rows.sort(key=lambda x: (x["session"], x["language"]))
    failures = [x for x in rows if not x["pass"]]

    pair_issues = []
    for s in sessions:
        sid = s["session"]
        id_row = next(x for x in rows if x["session"] == sid and x["language"] == "id")
        en_row = next(x for x in rows if x["session"] == sid and x["language"] == "en")
        if id_row["live"]["related_sessions"] != en_row["live"]["related_sessions"]:
            pair_issues.append({
                "session": sid,
                "id": id_row["live"]["related_sessions"],
                "en": en_row["live"]["related_sessions"],
            })

    deep_ok = 0
    directional_ok = 0
    research_issues = []
    for n, s in enumerate(sessions, 1):
        id_ev = (s.get("seo", {}).get("id", {}) or {}).get("demand_evidence", "")
        en_ev = (s.get("seo", {}).get("en", {}) or {}).get("demand_evidence", "")
        if n <= 16:
            if id_ev.startswith("deep-live-serp-validated") and en_ev.startswith("deep-live-serp-validated"):
                deep_ok += 1
            else:
                research_issues.append({"session": s["session"], "expected": "deep-live-serp-validated", "id": id_ev, "en": en_ev})
        else:
            if id_ev == "serp-directional" and en_ev == "serp-directional":
                directional_ok += 1
            else:
                research_issues.append({"session": s["session"], "expected": "serp-directional", "id": id_ev, "en": en_ev})

    summary = {
        "sessions_checked": 47,
        "live_implementations_checked": len(rows),
        "http_200_count": sum(1 for x in rows if x["status"] == 200),
        "map_live_pass_count": sum(1 for x in rows if x["pass"]),
        "map_live_fail_count": len(failures),
        "related_pair_parity_count": 47 - len(pair_issues),
        "related_pair_mismatch_count": len(pair_issues),
        "deep_serp_boundary_pass_count": deep_ok,
        "directional_boundary_pass_count": directional_ok,
        "research_boundary_issue_count": len(research_issues),
        "overall_pass": (
            len(rows) == 94
            and not failures
            and not pair_issues
            and deep_ok == 16
            and directional_ok == 31
            and not research_issues
        ),
    }

    payload = {
        "summary": summary,
        "rows": rows,
        "related_pair_issues": pair_issues,
        "research_boundary_issues": research_issues,
    }
    (OUT / "live-keyword-map-report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = [
        "# TadabburLife Live Keyword-Map ↔ Landing QC",
        "",
        f"- Sessions checked: {summary['sessions_checked']} / 47",
        f"- Live implementations checked: {summary['live_implementations_checked']} / 94",
        f"- HTTP 200: {summary['http_200_count']} / 94",
        f"- Map ↔ live PASS: {summary['map_live_pass_count']} / 94",
        f"- Related ID/EN parity: {summary['related_pair_parity_count']} / 47",
        f"- Deep SERP boundary 001–016: {summary['deep_serp_boundary_pass_count']} / 16",
        f"- Directional boundary 017–047: {summary['directional_boundary_pass_count']} / 31",
        f"- Failures: {summary['map_live_fail_count']}",
        f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}",
        "",
    ]
    if failures:
        lines += ["## Map/live failures", ""]
        for row in failures:
            lines.append(f"- `{row['url']}`: {', '.join(row['issues'])}")
    if pair_issues:
        lines += ["", "## Related pair mismatches", ""]
        for row in pair_issues:
            lines.append(f"- Session {row['session']}: ID={row['id']} EN={row['en']}")
    if research_issues:
        lines += ["", "## Research-boundary issues", ""]
        for row in research_issues:
            lines.append(f"- Session {row['session']}: expected {row['expected']}")

    (OUT / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["overall_pass"] else 1

if __name__ == "__main__":
    sys.exit(main())
