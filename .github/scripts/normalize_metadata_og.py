#!/usr/bin/env python3
"""Normalize metadata + OG/share integrity across 94 TadabburLife landings.

Safety:
- Only <head> is modified.
- <body> must remain byte-for-byte unchanged.
- No keyword research/evidence fields are changed here.
- Broken/thin descriptions are repaired only from text already present on the same page.
"""

from __future__ import annotations
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

REPORT_DIR=Path("qc-metadata-normalization-report")
REPORT_DIR.mkdir(exist_ok=True)
PATHS=[
    Path(prefix)/f"{n:03d}"/"index.html"
    for prefix in ("tadabbur","en/tadabbur")
    for n in range(1,48)
]

META_TAG_RE=re.compile(r"<meta\b[^>]*>",re.I)
JSONLD_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>',re.I|re.S)

TARGET_META_KEYS={
    "description",
    "og:type","og:site_name","og:locale","og:title","og:description","og:url",
    "og:image","og:image:secure_url","og:image:type","og:image:width","og:image:height","og:image:alt",
    "twitter:card","twitter:title","twitter:description","twitter:image","twitter:image:alt"
}

def strip_tags(s:str)->str:
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",s))).strip()

def first(pattern:str,text:str)->str:
    m=re.search(pattern,text,re.I|re.S)
    return html.unescape(m.group(1).strip()) if m else ""

class SignalParser(HTMLParser):
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
            if key:
                self.meta[key]=d.get("content","")
        elif t=="link":
            self.links.append(d)
    def handle_endtag(self,tag):
        if tag.lower()=="title":
            self._title=False
    def handle_data(self,data):
        if self._title:
            self.title+=data

def parse(text:str)->SignalParser:
    p=SignalParser(); p.feed(text); p.title=strip_tags(p.title); return p

def canonical(p:SignalParser)->str:
    for d in p.links:
        rel={x.strip().lower() for x in d.get("rel","").split()}
        if "canonical" in rel:
            return d.get("href","")
    return ""

def h1(text:str)->str:
    return strip_tags(first(r"<h1\b[^>]*>(.*?)</h1>",text))

def body_part(text:str)->str:
    i=text.lower().find("<body")
    return text[i:] if i>=0 else ""

def session_head(text:str)->tuple[str,str]:
    m=re.search(r'<div\s+class=["\']session-head["\'][^>]*>(.*?)</div>',text,re.I|re.S)
    if not m:
        return "",""
    block=m.group(1)
    return strip_tags(first(r"<h2\b[^>]*>(.*?)</h2>",block)), strip_tags(first(r"<p\b[^>]*>(.*?)</p>",block))

def article_paragraphs(text:str)->list[str]:
    m=re.search(r"<article\b[^>]*>(.*?)</article>",text,re.I|re.S)
    if not m:
        return []
    out=[]
    for raw in re.findall(r"<p\b[^>]*>(.*?)</p>",m.group(1),re.I|re.S):
        val=strip_tags(raw)
        if val:
            out.append(val)
    return out

def suspicious_truncation(desc:str,first_p:str)->bool:
    d=desc.strip()
    if not d: return False
    if first_p and first_p.startswith(d) and len(first_p)>len(d) and not re.search(r'[.!?…]["\')\]]?$',d):
        return True
    last=re.search(r"([A-Za-z]{1,3})$",d)
    return bool(len(d)>=140 and last and not re.search(r'[.!?…]$',d))

def complete_excerpt(text:str,max_soft:int=180)->str:
    text=strip_tags(text)
    if not text:
        return ""
    sentences=re.split(r'(?<=[.!?…])\s+',text)
    chosen=[]
    total=0
    for s in sentences:
        s=s.strip()
        if not s: continue
        proposed=(" ".join(chosen+[s])).strip()
        if chosen and len(proposed)>max_soft:
            break
        chosen.append(s)
        total=len(proposed)
        if total>=95:
            break
    if chosen:
        out=" ".join(chosen).strip()
    else:
        out=text
    if out and not re.search(r'[.!?…]$',out):
        out += "."
    return out

