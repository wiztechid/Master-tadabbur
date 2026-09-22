#!/usr/bin/env python3
"""Normalize Article + BreadcrumbList JSON-LD across 94 TadabburLife session landings.

Scope is intentionally limited to JSON-LD inside <head>. The script asserts that
<body> content remains byte-for-byte identical for every modified file.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(".")
REPORT_DIR = Path("qc-schema-report")
REPORT_DIR.mkdir(exist_ok=True)

PATHS = [
    Path(prefix) / f"{n:03d}" / "index.html"
    for prefix in ("tadabbur", "en/tadabbur")
    for n in range(1, 48)
]

JSONLD_RE = re.compile(
    r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>',
    re.I | re.S,
)

def first(pattern: str, text: str, flags: int = re.I | re.S) -> str:
    m = re.search(pattern, text, flags)
    return html.unescape(m.group(1).strip()) if m else ""

def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()

def meta_description(text: str) -> str:
    return (
        first(r'<meta\b[^>]*\bname=["\']description["\'][^>]*\bcontent=["\']([^"\']*)', text)
        or first(r'<meta\b[^>]*\bcontent=["\']([^"\']*)["\'][^>]*\bname=["\']description["\']', text)
    )

def canonical(text: str) -> str:
    return (
        first(r'<link\b[^>]*\brel=["\']canonical["\'][^>]*\bhref=["\']([^"\']+)', text)
        or first(r'<link\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*\brel=["\']canonical["\']', text)
    )

def h1(text: str) -> str:
    return strip_tags(first(r"<h1\b[^>]*>(.*?)</h1>", text))

def title(text: str) -> str:
    return strip_tags(first(r"<title\b[^>]*>(.*?)</title>", text))

def body_part(text: str) -> str:
    i = text.lower().find("<body")
    return text[i:] if i >= 0 else ""

def load_existing_jsonld(text: str) -> list[Any]:
    out: list[Any] = []
    for raw in JSONLD_RE.findall(text):
        try:
            out.append(json.loads(raw))
        except Exception:
            # QC will catch malformed leftovers; do not silently rewrite unknown invalid data.
            out.append({"__malformed_raw__": raw})
    return out

def schema_types(obj: Any) -> set[str]:
    if not isinstance(obj, dict):
        return set()
    typ = obj.get("@type")
    if isinstance(typ, str):
        return {typ}
    if isinstance(typ, list):
        return {str(x) for x in typ}
    return set()

def json_script(obj: dict[str, Any]) -> str:
    return '<script type="application/ld+json">' + json.dumps(
        obj, ensure_ascii=False, separators=(",", ":")
    ) + "</script>"

def normalize_file(path: Path) -> dict[str, Any]:
    original = path.read_text(encoding="utf-8")
    original_body = body_part(original)

    can = canonical(original)
    desc = meta_description(original)
    headline = h1(original) or title(original)
    is_en = str(path).startswith("en/")
    lang = "en" if is_en else "id-ID"

    if not can or not desc or not headline:
        raise RuntimeError(f"{path}: missing canonical/description/headline")

    existing = load_existing_jsonld(original)
    malformed = [x for x in existing if isinstance(x, dict) and "__malformed_raw__" in x]
    if malformed:
        raise RuntimeError(f"{path}: malformed existing JSON-LD; refusing automatic rewrite")

    article_old = next(
        (x for x in existing if isinstance(x, dict) and "Article" in schema_types(x)),
        {},
    )

    article: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": desc,
        "inLanguage": lang,
        "url": can,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": can,
        },
        "author": {
            "@type": "Person",
            "name": "Suiza Ixan Saputro",
        },
        "publisher": {
            "@type": "Organization",
            "@id": "https://tadabburlife.com/#organization",
            "name": "TadabburLife",
            "url": "https://tadabburlife.com/",
        },
        "isPartOf": {
            "@type": "WebSite",
            "@id": "https://tadabburlife.com/#website",
            "name": "TadabburLife",
            "url": "https://tadabburlife.com/",
        },
    }

    # Preserve useful pre-existing editorial/schema fields without inventing them.
    for key in ("alternativeHeadline", "keywords", "datePublished", "dateModified"):
        if isinstance(article_old, dict) and article_old.get(key):
            article[key] = article_old[key]

    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "TadabburLife",
                "item": "https://tadabburlife.com/",
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": headline,
                "item": can,
            },
        ],
    }

    def remove_target_jsonld(match: re.Match[str]) -> str:
        raw = match.group(1)
        try:
            obj = json.loads(raw)
        except Exception:
            return match.group(0)
        types = schema_types(obj)
        if "Article" in types or "BreadcrumbList" in types:
            return ""
        return match.group(0)

    updated = JSONLD_RE.sub(remove_target_jsonld, original)
    injection = json_script(article) + json_script(breadcrumb)
    if "</head>" not in updated.lower():
        raise RuntimeError(f"{path}: </head> missing")

    # Preserve original casing of closing head using regex.
    updated, count = re.subn(r"</head>", injection + "</head>", updated, count=1, flags=re.I)
    if count != 1:
        raise RuntimeError(f"{path}: schema injection failed")

    if body_part(updated) != original_body:
        raise RuntimeError(f"{path}: BODY CHANGED — aborting to protect sacred/content layer")

    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")

    return {
        "path": str(path),
        "changed": changed,
        "canonical": can,
        "headline": headline,
        "inLanguage": lang,
        "body_unchanged": body_part(updated) == original_body,
        "preserved_fields": [
            key for key in ("alternativeHeadline", "keywords", "datePublished", "dateModified")
            if key in article
        ],
    }

def qc_file(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    can = canonical(text)
    headline = h1(text) or title(text)
    desc = meta_description(text)
    expected_lang = "en" if str(path).startswith("en/") else "id-ID"

    parsed: list[Any] = []
    parse_errors = 0
    for raw in JSONLD_RE.findall(text):
        try:
            parsed.append(json.loads(raw))
        except Exception:
            parse_errors += 1

    articles = [x for x in parsed if isinstance(x, dict) and "Article" in schema_types(x)]
    crumbs = [x for x in parsed if isinstance(x, dict) and "BreadcrumbList" in schema_types(x)]

    issues: list[str] = []
    if parse_errors:
        issues.append("jsonld_parse_error")
    if len(articles) != 1:
        issues.append(f"article_count_{len(articles)}")
    if len(crumbs) != 1:
        issues.append(f"breadcrumb_count_{len(crumbs)}")

    if len(articles) == 1:
        a = articles[0]
        checks = {
            "headline": a.get("headline") == headline,
            "description": a.get("description") == desc,
            "inLanguage": a.get("inLanguage") == expected_lang,
            "url": a.get("url") == can,
            "mainEntityOfPage": isinstance(a.get("mainEntityOfPage"), dict)
                and a["mainEntityOfPage"].get("@type") == "WebPage"
                and a["mainEntityOfPage"].get("@id") == can,
            "author": isinstance(a.get("author"), dict)
                and a["author"].get("@type") == "Person"
                and a["author"].get("name") == "Suiza Ixan Saputro",
            "publisher": isinstance(a.get("publisher"), dict)
                and a["publisher"].get("@type") == "Organization"
                and a["publisher"].get("name") == "TadabburLife"
                and a["publisher"].get("url") == "https://tadabburlife.com/",
            "isPartOf": isinstance(a.get("isPartOf"), dict)
                and a["isPartOf"].get("@type") == "WebSite"
                and a["isPartOf"].get("name") == "TadabburLife"
                and a["isPartOf"].get("url") == "https://tadabburlife.com/",
        }
        issues += [f"article_{k}" for k, ok in checks.items() if not ok]

    if len(crumbs) == 1:
        items = crumbs[0].get("itemListElement")
        if not isinstance(items, list) or len(items) != 2:
            issues.append("breadcrumb_items")
        else:
            b1, b2 = items
            if not (
                isinstance(b1, dict)
                and b1.get("position") == 1
                and b1.get("name") == "TadabburLife"
                and b1.get("item") == "https://tadabburlife.com/"
            ):
                issues.append("breadcrumb_home")
            if not (
                isinstance(b2, dict)
                and b2.get("position") == 2
                and b2.get("name") == headline
                and b2.get("item") == can
            ):
                issues.append("breadcrumb_current")

    return {
        "path": str(path),
        "pass": not issues,
        "issues": issues,
        "article_count": len(articles),
        "breadcrumb_count": len(crumbs),
        "jsonld_parse_errors": parse_errors,
    }

def main() -> int:
    missing = [str(p) for p in PATHS if not p.exists()]
    if missing:
        print("Missing expected landing files:", *missing, sep="\n- ")
        return 1

    results = []
    try:
        for path in PATHS:
            results.append(normalize_file(path))
    except Exception as exc:
        print(f"NORMALIZATION ERROR: {exc}", file=sys.stderr)
        return 1

    qc = [qc_file(path) for path in PATHS]
    failures = [x for x in qc if not x["pass"]]

    summary = {
        "files_expected": 94,
        "files_checked": len(qc),
        "files_changed": sum(1 for x in results if x["changed"]),
        "body_unchanged_count": sum(1 for x in results if x["body_unchanged"]),
        "article_pass_count": sum(1 for x in qc if x["article_count"] == 1),
        "breadcrumb_pass_count": sum(1 for x in qc if x["breadcrumb_count"] == 1),
        "jsonld_parse_error_count": sum(x["jsonld_parse_errors"] for x in qc),
        "pass_count": sum(1 for x in qc if x["pass"]),
        "fail_count": len(failures),
        "overall_pass": len(qc) == 94 and not failures
            and all(x["body_unchanged"] for x in results),
    }

    payload = {"summary": summary, "normalization": results, "qc": qc}
    (REPORT_DIR / "schema-normalization-report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = [
        "# TadabburLife Schema Normalization QC",
        "",
        f"- Session landing files checked: {summary['files_checked']} / 94",
        f"- Files changed: {summary['files_changed']}",
        f"- Body unchanged: {summary['body_unchanged_count']} / 94",
        f"- Exactly one Article schema: {summary['article_pass_count']} / 94",
        f"- Exactly one BreadcrumbList schema: {summary['breadcrumb_pass_count']} / 94",
        f"- JSON-LD parse errors: {summary['jsonld_parse_error_count']}",
        f"- QC pass: {summary['pass_count']} / 94",
        f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}",
        "",
    ]
    if failures:
        lines += ["## Failures", ""]
        for row in failures:
            lines.append(f"- `{row['path']}`: {', '.join(row['issues'])}")
    (REPORT_DIR / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    if failures:
        for row in failures:
            print("FAIL", row["path"], row["issues"])
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
