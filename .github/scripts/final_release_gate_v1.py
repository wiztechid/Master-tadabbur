#!/usr/bin/env python3
"""TadabburLife Final Release Gate v1.0.

Gate revision: post-schema-parser hardening (2026-09-23).

Runs source-integrity + live custom-domain checks and writes one durable release
report. This gate is read-only with respect to public content. The keyword-map
sync script is executed only to prove idempotency; any resulting map diff fails
this gate and is not committed by the workflow.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".github" / "qc-state" / "final-release-v1"
LOGS = OUT / "logs"
OUT.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

BASE = "https://tadabburlife.com"
TESTED_SHA = os.environ.get("GITHUB_SHA", "")

def load_json(path: str) -> dict[str, Any] | None:
    p = ROOT / path
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None

def report_summary(path: str) -> dict[str, Any]:
    obj = load_json(path)
    if not isinstance(obj, dict):
        return {}
    s = obj.get("summary")
    if isinstance(s, dict):
        return s
    # Homepage report uses top-level overallPass.
    if "overallPass" in obj:
        return {
            "overall_pass": bool(obj.get("overallPass")),
            "propagated": obj.get("propagated"),
            "profiles": len(obj.get("profiles") or []),
        }
    return {}

def run(name: str, cmd: list[str], report: str | None = None, report_required: bool = False) -> dict[str, Any]:
    log_path = LOGS / f"{name}.log"
    started = time.time()
    with log_path.open("w", encoding="utf-8") as fh:
        proc = subprocess.Popen(
            cmd,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            sys.stdout.write(f"[{name}] {line}")
            fh.write(line)
        rc = proc.wait()
    summary = report_summary(report) if report else {}
    report_ok = True
    if report_required:
        report_ok = bool(summary) and bool(summary.get("overall_pass", summary.get("overallPass", False)))
    passed = rc == 0 and report_ok
    return {
        "name": name,
        "command": cmd,
        "exit_code": rc,
        "duration_seconds": round(time.time() - started, 2),
        "report": report,
        "report_summary": summary,
        "pass": passed,
    }

def source_inventory_check() -> dict[str, Any]:
    issues: list[str] = []
    expected = {f"{BASE}/"}
    expected |= {f"{BASE}/tadabbur/", f"{BASE}/en/tadabbur/"}
    expected |= {f"{BASE}/tadabbur/{n:03d}/" for n in range(1,48)}
    expected |= {f"{BASE}/en/tadabbur/{n:03d}/" for n in range(1,48)}
    expected |= {
        f"{BASE}/about/",
        f"{BASE}/privacy/",
        f"{BASE}/cookies/",
        f"{BASE}/terms/",
        f"{BASE}/disclaimer/",
        f"{BASE}/contact/",
    }

    sitemap = ROOT / "sitemap.xml"
    actual: set[str] = set()
    try:
        root = ET.fromstring(sitemap.read_text(encoding="utf-8"))
        actual = {(x.text or "").strip() for x in root.findall(".//{*}loc") if (x.text or "").strip()}
    except Exception as exc:
        issues.append(f"sitemap_parse:{exc!r}")

    if len(expected) != 103:
        issues.append(f"internal_expected_count_{len(expected)}")
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing: issues.append(f"sitemap_missing:{missing}")
        if extra: issues.append(f"sitemap_extra:{extra}")

    for n in range(1,48):
        for prefix in ("tadabbur","en/tadabbur"):
            p = ROOT / prefix / f"{n:03d}" / "index.html"
            if not p.exists():
                issues.append(f"missing_landing:{p.relative_to(ROOT)}")

    for p in (
        "index.html","tadabbur/index.html","en/tadabbur/index.html",
        "about/index.html","privacy/index.html","cookies/index.html",
        "terms/index.html","disclaimer/index.html","contact/index.html",
        "robots.txt","sitemap.xml","CNAME",
    ):
        if not (ROOT / p).exists():
            issues.append(f"missing_public_file:{p}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8") if (ROOT/"robots.txt").exists() else ""
    if "Disallow: /owner/" not in robots:
        issues.append("robots_owner_disallow_missing")
    if f"Sitemap: {BASE}/sitemap.xml" not in robots:
        issues.append("robots_sitemap_pointer_missing")

    cname = (ROOT / "CNAME").read_text(encoding="utf-8").strip() if (ROOT/"CNAME").exists() else ""
    if cname != "tadabburlife.com":
        issues.append(f"cname:{cname!r}")

    return {
        "name": "source_public_inventory",
        "expected_urls": len(expected),
        "actual_urls": len(actual),
        "issues": issues,
        "pass": not issues,
    }

def metadata_source_result() -> dict[str, Any]:
    p = load_json("qc-metadata-og-report/metadata-og-audit.json") or {}
    s = p.get("summary", {}) if isinstance(p, dict) else {}
    return {
        "name": "source_metadata_og_94",
        "report": "qc-metadata-og-report/metadata-og-audit.json",
        "report_summary": s,
        "pass": bool(s.get("overall_pass")),
    }

def git_diff_clean(path: str) -> dict[str, Any]:
    proc = subprocess.run(
        ["git","diff","--quiet","--",path],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    diff = ""
    if proc.returncode != 0:
        d = subprocess.run(
            ["git","diff","--",path],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        diff = d.stdout[-12000:]
        (LOGS/"keyword_map_drift.diff").write_text(diff, encoding="utf-8")
    return {
        "name": "keyword_map_no_drift_after_sync",
        "path": path,
        "exit_code": proc.returncode,
        "pass": proc.returncode == 0,
        "diff_log": "logs/keyword_map_drift.diff" if diff else None,
    }

def main() -> int:
    started = datetime.now(timezone.utc)
    checks: list[dict[str, Any]] = []

    checks.append(source_inventory_check())

    checks.append(run(
        "keyword_map_source_sync",
        ["python3",".github/scripts/sync_keyword_map.py"],
        "qc-keyword-map-report/keyword-map-sync-report.json",
        True,
    ))
    checks.append(git_diff_clean("seo/keyword-map.json"))

    run_meta = run(
        "source_metadata_og_audit",
        ["python3",".github/scripts/audit_metadata_og.py"],
        "qc-metadata-og-report/metadata-og-audit.json",
        False,
    )
    # audit_metadata_og.py is intentionally read-only and historically exits 0;
    # enforce its own summary explicitly.
    meta = metadata_source_result()
    meta["command_exit_code"] = run_meta["exit_code"]
    meta["duration_seconds"] = run_meta["duration_seconds"]
    checks.append(meta)

    checks.append(run("ayat_ownership_source", ["python3",".github/scripts/ayat_ownership_qc.py"]))
    checks.append(run("quran_progress_source", ["python3",".github/scripts/quran_progress_qc.py"]))

    checks.append(run(
        "live_103_url_crawl",
        ["python3",".github/scripts/live_crawl_qc.py"],
        "qc-live-report/live-crawl-report.json",
        True,
    ))
    checks.append(run(
        "live_hreflang_94",
        ["python3",".github/scripts/live_hreflang_qc.py"],
        "qc-live-hreflang-report/live-hreflang-report.json",
        True,
    ))
    checks.append(run(
        "live_keyword_map_94",
        ["python3",".github/scripts/live_keyword_map_qc.py"],
        "qc-live-keyword-map-report/live-keyword-map-report.json",
        True,
    ))
    checks.append(run(
        "live_metadata_og_94",
        ["python3",".github/scripts/live_metadata_og_qc.py"],
        "qc-live-metadata-og-report/live-metadata-og-report.json",
        True,
    ))
    checks.append(run(
        "live_reflection_og_94",
        ["python3",".github/scripts/live_reflection_og_qc.py"],
        "qc-live-reflection-og-report/live-reflection-og-report.json",
        True,
    ))
    checks.append(run(
        "live_schema_94",
        ["python3",".github/scripts/live_schema_qc.py"],
        "qc-live-schema-report/live-schema-report.json",
        True,
    ))
    checks.append(run(
        "live_internal_links_94",
        ["python3",".github/scripts/live_internal_links_qc.py"],
        "qc-live-internal-links-report/live-internal-link-parity-report.json",
        True,
    ))
    checks.append(run(
        "live_post_dedup_serp_12",
        ["python3",".github/scripts/live_post_dedup_serp_qc.py"],
        ".github/qc-state/post-dedup-serp/latest.json",
        True,
    ))
    checks.append(run(
        "live_reader_regression",
        ["node",".github/scripts/live_reader_regression.mjs"],
        "qc-live-reader-report/live-reader-regression-report.json",
        False,
    ))
    # Reader report uses summary.overallPass (capital P).
    reader = checks[-1]
    robj = load_json("qc-live-reader-report/live-reader-regression-report.json") or {}
    rsum = robj.get("summary", {}) if isinstance(robj, dict) else {}
    reader["report_summary"] = rsum
    reader["pass"] = reader["exit_code"] == 0 and bool(rsum.get("overallPass"))

    checks.append(run(
        "live_homepage_progress",
        ["node",".github/scripts/live_homepage_progress_qc.mjs"],
        ".github/qc-state/homepage-live/latest.json",
        False,
    ))
    homepage = checks[-1]
    hobj = load_json(".github/qc-state/homepage-live/latest.json") or {}
    homepage["report_summary"] = {
        "overall_pass": bool(hobj.get("overallPass")),
        "propagated": hobj.get("propagated"),
        "profiles": len(hobj.get("profiles") or []),
        "expected": hobj.get("expected"),
    }
    homepage["pass"] = homepage["exit_code"] == 0 and bool(hobj.get("overallPass"))

    finished = datetime.now(timezone.utc)
    failures = [x for x in checks if not x.get("pass")]
    overall = not failures

    result = {
        "gate": "TadabburLife Final Release Gate v1.0",
        "tested_commit": TESTED_SHA,
        "generated_at_utc": finished.isoformat(),
        "duration_seconds": round((finished-started).total_seconds(),2),
        "checks_total": len(checks),
        "checks_pass": sum(bool(x.get("pass")) for x in checks),
        "checks_fail": len(failures),
        "overall_pass": overall,
        "release_status": "GREEN" if overall else "BLOCKED",
        "checks": checks,
    }
    (OUT/"latest.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    lines = [
        "# TadabburLife — Final Release Gate v1.0","",
        f"- Tested commit: `{TESTED_SHA or 'local'}`",
        f"- Generated: {result['generated_at_utc']}",
        f"- Duration: {result['duration_seconds']} s",
        f"- Checks: {result['checks_pass']} / {result['checks_total']} PASS",
        f"- Release status: **{result['release_status']}**","",
        "| Gate | Result |",
        "|---|---:|",
    ]
    for x in checks:
        lines.append(f"| {x['name']} | {'PASS' if x.get('pass') else 'FAIL'} |")
    if failures:
        lines += ["","## Blocking failures",""]
        for x in failures:
            detail = x.get("issues") or x.get("report_summary") or x.get("exit_code")
            lines.append(f"- **{x['name']}** — {json.dumps(detail,ensure_ascii=False)}")
    else:
        lines += [
            "",
            "## Release decision",
            "",
            "**GREEN — website-side technical release gate passed.**",
            "",
            "The published 001–047 bilingual corpus is technically ready to proceed to Search Console indexing operations and the already-approved AdSense account-side submission/setup sequence.",
        ]
    (OUT/"SUMMARY.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    print("\n=== FINAL RELEASE GATE v1.0 ===")
    print(json.dumps({
        "tested_commit":TESTED_SHA,
        "checks_pass":result["checks_pass"],
        "checks_total":result["checks_total"],
        "release_status":result["release_status"],
        "failures":[x["name"] for x in failures],
    },indent=2))
    return 0 if overall else 1

if __name__=="__main__":
    sys.exit(main())
