#!/usr/bin/env python3
"""Generate 94 branded OG images from the existing TadabburLife Reflection Card source.

The data rules intentionally mirror index.html:
- title = .session-head h2
- quote = first .call p, fallback .feature .tr, fallback title
- task = last .call p, fallback language default

Output is a landscape 1200x630 derivative of the same Reflection Card visual
language so social crawlers can consume a static image without JavaScript.
"""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any

W, H = 1200, 630
ROOT = Path(".")
OUT = Path("og/reflection")
REPORT = Path("qc-og-reflection-report")
REPORT.mkdir(exist_ok=True)

PATHS = [
    (Path("tadabbur") / f"{n:03d}" / "index.html", n, False)
    for n in range(1, 48)
] + [
    (Path("en/tadabbur") / f"{n:03d}" / "index.html", n, True)
    for n in range(1, 48)
]

def strip_tags(value: str) -> str:
    value = re.sub(r"<script\b[^>]*>.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style\b[^>]*>.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()

def first(pattern: str, text: str) -> str:
    m = re.search(pattern, text, re.I | re.S)
    return strip_tags(m.group(1)) if m else ""

def block(pattern: str, text: str) -> str:
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1) if m else ""

def extract_data(path: Path, n: int, is_en: bool) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    session_head = block(r'<div\s+class=["\']session-head["\'][^>]*>(.*?)</div>', text)
    title = first(r"<h2\b[^>]*>(.*?)</h2>", session_head)

    call_blocks = re.findall(r'<(?:div|section)\b[^>]*class=["\'][^"\']*\bcall\b[^"\']*["\'][^>]*>(.*?)</(?:div|section)>', text, re.I | re.S)
    call_ps: list[str] = []
    for cb in call_blocks:
        call_ps.extend(strip_tags(x) for x in re.findall(r"<p\b[^>]*>(.*?)</p>", cb, re.I | re.S) if strip_tags(x))

    feature = block(r'<(?:div|section)\b[^>]*class=["\'][^"\']*\bfeature\b[^"\']*["\'][^>]*>(.*?)</(?:div|section)>', text)
    feature_tr = first(r'<[^>]*class=["\'][^"\']*\btr\b[^"\']*["\'][^>]*>(.*?)</[^>]+>', feature)

    quote = call_ps[0] if call_ps else (feature_tr or title)
    task = call_ps[-1] if call_ps else (
        "Practice one concrete lesson from this session today."
        if is_en else
        "Praktikkan satu pelajaran konkret dari sesi ini hari ini."
    )
    url = (
        f"https://tadabburlife.com/en/tadabbur/{n:03d}/"
        if is_en else
        f"https://tadabburlife.com/tadabbur/{n:03d}/"
    )
    if not title or not quote or not task:
        raise RuntimeError(f"{path}: incomplete Reflection Card data")
    return {
        "session": f"{n:03d}",
        "language": "en" if is_en else "id",
        "title": title,
        "quote": quote,
        "task": task,
        "url": url,
        "source": str(path),
    }

def xml(s: str) -> str:
    return html.escape(s, quote=True)

def fit_lines(text: str, max_chars: int, max_lines: int) -> list[str]:
    words = text.replace("“", "").replace("”", "").split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = (current + " " + word).strip()
        if current and len(candidate) > max_chars:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while len(last) > max_chars - 1:
            last = last[:-1]
        lines[-1] = last.rstrip(" ,.;:-") + "…"
    return lines

def tspans(lines: list[str], x: int, y: int, line_height: int) -> str:
    return "".join(
        f'<tspan x="{x}" y="{y + i*line_height}">{xml(line)}</tspan>'
        for i, line in enumerate(lines)
    )

