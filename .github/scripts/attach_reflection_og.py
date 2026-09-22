#!/usr/bin/env python3
"""Attach generated Reflection Card OG images to all 94 session landings.

Only <head> is modified. <body> must remain byte-for-byte unchanged.
"""

from __future__ import annotations
import html
import re
import sys
from pathlib import Path

PATHS=[
    (Path("tadabbur")/f"{n:03d}"/"index.html",n,False)
    for n in range(1,48)
]+[
    (Path("en/tadabbur")/f"{n:03d}"/"index.html",n,True)
    for n in range(1,48)
]

TARGET_KEYS={
    "og:image","og:image:secure_url","og:image:type","og:image:width","og:image:height","og:image:alt",
    "twitter:image","twitter:image:alt"
}

META_RE=re.compile(r"<meta\b[^>]*>",re.I)

def body_part(text:str)->str:
    i=text.lower().find("<body")
    return text[i:] if i>=0 else ""

def attr(tag:str,name:str)->str:
    m=re.search(r'\b'+re.escape(name)+r'=["\']([^"\']*)["\']',tag,re.I)
    return html.unescape(m.group(1)) if m else ""

def meta_key(tag:str)->str:
    return (attr(tag,"property") or attr(tag,"name")).lower()

def h1(text:str)->str:
    m=re.search(r"<h1\b[^>]*>(.*?)</h1>",text,re.I|re.S)
    if not m:return ""
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",m.group(1)))).strip()

def canonical_tag(text:str)->re.Match[str]|None:
    return re.search(r'<link\b[^>]*\brel=["\']canonical["\'][^>]*>',text,re.I)

def esc(s:str)->str:
    return html.escape(s,quote=True)

def update(path:Path,n:int,is_en:bool)->dict:
    original=path.read_text(encoding="utf-8")
    original_body=body_part(original)
    heading=h1(original)
    if not heading:
        raise RuntimeError(f"{path}: missing H1")

    lang="en" if is_en else "id"
    image=f"https://tadabburlife.com/og/reflection/{lang}/{n:03d}.png"
    image_file=Path(f"og/reflection/{lang}/{n:03d}.png")
    if not image_file.exists():
        raise RuntimeError(f"{path}: generated OG image missing: {image_file}")

    # Remove old image fields only.
    cleaned=META_RE.sub(lambda m:"" if meta_key(m.group(0)) in TARGET_KEYS else m.group(0),original)

    # Upgrade twitter:card if present; add if absent.
    if re.search(r'<meta\b[^>]*\bname=["\']twitter:card["\'][^>]*>',cleaned,re.I):
        cleaned=re.sub(
            r'<meta\b[^>]*\bname=["\']twitter:card["\'][^>]*>',
            '<meta name="twitter:card" content="summary_large_image">',
            cleaned,count=1,flags=re.I
        )
    else:
        cm=canonical_tag(cleaned)
        if not cm: raise RuntimeError(f"{path}: canonical insertion point missing")
        cleaned=cleaned[:cm.start()]+'<meta name="twitter:card" content="summary_large_image">'+cleaned[cm.start():]

    alt=f"{heading} — TadabburLife Reflection Card"
    tags="".join([
        f'<meta property="og:image" content="{esc(image)}">',
        f'<meta property="og:image:secure_url" content="{esc(image)}">',
        '<meta property="og:image:type" content="image/png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{esc(alt)}">',
        f'<meta name="twitter:image" content="{esc(image)}">',
        f'<meta name="twitter:image:alt" content="{esc(alt)}">',
    ])
    cm=canonical_tag(cleaned)
    if not cm: raise RuntimeError(f"{path}: canonical tag missing")
    updated=cleaned[:cm.start()]+tags+cleaned[cm.start():]

    if body_part(updated)!=original_body:
        raise RuntimeError(f"{path}: BODY CHANGED — abort")
    path.write_text(updated,encoding="utf-8")
    return {"path":str(path),"image":image,"bytes":image_file.stat().st_size,"body_unchanged":True}

def main()->int:
    rows=[update(*spec) for spec in PATHS]
    ok=len(rows)==94 and all(r["body_unchanged"] and r["bytes"]>10000 for r in rows)
    print({
        "files_updated":len(rows),
        "body_unchanged":sum(1 for r in rows if r["body_unchanged"]),
        "images_present":sum(1 for r in rows if r["bytes"]>10000),
        "overall_pass":ok
    })
    return 0 if ok else 1

if __name__=="__main__":
    sys.exit(main())
