#!/usr/bin/env python3
"""Live QC for 94 Reflection Card OG images and their landing metadata."""

from __future__ import annotations
import html
import json
import re
import struct
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path

BASE="https://tadabburlife.com"
OUT=Path("qc-live-reflection-og-report")
OUT.mkdir(exist_ok=True)
WORKERS=12
TIMEOUT=20
ATTEMPTS=6
WAIT=15
UA="Mozilla/5.0 (compatible; TadabburLifeReflectionOGQC/1.0; +https://tadabburlife.com/)"

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta={}
    def handle_starttag(self,tag,attrs):
        if tag.lower()!="meta": return
        d={k.lower():(v or "") for k,v in attrs}
        key=(d.get("property") or d.get("name") or "").lower()
        if key:self.meta[key]=d.get("content","")

def fetch(url:str):
    last=""
    for a in range(3):
        try:
            req=urllib.request.Request(url,headers={
                "User-Agent":UA,
                "Accept":"*/*",
                "Cache-Control":"no-cache",
                "Pragma":"no-cache",
            })
            with urllib.request.urlopen(req,timeout=TIMEOUT) as r:
                raw=r.read()
                return r.status,r.geturl(),r.headers,raw,""
        except Exception as e:
            last=repr(e)
            if a<2:time.sleep(1+a)
    return None,"",{},b"",last

def png_size(raw:bytes):
    if len(raw)<24 or raw[:8]!=b"\x89PNG\r\n\x1a\n" or raw[12:16]!=b"IHDR":
        return None,None
    return struct.unpack(">II",raw[16:24])

def inspect(n:int,is_en:bool):
    sid=f"{n:03d}"
    lang="en" if is_en else "id"
    page=f"{BASE}/{'en/' if is_en else ''}tadabbur/{sid}/"
    expected_img=f"{BASE}/og/reflection/{lang}/{sid}.png"
    pstatus,pfinal,pheaders,praw,perror=fetch(page)
    issues=[]
    if pstatus!=200:issues.append(f"page_http_{pstatus}")
    if pfinal!=page:issues.append("page_final_url")
    text=praw.decode("utf-8",errors="replace")
    parser=P();parser.feed(text);m=parser.meta

    checks={
      "og_image":m.get("og:image")==expected_img,
      "og_secure":m.get("og:image:secure_url")==expected_img,
      "og_type":m.get("og:image:type")=="image/png",
      "og_width":m.get("og:image:width")=="1200",
      "og_height":m.get("og:image:height")=="630",
      "og_alt":bool(m.get("og:image:alt")),
      "twitter_card":m.get("twitter:card")=="summary_large_image",
      "twitter_image":m.get("twitter:image")==expected_img,
      "twitter_alt":bool(m.get("twitter:image:alt")),
    }
    issues += [k for k,v in checks.items() if not v]

    istatus,ifinal,iheaders,iraw,ierror=fetch(expected_img)
    if istatus!=200:issues.append(f"image_http_{istatus}")
    if ifinal!=expected_img:issues.append("image_final_url")
    ctype=str(iheaders.get("Content-Type","")).split(";")[0].strip().lower() if iheaders else ""
    if ctype!="image/png":issues.append(f"image_content_type_{ctype or 'missing'}")
    width,height=png_size(iraw)
    if (width,height)!=(1200,630):issues.append(f"image_dimensions_{width}x{height}")
    if len(iraw)<10000:issues.append("image_too_small")

    return {
      "session":sid,"language":lang,"page":page,"image":expected_img,
      "page_status":pstatus,"image_status":istatus,"content_type":ctype,
      "width":width,"height":height,"bytes":len(iraw),
      "pass":not issues,"issues":issues,
      "page_error":perror,"image_error":ierror
    }

def run_once():
    specs=[(n,e) for n in range(1,48) for e in (False,True)]
    rows=[]
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs={pool.submit(inspect,*s):s for s in specs}
        for fut in as_completed(futs):rows.append(fut.result())
    rows.sort(key=lambda x:(x["session"],x["language"]))
    fails=[r for r in rows if not r["pass"]]
    summary={
      "landing_count":len(rows),
      "page_http_200":sum(r["page_status"]==200 for r in rows),
      "image_http_200":sum(r["image_status"]==200 for r in rows),
      "png_1200x630":sum((r["width"],r["height"])==(1200,630) for r in rows),
      "unique_image_urls":len({r["image"] for r in rows}),
      "pass_count":sum(r["pass"] for r in rows),
      "fail_count":len(fails),
      "min_image_bytes":min((r["bytes"] for r in rows),default=0),
      "max_image_bytes":max((r["bytes"] for r in rows),default=0),
      "overall_pass":len(rows)==94 and not fails and len({r["image"] for r in rows})==94,
    }
    return summary,rows,fails

def main():
    final=None
    for attempt in range(1,ATTEMPTS+1):
        summary,rows,fails=run_once()
        print(f"Attempt {attempt}/{ATTEMPTS}: {json.dumps(summary)}")
        final=(summary,rows,fails)
        if summary["overall_pass"]:break
        if attempt<ATTEMPTS:
            print(f"Waiting {WAIT}s for Pages/cache propagation...")
            time.sleep(WAIT)
    summary,rows,fails=final
    (OUT/"live-reflection-og-report.json").write_text(
      json.dumps({"summary":summary,"rows":rows},ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# TadabburLife Live Reflection Card OG QC","",
      f"- Landing metadata checked: {summary['landing_count']} / 94",
      f"- Landing HTTP 200: {summary['page_http_200']} / 94",
      f"- Image HTTP 200: {summary['image_http_200']} / 94",
      f"- PNG 1200×630: {summary['png_1200x630']} / 94",
      f"- Unique image URLs: {summary['unique_image_urls']} / 94",
      f"- PASS: {summary['pass_count']} / 94",
      f"- FAIL: {summary['fail_count']}",
      f"- Image bytes: {summary['min_image_bytes']}–{summary['max_image_bytes']}",
      f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}",""]
    if fails:
        lines+=["## Failures",""]+[f"- `{r['page']}`: {', '.join(r['issues'])}" for r in fails]
    (OUT/"SUMMARY.md").write_text("\n".join(lines),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    return 0 if summary["overall_pass"] else 1

if __name__=="__main__":
    sys.exit(main())
