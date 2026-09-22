#!/usr/bin/env python3
"""Live custom-domain crawl QC for TadabburLife.

Crawls every canonical URL listed in the live sitemap and writes JSON/CSV/Markdown
reports. Uses Python stdlib only so it runs on GitHub-hosted runners without
additional dependencies.
"""

from __future__ import annotations

import csv
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE = "https://tadabburlife.com"
SITEMAP = BASE + "/sitemap.xml"
ROBOTS = BASE + "/robots.txt"
EXPECTED_SITEMAP_COUNT = 103
TIMEOUT = 20
RETRIES = 2
WORKERS = 12
USER_AGENT = "Mozilla/5.0 (compatible; TadabburLifeLiveQC/1.0; +https://tadabburlife.com/)"

REPORT_DIR = Path("qc-live-report")
REPORT_DIR.mkdir(exist_ok=True)


class RedirectTracker(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.redirects: list[dict[str, Any]] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.redirects.append({"status": code, "location": newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url: str, timeout: int = TIMEOUT) -> dict[str, Any]:
    last_error = None
    for attempt in range(RETRIES + 1):
        tracker = RedirectTracker()
        opener = urllib.request.build_opener(tracker)
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "id,en;q=0.8",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            },
        )
        started = time.time()
        try:
            with opener.open(req, timeout=timeout) as resp:
                raw = resp.read()
                charset = resp.headers.get_content_charset() or "utf-8"
                text = raw.decode(charset, errors="replace")
                return {
                    "ok": True,
                    "requested_url": url,
                    "status": getattr(resp, "status", None) or resp.getcode(),
                    "final_url": resp.geturl(),
                    "redirects": tracker.redirects,
                    "content_type": resp.headers.get("Content-Type", ""),
                    "cache_control": resp.headers.get("Cache-Control", ""),
                    "etag": resp.headers.get("ETag", ""),
                    "last_modified": resp.headers.get("Last-Modified", ""),
                    "bytes": len(raw),
                    "elapsed_ms": round((time.time() - started) * 1000),
                    "text": text,
                    "error": "",
                }
        except urllib.error.HTTPError as exc:
            body = b""
            try:
                body = exc.read()
            except Exception:
                pass
            return {
                "ok": False,
                "requested_url": url,
                "status": exc.code,
                "final_url": exc.geturl(),
                "redirects": tracker.redirects,
                "content_type": exc.headers.get("Content-Type", "") if exc.headers else "",
                "cache_control": exc.headers.get("Cache-Control", "") if exc.headers else "",
                "etag": exc.headers.get("ETag", "") if exc.headers else "",
                "last_modified": exc.headers.get("Last-Modified", "") if exc.headers else "",
                "bytes": len(body),
                "elapsed_ms": round((time.time() - started) * 1000),
                "text": body.decode("utf-8", errors="replace"),
                "error": f"HTTPError {exc.code}: {exc.reason}",
            }
        except Exception as exc:
            last_error = repr(exc)
            if attempt < RETRIES:
                time.sleep(1.2 * (attempt + 1))
                continue
    return {
        "ok": False,
        "requested_url": url,
        "status": None,
        "final_url": "",
        "redirects": [],
        "content_type": "",
        "cache_control": "",
        "etag": "",
        "last_modified": "",
        "bytes": 0,
        "elapsed_ms": None,
        "text": "",
        "error": last_error or "unknown error",
    }


def first(pattern: str, text: str, flags: int = re.I | re.S) -> str:
    m = re.search(pattern, text, flags)
    return html.unescape(m.group(1).strip()) if m else ""


