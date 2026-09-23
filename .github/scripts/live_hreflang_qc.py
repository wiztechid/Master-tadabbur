#!/usr/bin/env python3
"""Live canonical/hreflang reciprocity QC for 94 TadabburLife session landings."""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://tadabburlife.com"
SITEMAP = BASE + "/sitemap.xml"
OUT = Path("qc-live-hreflang-report")
OUT.mkdir(exist_ok=True)
WORKERS = 12
TIMEOUT = 20
ATTEMPTS = 6
WAIT = 15
UA = "Mozilla/5.0 (compatible; TadabburLifeHreflangQC/1.0; +https://tadabburlife.com/)"

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_lang = ""
        self.canonical = ""
        self.alternates = {}
        self.robots = ""
    def handle_starttag(self, tag, attrs):
        d = {k.lower():(v or "") for k,v in attrs}
        t = tag.lower()
        if t == "html" and not self.html_lang:
            self.html_lang = d.get("lang","")
        elif t == "link":
            rel = {x.strip().lower() for x in d.get("rel","").split()}
            if "canonical" in rel and not self.canonical:
                self.canonical = d.get("href","")
            if "alternate" in rel and d.get("hreflang"):
                self.alternates[d.get("hreflang","").lower()] = d.get("href","")
        elif t == "meta" and d.get("name","").lower() == "robots":
            self.robots = d.get("content","")

def fetch(url):
    last = ""
    for a in range(3):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            })
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                raw = r.read()
                charset = r.headers.get_content_charset() or "utf-8"
                return r.status, r.geturl(), raw.decode(charset, errors="replace"), ""
        except Exception as exc:
            last = repr(exc)
            if a < 2:
                time.sleep(1+a)
    return None, "", "", last

def expected(n, lang):
    sid = f"{n:03d}"
    id_url = f"{BASE}/tadabbur/{sid}/"
    en_url = f"{BASE}/en/tadabbur/{sid}/"
    return {
        "self": en_url if lang == "en" else id_url,
        "html_lang": lang,
        "alternates": {"id": id_url, "en": en_url, "x-default": id_url},
    }

def inspect(n, lang, sitemap_urls):
    exp = expected(n, lang)
    status, final, text, error = fetch(exp["self"])
    p = P(); p.feed(text)
    issues = []
    if status != 200: issues.append(f"http_{status}")
    if final != exp["self"]: issues.append("final_url")
    if p.html_lang != exp["html_lang"]: issues.append("html_lang")
    if p.canonical != exp["self"]: issues.append("canonical")
    if "noindex" in p.robots.lower(): issues.append("noindex")
    for key, url in exp["alternates"].items():
        if p.alternates.get(key) != url:
            issues.append(f"hreflang_{key}")
    extra = sorted(set(p.alternates) - {"id","en","x-default"})
    if extra:
        issues.append("unexpected_hreflang:" + ",".join(extra))
    if exp["self"] not in sitemap_urls:
        issues.append("missing_from_sitemap")
    return {
        "session": f"{n:03d}",
        "language": lang,
        "url": exp["self"],
        "status": status,
        "canonical": p.canonical,
        "alternates": p.alternates,
        "pass": not issues,
        "issues": issues,
        "error": error,
    }

def run_once():
    sm_status, sm_final, sm_text, sm_error = fetch(SITEMAP)
    global_issues = []
    sitemap_urls = set()
    if sm_status != 200:
        global_issues.append(f"sitemap_http_{sm_status}")
    elif sm_final != SITEMAP:
        global_issues.append("sitemap_final_url")
    else:
        try:
            root = ET.fromstring(sm_text)
            sitemap_urls = {(x.text or "").strip() for x in root.findall(".//{*}loc") if (x.text or "").strip()}
        except Exception as exc:
            global_issues.append(f"sitemap_parse:{exc!r}")
    expected_session_urls = {
        expected(n, lang)["self"]
        for n in range(1,48)
        for lang in ("id","en")
    }
    if len(sitemap_urls) != 103:
        global_issues.append(f"sitemap_count_{len(sitemap_urls)}")
    missing_session_urls = sorted(expected_session_urls - sitemap_urls)
    if missing_session_urls:
        global_issues.append(f"missing_session_urls_{len(missing_session_urls)}")

    rows = []
    specs = [(n,lang) for n in range(1,48) for lang in ("id","en")]
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(inspect,n,lang,sitemap_urls):(n,lang) for n,lang in specs}
        for fut in as_completed(futs):
            rows.append(fut.result())
    rows.sort(key=lambda x:(x["session"],x["language"]))

    pair_issues = []
    for n in range(1,48):
        sid=f"{n:03d}"
        idr=next(x for x in rows if x["session"]==sid and x["language"]=="id")
        enr=next(x for x in rows if x["session"]==sid and x["language"]=="en")
        exp_id=expected(n,"id")["alternates"]
        exp_en=expected(n,"en")["alternates"]
        if idr["alternates"] != exp_id or enr["alternates"] != exp_en:
            pair_issues.append(sid)

    fails=[r for r in rows if not r["pass"]]
    summary={
        "sitemap_status":sm_status,
        "sitemap_urls":len(sitemap_urls),
        "landings_checked":len(rows),
        "http_200":sum(r["status"]==200 for r in rows),
        "canonical_pass":sum(r["canonical"]==r["url"] for r in rows),
        "hreflang_pass":sum(
            r["alternates"]==expected(int(r["session"]),r["language"])["alternates"]
            for r in rows
        ),
        "reciprocal_pairs_pass":47-len(pair_issues),
        "fail_count":len(fails),
        "global_issues":global_issues,
        "pair_issues":pair_issues,
        "overall_pass":len(rows)==94 and not fails and not global_issues and not pair_issues,
    }
    return summary,rows,fails

def main():
    final=None
    for attempt in range(1,ATTEMPTS+1):
        summary,rows,fails=run_once()
        print(f"Attempt {attempt}/{ATTEMPTS}: {json.dumps(summary)}")
        final=(summary,rows,fails,attempt)
        if summary["overall_pass"]:
            break
        if attempt<ATTEMPTS:
            time.sleep(WAIT)
    summary,rows,fails,attempt=final
    payload={"summary":summary,"attempts":attempt,"rows":rows}
    (OUT/"live-hreflang-report.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=[
        "# TadabburLife Live Canonical + Hreflang QC","",
        f"- Attempts: {attempt}",
        f"- Sitemap: {summary['sitemap_urls']} / 103",
        f"- Landings checked: {summary['landings_checked']} / 94",
        f"- HTTP 200: {summary['http_200']} / 94",
        f"- Canonical PASS: {summary['canonical_pass']} / 94",
        f"- Hreflang ID/EN/x-default PASS: {summary['hreflang_pass']} / 94",
        f"- Reciprocal pairs PASS: {summary['reciprocal_pairs_pass']} / 47",
        f"- FAIL: {summary['fail_count']}",
        f"- Global issues: {', '.join(summary['global_issues']) if summary['global_issues'] else 'none'}",
        f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}",""
    ]
    if fails:
        lines+=["## Failures",""]+[f"- {r['url']}: {', '.join(r['issues'])}" for r in fails]
    (OUT/"SUMMARY.md").write_text("\n".join(lines),encoding="utf-8")
    return 0 if summary["overall_pass"] else 1

if __name__=="__main__":
    sys.exit(main())
