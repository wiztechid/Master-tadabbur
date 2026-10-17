#!/usr/bin/env python3
"""Static contract QC for all published bilingual session landing pages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import hashlib
import sys

ROOT=Path(__file__).resolve().parents[2]
BASE="https://tadabburlife.com"
FROZEN_TEMPLATE_CSS_BLOB_SHA="524bcb52805e1af028d85405a71c17090368509e"
def git_blob_sha(content):
    data=content.encode("utf-8")
    return hashlib.sha1(b"blob "+str(len(data)).encode("ascii")+b"\0"+data).hexdigest()
LEGAL={"about","privacy","cookies","terms","disclaimer","contact"}

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.attrs=[]
        self.h1=0
        self.styles=[]
        self.style_open=False
        self.jsonld=[]
        self.script_type=None
        self.script_data=[]
        self.links=[]
    def handle_starttag(self,tag,attrs):
        a={k.lower():v for k,v in attrs}
        self.attrs.append((tag.lower(),a))
        if tag.lower()=="h1": self.h1+=1
        if tag.lower()=="a" and a.get("href"): self.links.append(a["href"])
        if tag.lower()=="style": self.style_open=True; self.styles.append("")
        if tag.lower()=="script":
            self.script_type=a.get("type")
            self.script_data=[]
    def handle_endtag(self,tag):
        if tag.lower()=="style": self.style_open=False
        if tag.lower()=="script":
            if self.script_type=="application/ld+json":
                self.jsonld.append("".join(self.script_data))
            self.script_type=None; self.script_data=[]
    def handle_data(self,data):
        if self.style_open and self.styles: self.styles[-1]+=data
        if self.script_type: self.script_data.append(data)

def fail(errors,path,message): errors.append(f"{path}: {message}")
def attr(parser,tag,key,value):
    return [a for t,a in parser.attrs if t==tag and a.get(key)==value]
def meta(parser,key,value):
    return [a for t,a in parser.attrs if t=="meta" and a.get(key)==value]

errors=[]
checked=0
for n in range(1,50):
    number=f"{n:03d}"
    for lang,folder,language in (("id","tadabbur","id-ID"),("en","en/tadabbur","en")):
        rel=f"{folder}/{number}/index.html"
        path=ROOT/rel
        if not path.exists():
            fail(errors,rel,"missing landing"); continue
        checked+=1
        html=path.read_text(encoding="utf-8")
        p=Page(); p.feed(html)
        if p.styles or any("style" in a for _,a in p.attrs): fail(errors,rel,"inline styles are forbidden; use the frozen shared stylesheet")
        expected=f"{BASE}/{folder}/{number}/"
        titles=[a.get("content") for a in meta(p,"property","og:title")]
        descriptions=[a.get("content") for a in meta(p,"property","og:description")]
        canonicals=attr(p,"link","rel","canonical")
        viewport=meta(p,"name","viewport")
        desc=meta(p,"name","description")
        robots=meta(p,"name","robots")
        hreflang={a.get("hreflang"):a.get("href") for a in attr(p,"link","rel","alternate")}
        if p.h1!=1: fail(errors,rel,f"expected exactly one H1, got {p.h1}")
        if len(canonicals)!=1 or canonicals[0].get("href")!=expected: fail(errors,rel,"canonical missing, duplicated, or mismatched")
        if len(viewport)!=1: fail(errors,rel,"expected one viewport declaration")
        if len(desc)!=1 or not desc[0].get("content"): fail(errors,rel,"meta description missing or duplicated")
        if not hreflang.get("id") or not hreflang.get("en") or not hreflang.get("x-default"): fail(errors,rel,"id/en/x-default hreflang incomplete")
        else:
            if hreflang["id"]!=f"{BASE}/tadabbur/{number}/" or hreflang["en"]!=f"{BASE}/en/tadabbur/{number}/" or hreflang["x-default"]!=f"{BASE}/tadabbur/{number}/":
                fail(errors,rel,"hreflang target mismatch")
        if len(titles)!=1 or not titles[0]: fail(errors,rel,"OG title missing or duplicated")
        twitter_titles=[a.get("content") for a in meta(p,"name","twitter:title")]
        twitter_descriptions=[a.get("content") for a in meta(p,"name","twitter:description")]
        if len(twitter_titles)!=1 or (titles and twitter_titles[0]!=titles[0]): fail(errors,rel,"Twitter title must match OG title")
        if len(twitter_descriptions)!=1 or (descriptions and twitter_descriptions[0]!=descriptions[0]): fail(errors,rel,"Twitter description must match OG description")
        if len(descriptions)!=1 or not descriptions[0]: fail(errors,rel,"OG description missing or duplicated")
        ogtypes=attr(p,"meta","property","og:type")
        ogurls=attr(p,"meta","property","og:url")
        if len(ogtypes)!=1 or ogtypes[0].get("content")!="article": fail(errors,rel,"OG type must be article")
        if len(ogurls)!=1 or ogurls[0].get("content")!=expected: fail(errors,rel,"OG URL must match canonical")
        if len(meta(p,"property","og:site_name"))!=1: fail(errors,rel,"OG site name missing or duplicated")
        if len(meta(p,"property","og:locale"))!=1: fail(errors,rel,"OG locale missing or duplicated")
        if len(meta(p,"name","twitter:card"))!=1 or len(meta(p,"name","twitter:title"))!=1 or len(meta(p,"name","twitter:description"))!=1:
            fail(errors,rel,"Twitter card/title/description incomplete")
        stylesheet=attr(p,"link","rel","stylesheet")
        expected_css="../../assets/css/session-landing-v1.css?v=1.2" if lang=="id" else "../../../assets/css/session-landing-v1.css?v=1.2"
        if len(stylesheet)!=1 or stylesheet[0].get("href")!=expected_css:
            fail(errors,rel,"expected exactly one shared session stylesheet with correct path")
        else:
            css_path=(path.parent/unquote(urlsplit(stylesheet[0]["href"]).path)).resolve()
            if not css_path.is_file(): fail(errors,rel,"shared session stylesheet asset missing")
            else:
                shared_css=css_path.read_text(encoding="utf-8")
                if git_blob_sha(shared_css)!=FROZEN_TEMPLATE_CSS_BLOB_SHA:
                    fail(errors,rel,"frozen shared template CSS changed; thaw and update the freeze record explicitly")
                if not re.search(r"@media\s*\(",shared_css):
                    fail(errors,rel,"responsive breakpoint missing from shared CSS")
                ayahbox_rule=re.search(r"\.ayahbox\s*\{([^}]*)\}",shared_css)
                arabic_rule=re.search(r'p\[lang="ar"\]\s*\{([^}]*)\}',shared_css)
                if not ayahbox_rule or "background:#0b5a45" not in ayahbox_rule.group(1):
                    fail(errors,rel,"Qur'an ayahbox background must remain green")
                if not arabic_rule or "background:#0b5a45" not in arabic_rule.group(1):
                    fail(errors,rel,"Arabic verse block background must be green")
        if n==49:
            heading="Tiga Ayat, Tiga Sudut Pandang" if lang=="id" else "Three Quranic Anchors"
            featured=re.search(r'<section\b(?=[^>]*\bclass=["\'][^"\']*\bfeature\b)[^>]*>(?:(?!</section>).)*?'+re.escape(heading),html,re.S)
            if not featured: fail(errors,rel,"primary Qur'an anchors must use the green feature card")
        if re.search(r"pagead\.googlesyndication\.com/pagead/js/adsbygoogle",html,re.I): fail(errors,rel,"AdSense loader found on session landing")
        footer=html[html.rfind("<footer"):] if "<footer" in html else ""
        footer_paths=set()
        for href in p.links:
            parts=urlsplit(href)
            pathpart=unquote(parts.path).strip("/")
            if pathpart:
                tail=pathpart.rstrip("/").split("/")[-1].lower()
                if tail in LEGAL: footer_paths.add(tail)
        missing=LEGAL-footer_paths
        if missing: fail(errors,rel,"trust/legal destination missing: "+", ".join(sorted(missing)))
        if any(not href or href.strip()=="#" or href.lower().startswith("javascript:") for href in p.links):
            fail(errors,rel,"inert anchor found")
        images=attr(p,"meta","property","og:image")
        twimages=meta(p,"name","twitter:image")
        if images:
            if len(images)!=1 or len(twimages)!=1 or images[0].get("content")!=twimages[0].get("content"):
                fail(errors,rel,"OG and Twitter image metadata must match")
            else:
                image_path=urlsplit(images[0]["content"]).path.lstrip("/")
                if not (ROOT/unquote(image_path)).is_file(): fail(errors,rel,"referenced OG image asset missing")
        elif twimages:
            fail(errors,rel,"Twitter image exists without an OG image")
        objects=[]
        for raw in p.jsonld:
            try: objects.append(json.loads(raw))
            except Exception as exc: fail(errors,rel,f"invalid JSON-LD: {exc}")
        article=next((o for o in objects if isinstance(o,dict) and o.get("@type")=="Article"),None)
        crumb=next((o for o in objects if isinstance(o,dict) and o.get("@type")=="BreadcrumbList"),None)
        if not article: fail(errors,rel,"Article JSON-LD missing")
        else:
            for key in ("headline","description","inLanguage","author","publisher","mainEntityOfPage"):
                if not article.get(key): fail(errors,rel,f"Article JSON-LD missing {key}")
            if article.get("inLanguage")!=language: fail(errors,rel,"Article inLanguage mismatches page language")
            main=article.get("mainEntityOfPage")
            mainurl=main.get("@id") if isinstance(main,dict) else main
            if mainurl!=expected: fail(errors,rel,"Article mainEntityOfPage mismatches canonical")
            if article.get("author",{}).get("@type")!="Person": fail(errors,rel,"Article author must be a Person")
            if article.get("publisher",{}).get("@type")!="Organization": fail(errors,rel,"Article publisher must be an Organization")
        if not crumb: fail(errors,rel,"BreadcrumbList JSON-LD missing")
        elif len(crumb.get("itemListElement",[]))<2: fail(errors,rel,"BreadcrumbList must include home and current session")

print(f"Template contract QC: {checked}/98 pages inspected; {'PASS' if not errors else 'FAIL'}")
for item in errors: print(" -",item)
sys.exit(bool(errors))
