#!/usr/bin/env python3
"""Verify normalized TadabburLife schema on all 94 live session landings."""

from __future__ import annotations
import html
import json
import re
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE="https://tadabburlife.com"
TIMEOUT=20
WORKERS=12
USER_AGENT="Mozilla/5.0 (compatible; TadabburLifeSchemaQC/1.0; +https://tadabburlife.com/)"
OUT=Path("qc-live-schema-report")
OUT.mkdir(exist_ok=True)

URLS=[
    f"{BASE}/tadabbur/{n:03d}/" for n in range(1,48)
]+[
    f"{BASE}/en/tadabbur/{n:03d}/" for n in range(1,48)
]

JSONLD_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>',re.I|re.S)

def first(pattern,text):
    m=re.search(pattern,text,re.I|re.S)
    return html.unescape(m.group(1).strip()) if m else ""

def strip_tags(s):
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",s))).strip()

def fetch(url):
    last=""
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={
                "User-Agent":USER_AGENT,
                "Accept":"text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
                "Cache-Control":"no-cache",
                "Pragma":"no-cache",
            })
            with urllib.request.urlopen(req,timeout=TIMEOUT) as r:
                return r.status,r.geturl(),r.read().decode(r.headers.get_content_charset() or "utf-8",errors="replace"),""
        except Exception as e:
            last=repr(e)
            if attempt<2: time.sleep(1+attempt)
    return None,"","",last

def types(obj):
    if not isinstance(obj,dict): return set()
    t=obj.get("@type")
    if isinstance(t,str): return {t}
    if isinstance(t,list): return set(map(str,t))
    return set()

def inspect(url):
    status,final,text,error=fetch(url)
    issues=[]
    if status!=200: issues.append(f"http_{status}")
    if final!=url: issues.append("final_url_mismatch")

    can=first(r'<link\b[^>]*\brel=["\']canonical["\'][^>]*\bhref=["\']([^"\']+)',text) or first(r'<link\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*\brel=["\']canonical["\']',text)
    desc=first(r'<meta\b[^>]*\bname=["\']description["\'][^>]*\bcontent=["\']([^"\']*)',text) or first(r'<meta\b[^>]*\bcontent=["\']([^"\']*)["\'][^>]*\bname=["\']description["\']',text)
    h1=strip_tags(first(r"<h1\b[^>]*>(.*?)</h1>",text))
    lang="en" if "/en/tadabbur/" in url else "id-ID"

    parsed=[]
    parse_errors=0
    for raw in JSONLD_RE.findall(text):
        try: parsed.append(json.loads(raw))
        except Exception: parse_errors+=1
    if parse_errors: issues.append("jsonld_parse_error")

    articles=[x for x in parsed if isinstance(x,dict) and "Article" in types(x)]
    crumbs=[x for x in parsed if isinstance(x,dict) and "BreadcrumbList" in types(x)]
    if len(articles)!=1: issues.append(f"article_count_{len(articles)}")
    if len(crumbs)!=1: issues.append(f"breadcrumb_count_{len(crumbs)}")

    if len(articles)==1:
        a=articles[0]
        checks={
            "headline":a.get("headline")==h1,
            "description":a.get("description")==desc,
            "inLanguage":a.get("inLanguage")==lang,
            "url":a.get("url")==can==url,
            "mainEntityOfPage":isinstance(a.get("mainEntityOfPage"),dict) and a["mainEntityOfPage"].get("@type")=="WebPage" and a["mainEntityOfPage"].get("@id")==url,
            "author":isinstance(a.get("author"),dict) and a["author"].get("@type")=="Person" and a["author"].get("name")=="Suiza Ixan Saputro",
            "publisher":isinstance(a.get("publisher"),dict) and a["publisher"].get("@type")=="Organization" and a["publisher"].get("name")=="TadabburLife" and a["publisher"].get("url")==f"{BASE}/",
            "isPartOf":isinstance(a.get("isPartOf"),dict) and a["isPartOf"].get("@type")=="WebSite" and a["isPartOf"].get("name")=="TadabburLife" and a["isPartOf"].get("url")==f"{BASE}/",
        }
        issues += [f"article_{k}" for k,v in checks.items() if not v]

    if len(crumbs)==1:
        items=crumbs[0].get("itemListElement")
        if not isinstance(items,list) or len(items)!=2:
            issues.append("breadcrumb_items")
        else:
            b1,b2=items
            if not (isinstance(b1,dict) and b1.get("position")==1 and b1.get("name")=="TadabburLife" and b1.get("item")==f"{BASE}/"):
                issues.append("breadcrumb_home")
            if not (isinstance(b2,dict) and b2.get("position")==2 and b2.get("name")==h1 and b2.get("item")==url):
                issues.append("breadcrumb_current")

    return {"url":url,"status":status,"final_url":final,"canonical":can,"h1":h1,"pass":not issues,"issues":issues,"error":error}

def main():
    rows=[]
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs={pool.submit(inspect,u):u for u in URLS}
        for i,f in enumerate(as_completed(futs),1):
            row=f.result()
            rows.append(row)
            print(f"[{i:02d}/94] {'PASS' if row['pass'] else 'FAIL'} {row['url']}"+(f" :: {','.join(row['issues'])}" if row['issues'] else ""))
    rows.sort(key=lambda x:x["url"])
    failed=[r for r in rows if not r["pass"]]
    summary={
        "urls_expected":94,
        "urls_checked":len(rows),
        "http_200_count":sum(1 for r in rows if r["status"]==200),
        "pass_count":sum(1 for r in rows if r["pass"]),
        "fail_count":len(failed),
        "overall_pass":len(rows)==94 and not failed,
    }
    (OUT/"live-schema-report.json").write_text(json.dumps({"summary":summary,"rows":rows},ensure_ascii=False,indent=2),encoding="utf-8")
    lines=[
        "# TadabburLife Live Schema QC","",
        f"- URLs checked: {summary['urls_checked']} / 94",
        f"- HTTP 200: {summary['http_200_count']} / 94",
        f"- Schema PASS: {summary['pass_count']} / 94",
        f"- FAIL: {summary['fail_count']}",
        f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}",""
    ]
    if failed:
        lines += ["## Failures",""]+[f"- `{r['url']}`: {', '.join(r['issues'])}" for r in failed]
    (OUT/"SUMMARY.md").write_text("\n".join(lines),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    return 0 if summary["overall_pass"] else 1

if __name__=="__main__":
    sys.exit(main())