def repair_description(text:str,old:str)->tuple[str,bool,str]:
    h2_text,first_p=session_head(text)
    broken=suspicious_truncation(old,first_p)
    thin=len(old.strip())<70
    if not (broken or thin):
        return old,False,""

    source=first_p
    if len(source)<80:
        for p in article_paragraphs(text):
            if len(p)>=80 and p!=first_p and "translation:" not in p.lower():
                source=p
                break

    excerpt=complete_excerpt(source)
    parts=[]
    if h2_text:
        parts.append(h2_text.rstrip(".!?…"))
    if excerpt:
        parts.append(excerpt)
    new=". ".join(parts).replace(".. ",". ").strip()
    if new and not re.search(r'[.!?…]$',new):
        new += "."
    if not new:
        return old,False,""
    return new, new!=old, ("truncated" if broken else "thin")

def meta_key(tag:str)->str:
    class One(HTMLParser):
        def __init__(self):
            super().__init__(); self.attrs={}
        def handle_starttag(self,t,attrs):
            if t.lower()=="meta":
                self.attrs={k.lower():(v or "") for k,v in attrs}
    p=One(); p.feed(tag)
    return (p.attrs.get("property") or p.attrs.get("name") or "").lower()

def esc(s:str)->str:
    return html.escape(s,quote=True)

def standard_meta(desc:str,heading:str,can:str,locale:str)->str:
    m=re.search(r"/tadabbur/(\d{3})/$",can)
    if not m:
        raise RuntimeError(f"Cannot derive OG image from canonical: {can}")
    sid=m.group(1)
    lang="en" if "/en/tadabbur/" in can else "id"
    image=f"https://tadabburlife.com/og/reflection/{lang}/{sid}.png"
    alt=f"{heading} — TadabburLife Reflection Card"
    return "".join([
        f'<meta name="description" content="{esc(desc)}">',
        '<meta property="og:type" content="article">',
        '<meta property="og:site_name" content="TadabburLife">',
        f'<meta property="og:locale" content="{locale}">',
        f'<meta property="og:title" content="{esc(heading)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{esc(can)}">',
        f'<meta property="og:image" content="{esc(image)}">',
        f'<meta property="og:image:secure_url" content="{esc(image)}">',
        '<meta property="og:image:type" content="image/png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{esc(alt)}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(heading)}">',
        f'<meta name="twitter:description" content="{esc(desc)}">',
        f'<meta name="twitter:image" content="{esc(image)}">',
        f'<meta name="twitter:image:alt" content="{esc(alt)}">',
    ])

def update_article_schema(text:str,heading:str,desc:str,can:str)->str:
    def repl(m:re.Match[str])->str:
        raw=m.group(1)
        try: obj=json.loads(raw)
        except Exception: return m.group(0)
        typ=obj.get("@type") if isinstance(obj,dict) else None
        types={typ} if isinstance(typ,str) else set(typ or []) if isinstance(typ,list) else set()
        if "Article" not in types:
            return m.group(0)
        obj["headline"]=heading
        obj["description"]=desc
        obj["url"]=can
        obj["mainEntityOfPage"]={"@type":"WebPage","@id":can}
        return '<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False,separators=(",",":"))+'</script>'
    return JSONLD_RE.sub(repl,text)

def normalize(path:Path)->dict[str,Any]:
    original=path.read_text(encoding="utf-8")
    original_body=body_part(original)
    p=parse(original)
    can=canonical(p)
    heading=h1(original)
    old_desc=p.meta.get("description","")
    is_en=str(path).startswith("en/")
    locale="en_US" if is_en else "id_ID"

    if not can or not heading or not old_desc:
        raise RuntimeError(f"{path}: missing canonical/H1/description")

    new_desc,desc_changed,repair_reason=repair_description(original,old_desc)

    # Remove only target metadata tags.
    cleaned=META_TAG_RE.sub(lambda m:"" if meta_key(m.group(0)) in TARGET_META_KEYS else m.group(0),original)

    # Insert standardized metadata immediately before canonical link.
    can_match=re.search(r'<link\b[^>]*\brel=["\']canonical["\'][^>]*>',cleaned,re.I)
    if not can_match:
        can_match=re.search(r'<link\b[^>]*\bhref=["\']'+re.escape(can)+r'["\'][^>]*>',cleaned,re.I)
    if not can_match:
        raise RuntimeError(f"{path}: canonical tag insertion point not found")
    metas=standard_meta(new_desc,heading,can,locale)
    updated=cleaned[:can_match.start()]+metas+cleaned[can_match.start():]
    updated=update_article_schema(updated,heading,new_desc,can)

    if body_part(updated)!=original_body:
        raise RuntimeError(f"{path}: BODY CHANGED — abort")

    path.write_text(updated,encoding="utf-8")
    return {
        "path":str(path),
        "description_changed":desc_changed,
        "repair_reason":repair_reason,
        "old_description":old_desc,
        "new_description":new_desc,
        "body_unchanged":True,
    }

