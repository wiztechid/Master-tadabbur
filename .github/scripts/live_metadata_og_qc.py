#!/usr/bin/env python3
"""Live metadata + OG/share integrity QC for 94 TadabburLife session landings."""

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

BASE="https://tadabburlife.com"
MAP=Path("seo/keyword-map.json")
OUT=Path("qc-live-metadata-og-report")
OUT.mkdir(exist_ok=True)
WORKERS=12
TIMEOUT=20
ATTEMPTS=6
WAIT=15
UA="Mozilla/5.0 (compatible; TadabburLifeMetadataShareQC/1.0; +https://tadabburlife.com/)"

JSONLD_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>',re.I|re.S)

def strip_tags(s:str)->str:
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",s))).strip()

def first(pattern:str,text:str)->str:
    m=re.search(pattern,text,re.I|re.S)
    return html.unescape(m.group(1).strip()) if m else ""

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_lang=""
        self.title=""
        self._title=False
        self.meta={}
        self.links=[]
    def handle_starttag(self,tag,attrs):
        d={k.lower():(v or "") for k,v in attrs}
        t=tag.lower()
        if t=="html" and not self.html_lang:
            self.html_lang=d.get("lang","")
        elif t=="title":
            self._title=True
        elif t=="meta":
            key=(d.get("property") or d.get("name") or "").lower()
            if key:self.meta[key]=d.get("content","")
        elif t=="link":
            self.links.append(d)
    def handle_endtag(self,tag):
        if tag.lower()=="title":self._title=False
    def handle_data(self,data):
        if self._title:self.title+=data

def parse(text:str)->Parser:
    p=Parser();p.feed(text);p.title=strip_tags(p.title);return p

def canonical(p:Parser)->str:
    for d in p.links:
        rel={x.strip().lower() for x in d.get("rel","").split()}
        if "canonical" in rel:return d.get("href","")
    return ""

def h1(text:str)->str:
    return strip_tags(first(r"<h1\b[^>]*>(.*?)</h1>",text))

def fetch(url:str):
    last=""
    for a in range(3):
        try:
            req=urllib.request.Request(url,headers={
                "User-Agent":UA,
                "Accept":"text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
                "Cache-Control":"no-cache",
                "Pragma":"no-cache",
            })
            with urllib.request.urlopen(req,timeout=TIMEOUT) as r:
                return r.status,r.geturl(),r.read().decode(r.headers.get_content_charset() or "utf-8",errors="replace"),""
        except Exception as e:
            last=repr(e)
            if a<2:time.sleep(1+a)
    return None,"","",last

def article_schema(text:str)->tuple[int,dict[str,Any]|None,int]:
    articles=[];errors=0
    for raw in JSONLD_RE.findall(text):
        try:
            obj=json.loads(raw)
            typ=obj.get("@type") if isinstance(obj,dict) else None
            types={typ} if isinstance(typ,str) else set(typ or []) if isinstance(typ,list) else set()
            if "Article" in types:articles.append(obj)
        except Exception:errors+=1
    return len(articles),(articles[0] if len(articles)==1 else None),errors

