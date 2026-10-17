#!/usr/bin/env python3
"""Render representative bilingual landing pages and assert mobile overflow/navigation."""
from pathlib import Path
import os, subprocess, sys, threading
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
samples=(("id","tadabbur"),("en","en/tadabbur"))
sessions=("001","048","049")
# Actual headless Chrome renders both language variants at common narrow widths.
    for lang,root in samples:
        for session in sessions:
            path=f"{root}/{session}/"
            for width in (375,390):
                url=f"http://127.0.0.1:{server.server_port}/{path}"
                screenshot=OUT/f"session-{session}-{lang}-{width}.png"
                cmd=[chrome,"--headless=new","--no-sandbox","--disable-gpu","--disable-dev-shm-usage",
                     "--force-device-scale-factor=1",f"--window-size={width},844","--hide-scrollbars",
                     f"--screenshot={screenshot}","--virtual-time-budget=1500",url]
                result=subprocess.run(cmd,capture_output=True,text=True,timeout=45)
                if result.returncode or not screenshot.exists() or screenshot.stat().st_size<2000:
                    failures.append(f"{path} {width}px screenshot failed: {result.stderr[-300:]}")
                else:
                    print(f"Screenshot: {screenshot.relative_to(ROOT)} ({screenshot.stat().st_size} bytes)")
# In Chrome, each iframe is a real mobile viewport. Check its document dimensions directly.
overflow_html=r'''<!doctype html><meta charset="utf-8"><title>Mobile overflow QC</title>
<pre id="results">RUNNING</pre><div id="frames"></div><script>
(async()=>{
const cases=[];
for(const root of ["tadabbur","en/tadabbur"])
 for(const session of ["001","048","049"])
  for(const width of [375,390]) cases.push({root,session,width});
let errors=[];
for(const c of cases){
 const frame=document.createElement("iframe");
 frame.style.cssText="display:block;border:0;height:844px;width:"+c.width+"px";
 document.querySelector("#frames").append(frame);
 await new Promise((resolve,reject)=>{
  const timer=setTimeout(()=>reject(Error("load timeout "+c.root+"/"+c.session+" "+c.width)),12000);
  frame.onload=()=>{clearTimeout(timer);resolve()};
  frame.src="/"+c.root+"/"+c.session+"/";
 }).catch(e=>errors.push(e.message));
 try{
  const doc=frame.contentDocument, de=doc.documentElement, body=doc.body;
  const viewport=frame.contentWindow.innerWidth;
  const scroll=Math.max(de.scrollWidth,body.scrollWidth);
  const client=de.clientWidth;
  if(scroll>client+1) errors.push(c.root+"/"+c.session+" "+c.width+"px horizontal overflow "+scroll+">"+client);
  if(viewport!==c.width) errors.push(c.root+"/"+c.session+" expected viewport "+c.width+" got "+viewport);
 }catch(e){errors.push("inspect failed "+c.root+"/"+c.session+": "+e.message)}
 frame.remove();
}
document.querySelector("#results").textContent=errors.length?"OVERFLOW_FAIL: "+errors.join(" | "):"OVERFLOW_PASS: "+cases.length+" real mobile viewport checks";
})();</script>'''
harness=OUT/"mobile-overflow-smoke.html"
harness.write_text(overflow_html,encoding="utf-8")
url=f"http://127.0.0.1:{server.server_port}/mobile-preview-artifacts/mobile-overflow-smoke.html"
cmd=[chrome,"--headless=new","--no-sandbox","--disable-gpu","--disable-dev-shm-usage",
     "--virtual-time-budget=60000","--dump-dom",url]
result=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
if "OVERFLOW_PASS: 12 real mobile viewport checks" not in result.stdout:
    failures.append("Mobile overflow check failed: "+result.stdout[-1800:])
else:
    print("Horizontal overflow PASS: 12 real mobile viewport checks")
# Interactive navigation smoke test in the same local origin.
test_html=r'''<!doctype html><meta charset="utf-8"><title>Navigation smoke</title>
<pre id="results">RUNNING</pre><iframe id="view" style="width:390px;height:700px"></iframe><script>
(async()=>{
const cases=[
["/tadabbur/049/","/en/tadabbur/049/"],
["/en/tadabbur/049/","/tadabbur/049/"],
["/tadabbur/049/","/tadabbur/010/"],
["/en/tadabbur/049/","/en/tadabbur/010/"],
["/tadabbur/049/","/privacy/"],
["/en/tadabbur/049/","/contact/"],
["/tadabbur/049/","/?session=49&lang=id"],
["/en/tadabbur/049/","/?session=49&lang=en"]];
let errors=[];
for(const [from,to] of cases){
 const iframe=document.querySelector("#view");
 await new Promise((resolve,reject)=>{
  const timer=setTimeout(()=>reject(Error("source timeout "+from)),6000);
  iframe.onload=()=>{clearTimeout(timer);resolve()};iframe.src=from;
 }).catch(e=>errors.push(e.message));
 const doc=iframe.contentDocument;
 const anchor=[...doc.querySelectorAll("a[href]")].find(a=>a.pathname===new URL(to,location.href).pathname&&a.search===new URL(to,location.href).search);
 if(!anchor){errors.push("missing link "+from+" -> "+to);continue}
 try{
  await new Promise((resolve,reject)=>{
   const timer=setTimeout(()=>reject(Error("click timeout "+from+" -> "+to)),6000);
   iframe.onload=()=>{clearTimeout(timer);resolve()};anchor.click();
  });
  if(iframe.contentWindow.location.pathname!==new URL(to,location.href).pathname)errors.push("wrong destination "+from+" -> "+to);
 }catch(e){errors.push(e.message)}
}
document.querySelector("#results").textContent=errors.length?"NAV_FAIL: "+errors.join(" | "):"NAV_PASS: "+cases.length+" real browser anchor clicks";
})();</script>'''
nav=OUT/"navigation-smoke.html";nav.write_text(test_html,encoding="utf-8")
navurl=f"http://127.0.0.1:{server.server_port}/mobile-preview-artifacts/navigation-smoke.html"
cmd=[chrome,"--headless=new","--no-sandbox","--disable-gpu","--disable-dev-shm-usage","--virtual-time-budget=45000","--dump-dom",navurl]
result=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
if "NAV_PASS: 8 real browser anchor clicks" not in result.stdout:
    failures.append("Navigation click smoke failed: "+result.stdout[-1500:])
else:
    print("Interactive navigation PASS: 8 browser anchor clicks")
server.shutdown()
if failures:
    print("\\n".join(failures),file=sys.stderr);sys.exit(1)
print("Mobile screenshot generation and representative overflow regression PASS; visually inspect the uploaded screenshots.")
