#!/usr/bin/env python3
"""Run headless Chrome against a local branch preview at mobile widths."""
from pathlib import Path
import os, subprocess, sys, threading, tempfile
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
            if width == 390:
                # PDF prints the full document, including below-the-fold content.
                pdf = OUT / f"session049-{lang}-fullpage.pdf"
                pdf_cmd = [chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
                           "--disable-dev-shm-usage", "--no-pdf-header-footer",
                           f"--window-size={width},844", f"--print-to-pdf={pdf}",
                           "--virtual-time-budget=1500", url]
                pdf_result = subprocess.run(pdf_cmd, capture_output=True, text=True, timeout=45)
                if pdf_result.returncode or not pdf.exists() or pdf.stat().st_size < 5000:
                    failures.append(f"{lang} full-document PDF failed: {pdf_result.stderr[-300:]}")
                else:
                    print(f"Full document: {pdf.relative_to(ROOT)} ({pdf.stat().st_size} bytes)")
finally:
    pass
# Interactive navigation smoke test in the same local origin.
# Use real anchor clicks in Chrome rather than relying only on static href existence.
test_html = r'''<!doctype html><meta charset="utf-8"><title>Navigation smoke</title>
<pre id="results">RUNNING</pre><iframe id="view" style="width:390px;height:700px"></iframe>
<script>
(async()=>{
const cases=[
["/tadabbur/049/","/en/tadabbur/049/"],
["/en/tadabbur/049/","/tadabbur/049/"],
["/tadabbur/049/","/tadabbur/010/"],
["/en/tadabbur/049/","/en/tadabbur/010/"],
["/tadabbur/049/","/privacy/"],
["/en/tadabbur/049/","/contact/"],
["/tadabbur/049/","/?session=49&lang=id"],
["/en/tadabbur/049/","/?session=49&lang=en"]
];
let errors=[];
for(const [from,to] of cases){
 const iframe=document.querySelector("#view");
 await new Promise((resolve,reject)=>{
  const timer=setTimeout(()=>reject(Error("source timeout "+from)),6000);
  iframe.onload=()=>{clearTimeout(timer);resolve()};
  iframe.src=from;
 }).catch(e=>errors.push(e.message));
 const doc=iframe.contentDocument;
 const anchor=[...doc.querySelectorAll("a[href]")].find(a=>a.pathname===new URL(to,location.href).pathname && a.search===new URL(to,location.href).search);
 if(!anchor){errors.push("missing link "+from+" -> "+to);continue}
 try{
  await new Promise((resolve,reject)=>{
   const timer=setTimeout(()=>reject(Error("click timeout "+from+" -> "+to)),6000);
   iframe.onload=()=>{clearTimeout(timer);resolve()};
   anchor.click();
  });
  if(iframe.contentWindow.location.pathname!==new URL(to,location.href).pathname)
    errors.push("wrong destination "+from+" -> "+to);
 }catch(e){errors.push(e.message)}
}
document.querySelector("#results").textContent=errors.length?"NAV_FAIL: "+errors.join(" | "):"NAV_PASS: "+cases.length+" real browser anchor clicks";
})();
</script>'''
harness=ROOT/"mobile-preview-artifacts"/"navigation-smoke.html"
harness.write_text(test_html,encoding="utf-8")
url=f"http://127.0.0.1:{server.server_port}/mobile-preview-artifacts/navigation-smoke.html"
cmd=[chrome,"--headless=new","--no-sandbox","--disable-gpu","--disable-dev-shm-usage",
     "--virtual-time-budget=45000","--dump-dom",url]
result=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
if "NAV_PASS: 8 real browser anchor clicks" not in result.stdout:
    failures.append("Navigation click smoke failed: "+result.stdout[-1500:])
else:
    print("Interactive navigation PASS: 8 browser anchor clicks")
server.shutdown()
if failures:
    print("\n".join(failures),file=sys.stderr)
    sys.exit(1)
print("Mobile screenshot generation PASS (visual inspection of artifacts still required)")
