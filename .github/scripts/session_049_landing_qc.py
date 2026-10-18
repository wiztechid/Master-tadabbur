#!/usr/bin/env python3
"""Lightweight static prepublish gate for bilingual Session 049 landings."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys
import re

ROOT = Path(__file__).resolve().parents[2]
PAGES = [ROOT / "tadabbur/049/index.html", ROOT / "en/tadabbur/049/index.html"]

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.h1 = 0
        self.viewport = False
        self.canonical = False
        self.styles = ""
        self.stylesheets = []
        self.in_style = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "meta" and a.get("name") == "viewport":
            self.viewport = True
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = True
        if tag == "link" and a.get("rel") == "stylesheet" and a.get("href"):
            self.stylesheets.append(a["href"])
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag == "style":
            self.in_style = True
    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False
    def handle_data(self, data):
        if self.in_style:
            self.styles += data

issues = []
for page in PAGES:
    if not page.exists():
        issues.append(f"missing page: {page}")
        continue
    scan = Scan()
    scan.feed(page.read_text(encoding="utf-8"))
    if scan.h1 != 1:
        issues.append(f"{page}: expected one H1, found {scan.h1}")
    if not scan.viewport or not scan.canonical:
        issues.append(f"{page}: missing viewport or canonical")
    expected_css = "../../../assets/css/session-landing-v1.css?v=1.4" if "/en/" in page.as_posix() else "../../assets/css/session-landing-v1.css?v=1.4"
    shared_stylesheets = [href for href in scan.stylesheets if "session-landing-v1.css" in href]
    if shared_stylesheets != [expected_css]:
        issues.append(f"{page}: expected one shared stylesheet at {expected_css}")
    else:
        css_path = (page.parent / unquote(urlsplit(shared_stylesheets[0]).path)).resolve()
        if not css_path.is_file():
            issues.append(f"{page}: shared stylesheet missing")
        else:
            scan.styles = css_path.read_text(encoding="utf-8")
    if not any("fonts.googleapis.com/css2?family=Noto+Naskh+Arabic" in href and "display=swap" in href for href in scan.stylesheets):
        issues.append(f"{page}: Noto Naskh Arabic font stylesheet missing")
    heading = "Three Quranic Anchors" if "/en/" in page.as_posix() else "Tiga Ayat, Tiga Sudut Pandang"
    if not re.search(r'<section class="card feature">.*?'+re.escape(heading), page.read_text(encoding="utf-8"), re.S):
        issues.append(f"{page}: Quran anchors must use the green feature card")
    for selector in (".wrap", ".session-head", ".card", ".breadcrumb", ".seo-h1", "@media"):
        if selector not in scan.styles:
            issues.append(f"{page}: missing responsive/template selector {selector}")
    for href in scan.links:
        if not href.strip() or href == "#" or href.lower().startswith("javascript:"):
            issues.append(f"{page}: inert link {href!r}")
            continue
        url = urlsplit(href)
        if url.scheme or url.netloc or href.startswith("#"):
            continue
        if url.path.startswith("/"):
            target = ROOT / unquote(url.path.lstrip("/"))
        else:
            target = page.parent / unquote(url.path)
        if target.is_dir():
            target = target / "index.html"
        elif not target.suffix:
            target = target / "index.html"
        if not target.resolve().is_relative_to(ROOT.resolve()) or not target.exists():
            issues.append(f"{page}: unresolved internal link {href}")
print("Session 049 prepublish:", "PASS" if not issues else "FAIL")
for issue in issues:
    print(" -", issue)
sys.exit(bool(issues))
