#!/usr/bin/env python3
"""Guard reviewed terminology parity between standalone pages and the interactive reader."""
from html.parser import HTMLParser
from pathlib import Path
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


def main():
    errors = []
    for check in CHECKS:
        reader_path = ROOT / check["reader"]
        landing_path = ROOT / check["landing"]
        try:
            reader = read_reader(reader_path, check["lang"], check["session"])
            landing = read_landing(landing_path)
        except (OSError, ValueError) as exc:
            errors.append(f"Sesi {check['session']} ({check['lang']}): {exc}")
            continue

        for source_name, content in (("reader", reader), ("landing", landing)):
            for phrase in check["required"]:
                if phrase not in content:
                    errors.append(
                        f"Sesi {check['session']} ({check['lang']}): "
                        f"required phrase {phrase!r} missing from {source_name}"
                    )
            for phrase in check["forbidden"]:
                if phrase in content:
                    errors.append(
                        f"Sesi {check['session']} ({check['lang']}): "
                        f"stale phrase {phrase!r} remains in {source_name}"
                    )

        if not errors:
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