def render_svg(data: dict[str, Any]) -> str:
    en = data["language"] == "en"
    kicker = "QUR’AN REFLECTION TODAY" if en else "REFLEKSI AL-QUR’AN HARI INI"
    try_label = "TRY TODAY" if en else "COBA HARI INI"
    brand = "Read • Understand • Reflect • Practice" if en else "Baca • Pahami • Renungkan • Amalkan"
    sess = ("Session " if en else "Sesi ") + data["session"]

    q = data["quote"]
    q_len = len(q)
    if q_len <= 120:
        q_size, q_chars, q_lines, q_lh = 43, 43, 4, 51
    elif q_len <= 220:
        q_size, q_chars, q_lines, q_lh = 36, 52, 5, 43
    else:
        q_size, q_chars, q_lines, q_lh = 31, 60, 6, 37

    quote_lines = fit_lines(q, q_chars, q_lines)
    title_lines = fit_lines(data["title"], 46, 2)
    task_lines = fit_lines(data["task"], 66, 3)

    quote_y = 170
    title_y = min(410, quote_y + len(quote_lines)*q_lh + 30)
    task_box_y = min(470, title_y + len(title_lines)*34 + 28)
    task_text_y = task_box_y + 61

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#087054"/>
      <stop offset="100%" stop-color="#063d30"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect x="26" y="26" width="1148" height="578" rx="24" fill="none" stroke="#d4a72c" stroke-width="7"/>

  <text x="70" y="79" fill="#f2d87e" font-family="DejaVu Sans, sans-serif" font-size="23" font-weight="700" letter-spacing="3">{xml(kicker)}</text>
  <text x="70" y="120" fill="#f2d87e" font-family="DejaVu Sans, sans-serif" font-size="31" font-weight="800">TADABBURLIFE</text>
  <text x="1128" y="105" fill="#ffffff" font-family="DejaVu Sans, sans-serif" font-size="24" font-weight="700" text-anchor="end">{xml(sess)}</text>

  <text x="70" y="{quote_y}" fill="#ffffff" font-family="DejaVu Sans, sans-serif" font-size="{q_size}" font-weight="800">
    {tspans(['“'+quote_lines[0]] + quote_lines[1:-1] + ([quote_lines[-1]+'”'] if len(quote_lines)>1 else [quote_lines[0]+'”']), 70, quote_y, q_lh) if len(quote_lines)>1 else tspans(['“'+quote_lines[0]+'”'],70,quote_y,q_lh)}
  </text>

  <text x="70" y="{title_y}" fill="#f2d87e" font-family="DejaVu Sans, sans-serif" font-size="27" font-weight="700">
    {tspans(title_lines,70,title_y,34)}
  </text>

  <rect x="70" y="{task_box_y}" width="1060" height="112" rx="20" fill="#ffffff" fill-opacity=".09"/>
  <text x="94" y="{task_box_y+36}" fill="#f2d87e" font-family="DejaVu Sans, sans-serif" font-size="20" font-weight="800">{xml(try_label)}</text>
  <text x="94" y="{task_text_y}" fill="#ffffff" font-family="DejaVu Sans, sans-serif" font-size="21" font-weight="500">
    {tspans(task_lines,94,task_text_y,28)}
  </text>

  <text x="70" y="580" fill="#f2d87e" font-family="DejaVu Sans, sans-serif" font-size="20" font-weight="700">TadabburLife • {xml(brand)}</text>
  <text x="1128" y="580" fill="#ffffff" font-family="DejaVu Sans, sans-serif" font-size="18" font-weight="500" text-anchor="end">tadabburlife.com</text>
</svg>'''

def write_image(data: dict[str, Any]) -> dict[str, Any]:
    lang = data["language"]
    sid = data["session"]
    folder = OUT / lang
    folder.mkdir(parents=True, exist_ok=True)
    svg_path = folder / f"{sid}.svg"
    png_path = folder / f"{sid}.png"
    svg_path.write_text(render_svg(data), encoding="utf-8")
    try:
        subprocess.run(
            ["rsvg-convert", "-w", str(W), "-h", str(H), "-o", str(png_path), str(svg_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError:
        raise RuntimeError("rsvg-convert is not installed")
    if not png_path.exists() or png_path.stat().st_size < 10_000:
        raise RuntimeError(f"{png_path}: PNG generation failed or image too small")
    return {
        **data,
        "svg": str(svg_path),
        "png": str(png_path),
        "png_bytes": png_path.stat().st_size,
        "og_url": f"https://tadabburlife.com/og/reflection/{lang}/{sid}.png",
    }

def main() -> int:
    generated = []
    for path, n, is_en in PATHS:
        generated.append(write_image(extract_data(path, n, is_en)))

    manifest = {
        "generated_on": "2026-09-22",
        "width": W,
        "height": H,
        "format": "png",
        "source": "TadabburLife Reflection Card rules from index.html",
        "count": len(generated),
        "images": generated,
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    summary = {
        "expected": 94,
        "generated": len(generated),
        "id_count": sum(1 for x in generated if x["language"] == "id"),
        "en_count": sum(1 for x in generated if x["language"] == "en"),
        "png_min_bytes": min(x["png_bytes"] for x in generated),
        "png_max_bytes": max(x["png_bytes"] for x in generated),
        "overall_pass": len(generated) == 94,
    }
    (REPORT / "og-reflection-generation.json").write_text(
        json.dumps({"summary": summary, "images": generated}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (REPORT / "SUMMARY.md").write_text(
        "\n".join([
            "# TadabburLife Reflection Card → OG Image Generation",
            "",
            f"- Generated: {summary['generated']} / 94",
            f"- ID: {summary['id_count']} / 47",
            f"- EN: {summary['en_count']} / 47",
            f"- Size: 1200×630 PNG",
            f"- Minimum PNG bytes: {summary['png_min_bytes']}",
            f"- Maximum PNG bytes: {summary['png_max_bytes']}",
            f"- Overall: {'PASS' if summary['overall_pass'] else 'FAIL'}",
            "",
        ]),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    return 0 if summary["overall_pass"] else 1

if __name__ == "__main__":
    sys.exit(main())
