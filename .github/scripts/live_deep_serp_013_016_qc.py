#!/usr/bin/env python3
from __future__ import annotations
import html, json, re, sys, time, urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE="https://tadabburlife.com"
OUT=Path("qc-live-deep-serp-013-016")
OUT.mkdir(exist_ok=True)
MAP=Path("seo/keyword-map.json")
UA="Mozilla/5.0 (compatible; TadabburLifeDeepSERPQC/1.0; +https://tadabburlife.com/)"

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title=""; self.in_title=False; self.meta={}; self.links=[]
    def handle_starttag(self,tag,attrs):
        d={k.lower():(v or "") for k,v in attrs}
        t=tag.lower()
        if t=="title": self.in_title=True
        elif t=="meta":
            key=(d.get("property") or d.get("name") or "").lower()
            if key:self.meta[key]=d.get("content","")
        elif t=="link": self.links.append(d)
    def handle_endtag(self,tag):
        if tag.lower()=="title": self.in_title=False
    def handle_data(self,data):
        if self.in_title:self.title+=data

def strip_tags(s):
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",s))).strip()

def fetch(url):
    last=""
    for a in range(3):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Cache-Control":"no-cache","Pragma":"no-cache"})
            with urllib.request.urlopen(req,timeout=20) as r:
                return r.status,r.geturl(),r.read().decode(r.headers.get_content_charset() or "utf-8",errors="replace"),""
        except Exception as e:
            last=repr(e); time.sleep(a+1)
    return None,"","",last

def canonical(p):
    for d in p.links:
        if "canonical" in {x.lower() for x in d.get("rel","").split()}:
            return d.get("href","")
    return ""

def article_schema(text):
    for raw in re.findall(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>',text,re.I|re.S):
        try:
            o=json.loads(raw)
            typ=o.get("@type") if isinstance(o,dict) else None
            if typ=="Article" or isinstance(typ,list) and "Article" in typ:return o
        except Exception:pass
    return {}

def main():
    data=json.loads(MAP.read_text(encoding="utf-8"))
    rows=[]
    for sid in ("013","014","015","016"):
        s=next(x for x in data["sessions"] if x["session"]==sid)
        for lang in ("id","en"):
            impl=s["implementation"][lang]
            url=impl["canonical"]
            status,final,text,error=fetch(url)
            p=Parser();p.feed(text);p.title=strip_tags(p.title)
            h1=strip_tags((re.search(r"<h1\b[^>]*>(.*?)</h1>",text,re.I|re.S) or [None,""])[1])
            can=canonical(p); desc=p.meta.get("description",""); a=article_schema(text)
            issues=[]
            if status!=200:issues.append(f"http_{status}")
            if final!=url:issues.append("final_url")
            if can!=url:issues.append("canonical")
            if p.title!=impl["seo_title"]:issues.append("title_map")
            if h1!=impl["h1"]:issues.append("h1_map")
            if desc!=impl["meta_description"]:issues.append("meta_map")
            if p.meta.get("og:title")!=h1:issues.append("og_title")
            if p.meta.get("og:description")!=desc:issues.append("og_description")
            if p.meta.get("og:url")!=url:issues.append("og_url")
            if a.get("headline")!=h1:issues.append("article_headline")
            if a.get("description")!=desc:issues.append("article_description")
            if text.count('data-seo-answer="deep-serp-2026-09-22"')!=1:issues.append("answer_block")
            ev=(s.get("seo",{}).get(lang,{}) or {}).get("demand_evidence","")
            if ev!="deep-live-serp-validated-2026-09-22":issues.append("evidence_status")
            if not (s.get("seo",{}).get(lang,{}) or {}).get("search_territory"):issues.append("search_territory")
            if not (s.get("seo",{}).get(lang,{}) or {}).get("cannibalization_guard"):issues.append("cannibalization_guard")
            rows.append({"session":sid,"lang":lang,"url":url,"status":status,"pass":not issues,"issues":issues,"error":error})
            print(("PASS" if not issues else "FAIL"),url,issues)
    fails=[x for x in rows if not x["pass"]]
    summary={"pages_checked":len(rows),"http_200":sum(x["status"]==200 for x in rows),"pass_count":sum(x["pass"] for x in rows),"fail_count":len(fails),"overall_pass":len(rows)==8 and not fails}
    (OUT/"report.json").write_text(json.dumps({"summary":summary,"rows":rows},indent=2),encoding="utf-8")
    lines=["# Live Deep SERP 013–016 QC","",f"- Pages checked: {summary['pages_checked']} / 8",f"- HTTP 200: {summary['http_200']} / 8",f"- PASS: {summary['pass_count']} / 8",f"- FAIL: {summary['fail_count']}",f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}",""]
    if fails:
        lines+=["## Failures",""]+[f"- {x['url']}: {', '.join(x['issues'])}" for x in fails]
    (OUT/"SUMMARY.md").write_text("\n".join(lines),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    return 0 if summary["overall_pass"] else 1

if __name__=="__main__":
    sys.exit(main())
