#!/usr/bin/env python3
"""Live functional internal-link parity QC for 94 TadabburLife session landings."""

from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE = "https://tadabburlife.com"
WORKERS = 12
TIMEOUT = 20
MAX_PROPAGATION_ATTEMPTS = 6
PROPAGATION_SLEEP = 15
USER_AGENT = "Mozilla/5.0 (compatible; TadabburLifeInternalLinkQC/1.0; +https://tadabburlife.com/)"

OUT = Path("qc-live-internal-links-report")
OUT.mkdir(exist_ok=True)

BREAD_RE = re.compile(r'<nav\s+class=["\']breadcrumb["\'][^>]*>.*?</nav>', re.I | re.S)
SEO_NAV_RE = re.compile(r'<nav\s+class=["\']seo-nav["\'][^>]*>.*?</nav>', re.I | re.S)
RELATED_RE = re.compile(r'<aside\s+class=["\']related["\'][^>]*>.*?</aside>', re.I | re.S)
CTA_RE = re.compile(r'<a\b[^>]*class=["\'][^"\']*(?:reader-cta|cta)[^"\']*["\'][^>]*>.*?</a>', re.I | re.S)
A_RE = re.compile(r'<a\b([^>]*)>(.*?)</a>', re.I | re.S)
HREF_RE = re.compile(r'\bhref=["\']([^"\']+)["\']', re.I)

def hrefs(block: str) -> list[str]:
    out = []
    for attrs, _ in A_RE.findall(block):
        m = HREF_RE.search(attrs)
        if m:
            out.append(html.unescape(m.group(1)))
    return out

def related_targets(text: str) -> list[int]:
    m = RELATED_RE.search(text)
    if not m:
        return []
    vals = []
    for href in hrefs(m.group(0)):
        mm = re.fullmatch(r"\.\./(\d{3})/", href)
        if mm:
            vals.append(int(mm.group(1)))
    return vals

def fetch(url: str):
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
                return r.status, r.geturl(), r.read().decode(
                    r.headers.get_content_charset() or "utf-8", errors="replace"
                ), ""
        except Exception as exc:
            last = repr(exc)
            if attempt < 2:
                time.sleep(1 + attempt)
    return None, "", "", last

def inspect(url: str, n: int, is_en: bool):
    status, final, text, error = fetch(url)
    issues = []

    if status != 200:
        issues.append(f"http_{status}")
    if final != url:
        issues.append("final_url_mismatch")

    bread = BREAD_RE.search(text)
    nav = SEO_NAV_RE.search(text)
    related = RELATED_RE.search(text)
    cta = CTA_RE.search(text)

    if not bread:
        issues.append("missing_breadcrumb")
    else:
        bhrefs = hrefs(bread.group(0))
        expected_home = "../../../" if is_en else "../../"
        expected_pair = (
            f"../../../tadabbur/{n:03d}/"
            if is_en
            else f"../../en/tadabbur/{n:03d}/"
        )
        if expected_home not in bhrefs:
            issues.append("breadcrumb_home")
        if expected_pair not in bhrefs:
            issues.append("language_pair_link")

    if not nav:
        issues.append("missing_seo_nav")
    else:
        nhrefs = hrefs(nav.group(0))
        if "../" not in nhrefs:
            issues.append("missing_hub_link")
        if n > 1 and f"../{n-1:03d}/" not in nhrefs:
            issues.append("missing_prev")
        if n < 47 and f"../{n+1:03d}/" not in nhrefs:
            issues.append("missing_next")
        if n == 1 and "../000/" in nhrefs:
            issues.append("invalid_prev")
        if n == 47 and "../048/" in nhrefs:
            issues.append("invalid_next")

    targets = related_targets(text)
    if not related:
        issues.append("missing_related")
    elif not targets:
        issues.append("related_no_session_links")
    elif n in targets:
        issues.append("related_self_link")
    elif any(x < 1 or x > 47 for x in targets):
        issues.append("related_out_of_range")

    if not cta:
        issues.append("missing_reader_cta")
    else:
        expected_lang = "en" if is_en else "id"
        block = cta.group(0)
        if f"session={n}" not in block or f"lang={expected_lang}" not in block:
            issues.append("reader_cta_target")

    return {
        "url": url,
        "session": n,
        "language": "en" if is_en else "id",
        "status": status,
        "final_url": final,
        "related_targets": targets,
        "issues": issues,
        "pass": not issues,
        "error": error,
    }

def run_once():
    specs = []
    for n in range(1, 48):
        specs.append((f"{BASE}/tadabbur/{n:03d}/", n, False))
        specs.append((f"{BASE}/en/tadabbur/{n:03d}/", n, True))

    rows = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(inspect, *spec): spec for spec in specs}
        for fut in as_completed(futs):
            rows.append(fut.result())
    rows.sort(key=lambda x: (x["session"], x["language"]))

    pair_issues = []
    for n in range(1, 48):
        id_row = next(x for x in rows if x["session"] == n and x["language"] == "id")
        en_row = next(x for x in rows if x["session"] == n and x["language"] == "en")
        if id_row["related_targets"] != en_row["related_targets"]:
            pair_issues.append({
                "session": n,
                "id": id_row["related_targets"],
                "en": en_row["related_targets"],
            })

    failures = [x for x in rows if not x["pass"]]
    summary = {
        "urls_expected": 94,
        "urls_checked": len(rows),
        "http_200_count": sum(1 for x in rows if x["status"] == 200),
        "page_pass_count": sum(1 for x in rows if x["pass"]),
        "page_fail_count": len(failures),
        "related_pair_parity_count": 47 - len(pair_issues),
        "related_pair_mismatch_count": len(pair_issues),
        "overall_pass": len(rows) == 94 and not failures and not pair_issues,
    }
    return summary, rows, failures, pair_issues

def main():
    final = None
    for attempt in range(1, MAX_PROPAGATION_ATTEMPTS + 1):
        summary, rows, failures, pair_issues = run_once()
        print(f"Attempt {attempt}/{MAX_PROPAGATION_ATTEMPTS}: {json.dumps(summary)}")
        final = (summary, rows, failures, pair_issues)
        if summary["overall_pass"]:
            break
        if attempt < MAX_PROPAGATION_ATTEMPTS:
            print(f"Live parity not ready; waiting {PROPAGATION_SLEEP}s for Pages/cache propagation...")
            time.sleep(PROPAGATION_SLEEP)

    summary, rows, failures, pair_issues = final
    payload = {
        "summary": summary,
        "rows": rows,
        "related_pair_issues": pair_issues,
    }
    (OUT / "live-internal-link-parity-report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = [
        "# TadabburLife Live Internal-Link Parity QC",
        "",
        f"- URLs checked: {summary['urls_checked']} / 94",
        f"- HTTP 200: {summary['http_200_count']} / 94",
        f"- Page structural link PASS: {summary['page_pass_count']} / 94",
        f"- Related ID/EN pair parity: {summary['related_pair_parity_count']} / 47",
        f"- Pair mismatches: {summary['related_pair_mismatch_count']}",
        f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}",
        "",
    ]
    if failures:
        lines += ["## Page failures", ""]
        lines += [f"- `{x['url']}`: {', '.join(x['issues'])}" for x in failures]
        lines.append("")
    if pair_issues:
        lines += ["## Related pair mismatches", ""]
        lines += [
            f"- Session {x['session']:03d}: ID={x['id']} EN={x['en']}"
            for x in pair_issues
        ]
    (OUT / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return 0 if summary["overall_pass"] else 1

if __name__ == "__main__":
    sys.exit(main())
