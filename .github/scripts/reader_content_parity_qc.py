#!/usr/bin/env python3
"""Guard reviewed terminology parity between standalone pages and the interactive reader."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]

CHECKS = [
    {
        "session": "001",
        "lang": "id",
        "reader": "data/sessions-001-017.html",
        "landing": "tadabbur/001/index.html",
        "required": ["kompas keputusan", "Kerangka refleksi ini"],
        "forbidden": ["Decision Compass", "Framework ini"],
    },
    {
        "session": "002",
        "lang": "id",
        "reader": "data/sessions-001-017.html",
        "landing": "tadabbur/002/index.html",
        "required": ["Audit Profil"],
        "forbidden": ["Profile Audit"],
    },
    {
        "session": "006",
        "lang": "id",
        "reader": "data/sessions-001-017.html",
        "landing": "tadabbur/006/index.html",
        "required": ["Cek Respons saat Tertekan"],
        "forbidden": ["Pressure Check"],
    },
    {
        "session": "016",
        "lang": "en",
        "reader": "data/sessions-001-017.html",
        "landing": "en/tadabbur/016/index.html",
        "required": ["Carry Forward", "review what you are carrying forward"],
        "forbidden": ["Provision", "audit your own provision"],
    },
]


class ReaderArticleText(HTMLParser):
    def __init__(self, language, session):
        super().__init__(convert_charrefs=True)
        self.language = language
        self.session = str(int(session))
        self.active = False
        self.finished = False
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag != "article" or self.active or self.finished:
            return
        values = dict(attrs)
        if (values.get("data-lang") == self.language
                and values.get("data-session-number") == self.session):
            self.active = True

    def handle_endtag(self, tag):
        if tag == "article" and self.active:
            self.active = False
            self.finished = True

    def handle_data(self, data):
        if self.active:
            self.text.append(data)


class LandingPageText(HTMLParser):
    SKIP = {"head", "script", "style"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip_stack = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            for index in range(len(self.skip_stack) - 1, -1, -1):
                if self.skip_stack[index] == tag:
                    del self.skip_stack[index:]
                    break

    def handle_data(self, data):
        if not self.skip_stack:
            self.text.append(data)


def read_reader(path, language, session):
    parser = ReaderArticleText(language, session)
    parser.feed(path.read_text(encoding="utf-8"))
    if not parser.finished:
        raise ValueError(
            f"interactive reader article not found: session {session} ({language}) in {path}"
        )
    return " ".join(parser.text)


def read_landing(path):
    parser = LandingPageText()
    parser.feed(path.read_text(encoding="utf-8"))
    return " ".join(parser.text)



def validate_reader_verse_contract(errors):
    index = ROOT / "index.html"
    try:
        page = index.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Interactive reader visual contract: cannot read index.html: {exc}")
        return

    style = re.search(r"<style>(.*?)</style>", page, flags=re.IGNORECASE | re.DOTALL)
    if not style:
        errors.append("Interactive reader visual contract: homepage style block missing")
        return
    css = re.sub(r"\s+", "", style.group(1))
    if "Noto+Naskh+Arabic" not in page:
        errors.append("Interactive reader visual contract: Noto Naskh Arabic font link missing")

    required_css = {
        "featured card geometry": "#session-content-root .session .card.feature,#session-content-root .en-session .card.feature{padding:22px!important;margin:15px 0!important;border-radius:22px!important}",
        "green/gold verse panel": "#session-content-root .feature .ayahbox{background:#0b5a45;border:2px solid #d9b94d;border-radius:20px;padding:22px}",
        "white Noto Arabic main verse": '#session-content-root .feature .ayah{color:#fff;font-family:"Noto Naskh Arabic",serif;font-size:40px!important;line-height:2.15!important}',
        "green/gold/white Arabic excerpts": '#session-content-root p[lang="ar"]{display:block;margin:14px 0;padding:16px 18px;background:#0b5a45;border:2px solid #d9b94d;border-radius:20px;color:#fff',
        "mobile verse size": "@media(max-width:650px){#session-content-root .session .card.feature,#session-content-root .en-session .card.feature{padding:20px 17px!important;margin:14px 0!important;border-radius:16px!important}#session-content-root .feature .ayah{font-size:32px!important;line-height:2.05!important}",
    }
    for label, fragment in required_css.items():
        if fragment.replace(" ", "") not in css:
            errors.append(f"Interactive reader visual contract: {label} rule missing")

    expected = {
        f"{prefix}s{number}"
        for number in range(1, 50)
        for prefix in ("", "en-")
    }
    found = {}
    for module in sorted((ROOT / "data").glob("sessions-*.html")):
        try:
            source = module.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"Interactive reader visual contract: cannot read {module}: {exc}")
            continue
        for article in re.findall(r"<article\b[\s\S]*?</article>", source, flags=re.IGNORECASE):
            opening = re.match(r'<article\b([^>]*)>', article, flags=re.IGNORECASE)
            if not opening:
                continue
            id_match = re.search(r'\bid="([^"]+)"', opening.group(1))
            article_id = id_match.group(1) if id_match else None
            if not article_id or not re.fullmatch(r"(?:en-)?s\d+", article_id):
                continue
            found[article_id] = article
    if set(found) != expected:
        missing, extra = sorted(expected - set(found)), sorted(set(found) - expected)
        if missing:
            errors.append("Interactive reader visual contract: missing modules " + ", ".join(missing))
        if extra:
            errors.append("Interactive reader visual contract: unexpected modules " + ", ".join(extra))

    for article_id, article in found.items():
        number_match = re.search(r"(\d+)$", article_id)
        number = int(number_match.group(1))
        if number in (16, 44):
            if "data-ayat-crossref" not in article:
                errors.append(f"Interactive reader visual contract: {article_id} must remain a cross-reference session")
        elif number == 49:
            arabic = re.findall(r'<p\b[^>]*\blang="ar"[^>]*>', article, flags=re.IGNORECASE)
            if len(arabic) < 3:
                errors.append(f"Interactive reader visual contract: {article_id} must retain its three styled Arabic anchors")
        else:
            feature = re.search(r'<section\b[^>]*\bclass="[^"]*\bfeature\b', article, flags=re.IGNORECASE)
            if not feature or not re.search(r'class="[^"]*\bayahbox\b', article) or not re.search(r'class="[^"]*\bayah\b', article):
                errors.append(f"Interactive reader visual contract: {article_id} is missing its featured Ayat Utama module")
    if not any(e.startswith("Interactive reader visual contract:") for e in errors):
        print("PASS Interactive Reader visual parity: 98 bilingual modules, Ayat Utama and Arabic text styles")

def main():
    errors = []
    validate_reader_verse_contract(errors)
    for check in CHECKS:
        reader_path = ROOT / check["reader"]
        landing_path = ROOT / check["landing"]
        try:
            reader = read_reader(reader_path, check["lang"], check["session"])
            landing = read_landing(landing_path)
        except (OSError, ValueError) as exc:
            errors.append(f"Sesi {check['session']} ({check['lang']}): {exc}")
            continue

        pair_errors = []
        for source_name, content in (("reader", reader), ("landing", landing)):
            for phrase in check["required"]:
                if phrase not in content:
                    pair_errors.append(
                        f"Sesi {check['session']} ({check['lang']}): "
                        f"required phrase {phrase!r} missing from {source_name}"
                    )
            for phrase in check["forbidden"]:
                if phrase in content:
                    pair_errors.append(
                        f"Sesi {check['session']} ({check['lang']}): "
                        f"stale phrase {phrase!r} remains in {source_name}"
                    )

        errors.extend(pair_errors)
        if not pair_errors:
            print(f"PASS Sesi {check['session']} ({check['lang']}) reader/landing parity")

    if errors:
        print("Reader content parity QC failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Reader content parity QC passed ({len(CHECKS)} reviewed session pairs).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