def strip_tags(value: str) -> str:
    value = re.sub(r"<script\b[^>]*>.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style\b[^>]*>.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def extract_html_signals(text: str) -> dict[str, str]:
    return {
        "title": first(r"<title[^>]*>(.*?)</title>", text),
        "canonical": first(r"<link\b[^>]*\brel=[\"']canonical[\"'][^>]*\bhref=[\"']([^\"']+)", text)
        or first(r"<link\b[^>]*\bhref=[\"']([^\"']+)[\"'][^>]*\brel=[\"']canonical[\"']", text),
        "robots": first(r"<meta\b[^>]*\bname=[\"']robots[\"'][^>]*\bcontent=[\"']([^\"']*)", text)
        or first(r"<meta\b[^>]*\bcontent=[\"']([^\"']*)[\"'][^>]*\bname=[\"']robots[\"']", text),
        "h1": strip_tags(first(r"<h1\b[^>]*>(.*?)</h1>", text)),
    }


def classify(url: str, fetched: dict[str, Any]) -> dict[str, Any]:
    text = fetched.get("text", "")
    lower = text.lower()
    signals = extract_html_signals(text)
    issues: list[str] = []

    status = fetched.get("status")
    final_url = fetched.get("final_url", "")
    redirects = fetched.get("redirects", [])

    if status != 200:
        issues.append(f"http_status_{status}")
    if final_url != url:
        issues.append("final_url_mismatch")
    if redirects:
        issues.append("redirect_present")

    if "text/html" not in fetched.get("content_type", "").lower():
        issues.append("non_html_content_type")

    if signals["canonical"] != url:
        issues.append("canonical_mismatch_or_missing")

    robots = signals["robots"].lower()
    if "noindex" in robots:
        issues.append("noindex")
    if not signals["title"]:
        issues.append("missing_title")
    if not signals["h1"]:
        issues.append("missing_h1")

    visible = strip_tags(text).lower()
    soft404_terms = (
        "404 not found",
        "page not found",
        "halaman tidak ditemukan",
        "there isn't a github pages site here",
    )
    soft404 = status == 200 and (
        any(term in visible for term in soft404_terms) or fetched.get("bytes", 0) < 500
    )
    if soft404:
        issues.append("soft404_suspect")

    if "wiztechid.github.io/master-tadabbur" in lower:
        issues.append("legacy_github_url")
    if re.search(r"\bmaster\s+tadabbur\b", visible, flags=re.I):
        issues.append("legacy_master_tadabbur_brand")

    # Public-information-page stale-template checks.
    if url.endswith("/about/") and "tentang proyek" in visible:
        issues.append("stale_about_kicker")
    if url.endswith("/contact/"):
        if "mailto:info@tadabburlife.com" not in lower:
            issues.append("contact_email_missing")
        if "github repository" in visible or "repositori resmi tadabburlife di github" in visible:
            issues.append("stale_github_contact")

    return {
        "url": url,
        "status": status,
        "final_url": final_url,
        "redirect_count": len(redirects),
        "redirects": redirects,
        "content_type": fetched.get("content_type", ""),
        "cache_control": fetched.get("cache_control", ""),
        "etag": fetched.get("etag", ""),
        "last_modified": fetched.get("last_modified", ""),
        "bytes": fetched.get("bytes", 0),
        "elapsed_ms": fetched.get("elapsed_ms"),
        "title": signals["title"],
        "canonical": signals["canonical"],
        "robots": signals["robots"],
        "h1": signals["h1"],
        "soft404_suspect": soft404,
        "issues": issues,
        "pass": not issues,
        "error": fetched.get("error", ""),
    }


def main() -> int:
    started = datetime.now(timezone.utc)

    robots_resp = fetch(ROBOTS)
    sitemap_resp = fetch(SITEMAP)

    global_issues: list[str] = []

    robots_text = robots_resp.get("text", "")
    if robots_resp.get("status") != 200:
        global_issues.append("robots_not_200")
    if "User-agent: *" not in robots_text:
        global_issues.append("robots_missing_user_agent")
    if "Disallow: /owner/" not in robots_text:
        global_issues.append("robots_owner_disallow_missing")
    if f"Sitemap: {SITEMAP}" not in robots_text:
        global_issues.append("robots_sitemap_pointer_missing")

    if sitemap_resp.get("status") != 200:
        global_issues.append("sitemap_not_200")
        urls: list[str] = []
    else:
        try:
            root = ET.fromstring(sitemap_resp["text"])
            urls = [
                (node.text or "").strip()
                for node in root.findall(".//{*}loc")
                if (node.text or "").strip()
            ]
        except Exception as exc:
            global_issues.append(f"sitemap_parse_error:{exc!r}")
            urls = []

    if len(urls) != EXPECTED_SITEMAP_COUNT:
        global_issues.append(f"sitemap_count_{len(urls)}_expected_{EXPECTED_SITEMAP_COUNT}")
    if len(set(urls)) != len(urls):
        global_issues.append("sitemap_duplicate_urls")
    if any(not u.startswith(BASE + "/") and u != BASE + "/" for u in urls):
        global_issues.append("sitemap_noncanonical_host_or_scheme")

    print(f"Live sitemap URLs: {len(urls)}")
    print(f"Robots status: {robots_resp.get('status')} | Sitemap status: {sitemap_resp.get('status')}")

    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        future_map = {pool.submit(fetch, u): u for u in urls}
        completed = 0
        for fut in as_completed(future_map):
            url = future_map[fut]
            try:
                fetched = fut.result()
            except Exception as exc:
                fetched = {
                    "status": None,
                    "final_url": "",
                    "redirects": [],
                    "content_type": "",
                    "cache_control": "",
                    "etag": "",
                    "last_modified": "",
                    "bytes": 0,
                    "elapsed_ms": None,
                    "text": "",
                    "error": repr(exc),
                }
            row = classify(url, fetched)
            rows.append(row)
            completed += 1
            marker = "PASS" if row["pass"] else "FAIL"
            print(f"[{completed:03}/{len(urls):03}] {marker} {row['status']} {url}" + (f" :: {','.join(row['issues'])}" if row["issues"] else ""))

    rows.sort(key=lambda x: x["url"])

    status_counts: dict[str, int] = {}
    for row in rows:
        key = str(row["status"])
        status_counts[key] = status_counts.get(key, 0) + 1

    failed = [r for r in rows if not r["pass"]]
    redirects = [r for r in rows if r["redirect_count"]]
    soft404 = [r for r in rows if r["soft404_suspect"]]
    canonical_bad = [r for r in rows if "canonical_mismatch_or_missing" in r["issues"]]
    noindex = [r for r in rows if "noindex" in r["issues"]]

    finished = datetime.now(timezone.utc)
    summary = {
        "generated_at_utc": finished.isoformat(),
        "duration_seconds": round((finished - started).total_seconds(), 2),
        "base": BASE,
        "robots_url": ROBOTS,
        "sitemap_url": SITEMAP,
        "expected_sitemap_urls": EXPECTED_SITEMAP_COUNT,
        "actual_sitemap_urls": len(urls),
        "robots_status": robots_resp.get("status"),
        "sitemap_status": sitemap_resp.get("status"),
        "global_issues": global_issues,
        "url_count": len(rows),
        "pass_count": sum(1 for r in rows if r["pass"]),
        "fail_count": len(failed),
        "status_counts": status_counts,
        "redirect_count": len(redirects),
        "soft404_suspect_count": len(soft404),
        "canonical_issue_count": len(canonical_bad),
        "noindex_count": len(noindex),
        "overall_pass": not global_issues and not failed and len(rows) == EXPECTED_SITEMAP_COUNT,
    }

    payload = {"summary": summary, "rows": rows}
    (REPORT_DIR / "live-crawl-report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    fieldnames = [
        "url", "status", "final_url", "redirect_count", "content_type", "cache_control",
        "etag", "last_modified", "bytes", "elapsed_ms", "title", "canonical", "robots",
        "h1", "soft404_suspect", "pass", "issues", "error"
    ]
    with (REPORT_DIR / "live-crawl-report.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = {k: row.get(k, "") for k in fieldnames}
            out["issues"] = "|".join(row.get("issues", []))
            writer.writerow(out)

    md = [
        "# TadabburLife Live 103-URL Crawl QC",
        "",
        f"- Generated: {summary['generated_at_utc']}",
        f"- Sitemap: {summary['actual_sitemap_urls']} / {summary['expected_sitemap_urls']} URLs",
        f"- HTTP 200: {summary['status_counts'].get('200', 0)}",
        f"- PASS: {summary['pass_count']}",
        f"- FAIL: {summary['fail_count']}",
        f"- Redirected URLs: {summary['redirect_count']}",
        f"- Canonical issues: {summary['canonical_issue_count']}",
        f"- noindex: {summary['noindex_count']}",
        f"- Soft-404 suspects: {summary['soft404_suspect_count']}",
        f"- Global issues: {', '.join(summary['global_issues']) if summary['global_issues'] else 'none'}",
        f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}",
        "",
    ]
    if failed:
        md += ["## Failures", ""]
        for row in failed:
            md.append(f"- `{row['url']}` — {', '.join(row['issues']) or row['error']}")
        md.append("")
    (REPORT_DIR / "SUMMARY.md").write_text("\n".join(md), encoding="utf-8")

    print("\n=== SUMMARY ===")
    print(json.dumps(summary, indent=2))
    return 0 if summary["overall_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
