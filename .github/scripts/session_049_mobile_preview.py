#!/usr/bin/env python3
"""Run headless Chrome against a local branch preview at mobile widths."""
from pathlib import Path
import os, re, subprocess, sys, tempfile, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"mobile-preview-artifacts"
OUT.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
os.chdir(ROOT)
server=ThreadingHTTPServer(("127.0.0.1",0),Quiet)
threading.Thread(target=server.serve_forever,daemon=True).start()
chrome=os.environ.get("CHROME_BIN","google-chrome")
failures=[]
try:
    for lang,path in (("id","tadabbur/049/"),("en","en/tadabbur/049/")):
        for width in (375,390):
            url=f"http://127.0.0.1:{server.server_port}/{path}"
            screenshot=OUT/f"session049-{lang}-{width}.png"
            # Chrome headless screenshot captures the actual rendered page, not source HTML.
            cmd=[chrome,"--headless=new","--no-sandbox","--disable-gpu","--disable-dev-shm-usage","--force-device-scale-factor=1",f"--window-size={width},844","--hide-scrollbars",f"--screenshot={screenshot}","--virtual-time-budget=1500",url]
            result=subprocess.run(cmd,capture_output=True,text=True,timeout=45)
            if result.returncode or not screenshot.exists() or screenshot.stat().st_size<2000:
                failures.append(f"{lang} {width}px screenshot failed: {result.stderr[-300:]}")
            else:
                print(f"Screenshot: {screenshot.relative_to(ROOT)} ({screenshot.stat().st_size} bytes)")
finally:
    server.shutdown()
if failures:
    print("\n".join(failures),file=sys.stderr)
    sys.exit(1)
print("Mobile screenshot generation PASS (visual inspection of artifacts still required)")
