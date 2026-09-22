#!/usr/bin/env python3
"""Audit metadata + OG/share integrity across 94 TadabburLife landings.

Read-only audit. No landing files are modified.
"""

from __future__ import annotations
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

OUT=Path("qc-metadata-og-report")
OUT.mkdir(exist_ok=True)
PATHS=[
    Path(prefix)/f"{n:03d}"/"index.html"
    for prefix in ("tadabbur","en/tadabbur")
    for n in range(1,48)
]

def strip_tags(s:str)->str:
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",s))).strip()

def first(pattern:str,text:str)->str:
    m=re.search(pattern,text,re.I|re.S)
    return html.unescape(m.group(1).strip()) if m else ""

class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_lang=""
        self.title=""
        self._in_title=False
        self.meta={}
        self.links=[]
    def handle_starttag(self,tag,attrs):
        d={k.lower():(v or "") for k,v in attrs}
        t=tag.lower()
        if t=="html" and not self.html_lang:
            self.html_lang=d.get("lang","")
        elif t=="title":
            self._in_title=True
        elif t=="meta":
            key=d.get("property") or d.get("name")
            if key:
                self.meta[key.lower()]=d.get("content","")
        elif t=="link":
            self.links.append(d)
    def handle_endtag(self,tag):
        if tag.lower()=="title":
            self._in_title=False
    def handle_data(self,data):
        if self._in_title:
            self.title+=data

def parse(text:str)->MetaParser:
    p=MetaParser(); p.feed(text); p.title=strip_tags(p.title); return p

def canonical(p:MetaParser)->str:
    for d in p.links:
        rel={x.strip().lower() for x in d.get("rel","").split()}
        if "canonical" in rel:
            return d.get("href","")
    return ""

def h1(text:str)->str:
    return strip_tags(first(r"<h1\b[^>]*>(.*?)</h1>",text))

def session_head_paragraph(text:str)->str:
    m=re.search(r'<div\s+class=["\']session-head["\'][^>]*>(.*?)</div>',text,re.I|re.S)
    if not m:
        return ""
    return strip_tags(first(r"<p\b[^>]*>(.*?)</p>",m.group(1)))

def suspicious_truncation(desc:str,body_first_p:str)->bool:
    d=desc.strip()
    if not d:
        return False
    # Strong signals only: the description is an exact prefix of a longer source
    # paragraph and ends without sentence punctuation, or ends in a 1–3 char word.
    if body_first_p and body_first_p.startswith(d) and len(body_first_p)>len(d):
        if not re.search(r'[.!?…]["\')\]]?$',d):
            return True
    last=re.search(r"([A-Za-z]{1,3})$",d)
    if len(d)>=140 and last and not re.search(r'[.!?…]$',d):
        return True
    return False

def audit(path:Path)->dict[str,Any]:
    text=path.read_text(encoding="utf-8")
    p=parse(text)
    can=canonical(p)
    heading=h1(text)
    desc=p.meta.get("description","")
    is_en=str(path).startswith("en/")
    expected_lang="en" if is_en else "id"
    expected_locale="en_US" if is_en else "id_ID"
    first_p=session_head_paragraph(text)

    issues=[]
    required={
      "title":p.title,
      "h1":heading,
      "description":desc,
      "canonical":can,
      "og:type":p.meta.get("og:type",""),
      "og:site_name":p.meta.get("og:site_name",""),
      "og:locale":p.meta.get("og:locale",""),
      "og:title":p.meta.get("og:title",""),
      "og:description":p.meta.get("og:description",""),
      "og:url":p.meta.get("og:url",""),
      "twitter:card":p.meta.get("twitter:card",""),
      "twitter:title":p.meta.get("twitter:title",""),
      "twitter:description":p.meta.get("twitter:description",""),
    }
    for k,v in required.items():
        if not v:
            issues.append(f"missing_{k}")

    if p.html_lang!=expected_lang: issues.append("html_lang")
    if p.meta.get("og:type") and p.meta.get("og:type")!="article": issues.append("og_type")
    if p.meta.get("og:site_name") and p.meta.get("og:site_name")!="TadabburLife": issues.append("og_site_name")
    if p.meta.get("og:locale") and p.meta.get("og:locale")!=expected_locale: issues.append("og_locale")
    if p.meta.get("og:url") and p.meta.get("og:url")!=can: issues.append("og_url")
    if p.meta.get("og:title") and p.meta.get("og:title")!=heading: issues.append("og_title_h1")
    if p.meta.get("og:description") and p.meta.get("og:description")!=desc: issues.append("og_description_meta")
    if p.meta.get("twitter:card") and p.meta.get("twitter:card")!="summary": issues.append("twitter_card")
    if p.meta.get("twitter:title") and p.meta.get("twitter:title")!=heading: issues.append("twitter_title_h1")
    if p.meta.get("twitter:description") and p.meta.get("twitter:description")!=desc: issues.append("twitter_description_meta")

    trunc=suspicious_truncation(desc,first_p)
    if trunc: issues.append("suspicious_meta_truncation")

    return {
      "path":str(path),"pass":not issues,"issues":issues,
      "title":p.title,"h1":heading,"description":desc,"description_length":len(desc),
      "canonical":can,"html_lang":p.html_lang,
      "og_type":p.meta.get("og:type",""),"og_site_name":p.meta.get("og:site_name",""),
      "og_locale":p.meta.get("og:locale",""),"og_title":p.meta.get("og:title",""),
      "og_description":p.meta.get("og:description",""),"og_url":p.meta.get("og:url",""),
      "twitter_card":p.meta.get("twitter:card",""),"twitter_title":p.meta.get("twitter:title",""),
      "twitter_description":p.meta.get("twitter:description",""),
      "og_image":p.meta.get("og:image",""),
      "first_paragraph":first_p,
      "suspicious_truncation":trunc,
    }

def main()->int:
    rows=[audit(p) for p in PATHS]
    failures=[r for r in rows if not r["pass"]]
    issue_counts={}
    for r in rows:
        for i in r["issues"]:
            issue_counts[i]=issue_counts.get(i,0)+1
    summary={
      "files_checked":len(rows),
      "pass_count":sum(1 for r in rows if r["pass"]),
      "fail_count":len(failures),
      "issue_counts":issue_counts,
      "og_image_count":sum(1 for r in rows if r["og_image"]),
      "overall_pass":not failures and len(rows)==94,
    }
    (OUT/"metadata-og-audit.json").write_text(json.dumps({"summary":summary,"rows":rows},ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# TadabburLife Metadata + OG/Share Audit","",
      f"- Files checked: {summary['files_checked']} / 94",
      f"- PASS: {summary['pass_count']}",
      f"- FAIL: {summary['fail_count']}",
      f"- OG image present: {summary['og_image_count']} / 94",
      f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}","",
      "## Issue counts",""]
    for k,v in sorted(issue_counts.items(), key=lambda kv:(-kv[1],kv[0])):
        lines.append(f"- {k}: {v}")
    if failures:
        lines+=["","## Failures",""]
        for r in failures:
            lines.append(f"- `{r['path']}`: {', '.join(r['issues'])}")
    (OUT/"SUMMARY.md").write_text("\n".join(lines),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    for r in failures:
        print("FAIL",r["path"],r["issues"],"DESC_LEN",r["description_length"],"DESC",repr(r["description"][-90:]))
    return 0

if __name__=="__main__":
    sys.exit(main())
