#!/usr/bin/env python3
from __future__ import annotations
import html, json, re, sys, time, urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE="https://tadabburlife.com"
OUT=Path(".github/qc-state/post-dedup-serp")
OUT.mkdir(parents=True,exist_ok=True)
MAP=Path("seo/keyword-map.json")
UA="Mozilla/5.0 (compatible; TadabburLifePostDedupSERPQC/1.0; +https://tadabburlife.com/)"
SESSIONS=("004","007","011","016","043","044")
EVIDENCE="deep-live-serp-revalidated-2026-09-23"
ANSWER='data-seo-answer="post-dedup-live-serp-2026-09-23"'

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title=""; self.in_title=False; self.meta={}; self.links=[]
    def handle_starttag(self,tag,attrs):
        d={k.lower():(v or "") for k,v in attrs}; t=tag.lower()
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
            o=json.loads(raw); typ=o.get("@type") if isinstance(o,dict) else None
            if typ=="Article" or isinstance(typ,list) and "Article" in typ:return o
        except Exception: pass
    return {}

def main():
    data=json.loads(MAP.read_text(encoding="utf-8"))
    by={x["session"]:x for x in data["sessions"]}
    expected_first=by["004"]["implementation"]["id"]["seo_title"]
    propagated=False; attempts=0
    for i in range(1,13):
        attempts=i
        status,_,text,_=fetch(BASE+"/tadabbur/004/?qc="+str(int(time.time())))
        p=Parser(); p.feed(text); p.title=strip_tags(p.title)
        if status==200 and p.title==expected_first:
            propagated=True; break
        if i<12: time.sleep(20)

    rows=[]
    for sid in SESSIONS:
        s=by[sid]
        for lang in ("id","en"):
            impl=s["implementation"][lang]
            url=impl["canonical"]
            status,final,text,error=fetch(url+"?qc="+str(int(time.time())))
            clean_url=url
            p=Parser(); p.feed(text); p.title=strip_tags(p.title)
            h1=strip_tags((re.search(r"<h1\b[^>]*>(.*?)</h1>",text,re.I|re.S) or [None,""])[1])
            can=canonical(p); desc=p.meta.get("description",""); a=article_schema(text)
            issues=[]
            if status!=200:issues.append(f"http_{status}")
            if final.split("?")[0]!=clean_url:issues.append("final_url")
            if can!=clean_url:issues.append("canonical")
            if p.title!=impl["seo_title"]:issues.append("title_map")
            if h1!=impl["h1"]:issues.append("h1_map")
            if desc!=impl["meta_description"]:issues.append("meta_map")
            if p.meta.get("og:title")!=h1:issues.append("og_title")
            if p.meta.get("og:description")!=desc:issues.append("og_description")
            if p.meta.get("og:url")!=clean_url:issues.append("og_url")
            if a.get("headline")!=h1:issues.append("article_headline")
            if a.get("description")!=desc:issues.append("article_description")
            if text.count(ANSWER)!=1:issues.append("answer_block")
            seo=(s.get("seo",{}).get(lang,{}) or {})
            if seo.get("demand_evidence")!=EVIDENCE:issues.append("evidence_status")
            if not seo.get("search_territory"):issues.append("search_territory")
            if not seo.get("cannibalization_guard"):issues.append("cannibalization_guard")
            rows.append({"session":sid,"lang":lang,"url":clean_url,"status":status,"pass":not issues,"issues":issues,"error":error})
            print(("PASS" if not issues else "FAIL"),clean_url,issues)

    owner_pairs={"004":"023","007":"031","011":"042","016":"030","043":"027","044":"010"}
    owner_issues=[]
    for sid,owner in owner_pairs.items():
        for lang in ("id","en"):
            guard=(by[owner].get("seo",{}).get(lang,{}) or {}).get("cannibalization_guard","")
            if sid not in guard and str(int(sid)) not in guard:
                owner_issues.append(f"owner_guard_{owner}_{lang}_missing_session_{sid}")

    fails=[x for x in rows if not x["pass"]]
    summary={
        "generated_at":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
        "propagated":propagated,
        "propagation_attempts":attempts,
        "pages_checked":len(rows),
        "http_200":sum(x["status"]==200 for x in rows),
        "pass_count":sum(x["pass"] for x in rows),
        "fail_count":len(fails),
        "owner_guard_issues":owner_issues,
        "overall_pass":propagated and len(rows)==12 and not fails and not owner_issues,
    }
    payload={"summary":summary,"rows":rows}
    (OUT/"latest.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    md=["# Post-Dedup Deep Live SERP QC","",
        f"- Generated: {summary['generated_at']}",
        f"- Propagation: {'PASS' if propagated else 'FAIL'} after {attempts} attempt(s)",
        f"- Pages checked: {summary['pages_checked']} / 12",
        f"- HTTP 200: {summary['http_200']} / 12",
        f"- PASS: {summary['pass_count']} / 12",
        f"- FAIL: {summary['fail_count']}",
        f"- Owner guard issues: {len(owner_issues)}",
        f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}",""]
    if fails:
        md+=["## Failures",""]+[f"- {x['url']}: {', '.join(x['issues'])}" for x in fails]+[""]
    if owner_issues:
        md+=["## Owner guard issues",""]+[f"- {x}" for x in owner_issues]+[""]
    (OUT/"SUMMARY.md").write_text("\n".join(md),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    return 0 if summary["overall_pass"] else 1

if __name__=="__main__":
    sys.exit(main())