def qc(path:Path)->dict[str,Any]:
    text=path.read_text(encoding="utf-8")
    p=parse(text)
    can=canonical(p); heading=h1(text); desc=p.meta.get("description","")
    is_en=str(path).startswith("en/")
    expected_lang="en" if is_en else "id"
    expected_locale="en_US" if is_en else "id_ID"
    _,first_p=session_head(text)
    issues=[]

    checks={
        "html_lang":p.html_lang==expected_lang,
        "og_type":p.meta.get("og:type")=="article",
        "og_site_name":p.meta.get("og:site_name")=="TadabburLife",
        "og_locale":p.meta.get("og:locale")==expected_locale,
        "og_title":p.meta.get("og:title")==heading,
        "og_description":p.meta.get("og:description")==desc,
        "og_url":p.meta.get("og:url")==can,
        "og_image":p.meta.get("og:image")==f"https://tadabburlife.com/og/reflection/{'en' if is_en else 'id'}/{path.parent.name}.png",
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
        "description_not_truncated":not suspicious_truncation(desc,first_p),
    }
    issues += [k for k,v in checks.items() if not v]

    # Article schema description/headline must remain synced.
    articles=[]
    parse_errors=0
    for raw in JSONLD_RE.findall(text):
        try:
            obj=json.loads(raw)
            typ=obj.get("@type") if isinstance(obj,dict) else None
            types={typ} if isinstance(typ,str) else set(typ or []) if isinstance(typ,list) else set()
            if "Article" in types:
                articles.append(obj)
        except Exception:
            parse_errors+=1
    if parse_errors: issues.append("jsonld_parse_error")
    if len(articles)!=1:
        issues.append(f"article_count_{len(articles)}")
    elif articles[0].get("headline")!=heading or articles[0].get("description")!=desc:
        issues.append("article_metadata_drift")

    return {"path":str(path),"pass":not issues,"issues":issues,"description_length":len(desc)}

def main()->int:
    results=[normalize(p) for p in PATHS]
    rows=[qc(p) for p in PATHS]
    failures=[r for r in rows if not r["pass"]]
    summary={
        "files_checked":94,
        "body_unchanged_count":sum(1 for r in results if r["body_unchanged"]),
        "description_repairs":sum(1 for r in results if r["description_changed"]),
        "truncation_repairs":sum(1 for r in results if r["repair_reason"]=="truncated"),
        "thin_description_repairs":sum(1 for r in results if r["repair_reason"]=="thin"),
        "pass_count":sum(1 for r in rows if r["pass"]),
        "fail_count":len(failures),
        "overall_pass":not failures and all(r["body_unchanged"] for r in results),
    }
    (REPORT_DIR/"metadata-normalization-report.json").write_text(json.dumps({"summary":summary,"normalization":results,"qc":rows},ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# TadabburLife Metadata Technical Integrity + OG/Share QC","",
      f"- Files checked: 94 / 94",
      f"- Body unchanged: {summary['body_unchanged_count']} / 94",
      f"- Description repairs: {summary['description_repairs']}",
      f"- Truncation repairs: {summary['truncation_repairs']}",
      f"- Thin-description repairs: {summary['thin_description_repairs']}",
      f"- QC PASS: {summary['pass_count']} / 94",
      f"- FAIL: {summary['fail_count']}",
      f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}",""]
    if failures:
        lines+=["## Failures",""]+[f"- `{r['path']}`: {', '.join(r['issues'])}" for r in failures]
    (REPORT_DIR/"SUMMARY.md").write_text("\n".join(lines),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    for r in failures:
        print("FAIL",r)
    return 0 if summary["overall_pass"] else 1

if __name__=="__main__":
    sys.exit(main())