def inspect(session:dict[str,Any],lang:str)->dict[str,Any]:
    sid=session["session"]
    url=f"{BASE}/{'en/' if lang=='en' else ''}tadabbur/{sid}/"
    status,final,text,error=fetch(url)
    p=parse(text);can=canonical(p);heading=h1(text);desc=p.meta.get("description","")
    expected=(session.get("implementation",{}) or {}).get(lang,{})
    expected_locale="en_US" if lang=="en" else "id_ID"
    expected_html_lang="en" if lang=="en" else "id"
    issues=[]
    if status!=200:issues.append(f"http_{status}")
    if final!=url:issues.append("final_url")
    if can!=url:issues.append("canonical")
    if p.html_lang!=expected_html_lang:issues.append("html_lang")
    if p.title!=expected.get("seo_title",""):issues.append("title_map")
    if heading!=expected.get("h1",""):issues.append("h1_map")
    if desc!=expected.get("meta_description",""):issues.append("description_map")
    checks={
        "og_type":p.meta.get("og:type")=="article",
        "og_site_name":p.meta.get("og:site_name")=="TadabburLife",
        "og_locale":p.meta.get("og:locale")==expected_locale,
        "og_title":p.meta.get("og:title")==heading,
        "og_description":p.meta.get("og:description")==desc,
        "og_url":p.meta.get("og:url")==can,
        "og_image":p.meta.get("og:image")==f"https://tadabburlife.com/og/reflection/{'en' if lang=='en' else 'id'}/{sid}.png",
        "og_image_secure":p.meta.get("og:image:secure_url")==p.meta.get("og:image"),
        "og_image_type":p.meta.get("og:image:type")=="image/png",
        "og_image_width":p.meta.get("og:image:width")=="1200",
        "og_image_height":p.meta.get("og:image:height")=="630",
        "og_image_alt":bool(p.meta.get("og:image:alt")),
        "twitter_card":p.meta.get("twitter:card")=="summary_large_image",
        "twitter_title":p.meta.get("twitter:title")==heading,
        "twitter_description":p.meta.get("twitter:description")==desc,
        "twitter_image":p.meta.get("twitter:image")==p.meta.get("og:image"),
        "twitter_image_alt":bool(p.meta.get("twitter:image:alt")),
        "description_nonempty":bool(desc),
        "description_not_thin":len(desc)>=70,
    }
    issues += [k for k,v in checks.items() if not v]
    count,article,parse_errors=article_schema(text)
    if parse_errors:issues.append("jsonld_parse_error")
    if count!=1:issues.append(f"article_count_{count}")
    elif article.get("headline")!=heading or article.get("description")!=desc:
        issues.append("article_metadata_drift")
    return {
        "session":sid,"language":lang,"url":url,"status":status,"pass":not issues,
        "issues":issues,"description_length":len(desc),"og_image":p.meta.get("og:image",""),
        "error":error
    }

def run_once(data):
    specs=[(s,l) for s in data["sessions"] for l in ("id","en")]
    rows=[]
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs={pool.submit(inspect,s,l):(s["session"],l) for s,l in specs}
        for fut in as_completed(futs):rows.append(fut.result())
    rows.sort(key=lambda x:(x["session"],x["language"]))
    fails=[r for r in rows if not r["pass"]]
    summary={
      "live_checked":len(rows),
      "http_200_count":sum(1 for r in rows if r["status"]==200),
      "pass_count":sum(1 for r in rows if r["pass"]),
      "fail_count":len(fails),
      "og_image_count":sum(1 for r in rows if r["og_image"]),
      "overall_pass":len(rows)==94 and not fails
    }
    return summary,rows,fails

def main():
    data=json.loads(MAP.read_text(encoding="utf-8"))
    final=None
    for attempt in range(1,ATTEMPTS+1):
        summary,rows,fails=run_once(data)
        print(f"Attempt {attempt}/{ATTEMPTS}: {json.dumps(summary)}")
        final=(summary,rows,fails)
        if summary["overall_pass"]:break
        if attempt<ATTEMPTS:
            print(f"Waiting {WAIT}s for Pages/cache propagation...")
            time.sleep(WAIT)
    summary,rows,fails=final
    (OUT/"live-metadata-og-report.json").write_text(json.dumps({"summary":summary,"rows":rows},ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# TadabburLife Live Metadata + OG/Share QC","",
      f"- Live URLs checked: {summary['live_checked']} / 94",
      f"- HTTP 200: {summary['http_200_count']} / 94",
      f"- Metadata/OG/share PASS: {summary['pass_count']} / 94",
      f"- FAIL: {summary['fail_count']}",
      f"- OG image present: {summary['og_image_count']} / 94 (not a blocker for text-summary cards)",
      f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}",""]
    if fails:
        lines+=["## Failures",""]+[f"- `{r['url']}`: {', '.join(r['issues'])}" for r in fails]
    (OUT/"SUMMARY.md").write_text("\n".join(lines),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    return 0 if summary["overall_pass"] else 1

if __name__=="__main__":
    sys.exit(main())
