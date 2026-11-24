const SOURCE_BASE = "https://raw.githubusercontent.com/wiztechid/Master-tadabbur/worker-migration-staging/";
const ROOT_FILES = new Set([
  "index.html", "robots.txt", "sitemap.xml", "ads.txt", "favicon.ico",
  "favicon-16.png", "favicon-32.png", "favicon-192.png", "favicon-512.png",
  "apple-touch-icon.png",
]);
const LEGAL = new Set(["about", "contact", "cookies", "disclaimer", "privacy", "terms"]);
const MODULES = new Set([
  "sessions-001-017.html", "sessions-018-032.html", "sessions-033-034.html",
  "sessions-035-051.html", "sessions-035-051-part2.html",
  "sessions-035-051-part3.html", "sessions-035-051-part4.html",
]);
function assetPath(pathname) {
  let path;
  try { path = decodeURIComponent(pathname).replace(/^\/+/, ""); }
  catch { return null; }
  if (!path || path === "index.html") return "index.html";
  if (ROOT_FILES.has(path)) return path;
  if (LEGAL.has(path.replace(/\/$/, "")) && pathname.endsWith("/")) return path.replace(/\/$/, "") + "/index.html";
  if (/^(?:en\/)?tadabbur\/$/.test(path) && pathname.endsWith("/")) return path + "index.html";
  if (/^(?:en\/)?tadabbur\/\d{3}\/$/.test(path) && pathname.endsWith("/")) return path + "index.html";
  if (/^(?:en\/)?tadabbur\/\d{3}$/.test(path)) return "__redirect__";
  if (LEGAL.has(path) || /^(?:en\/)?tadabbur$/.test(path)) return "__redirect__";
  if (/^assets\/css\/session-landing-v1\.css$/.test(path)) return path;
  if (/^og\/reflection\/(?:id|en)\/\d{3}\.png$/.test(path)) return path;
  if (path === "data/quran-progress.json" || (path.startsWith("data/") && MODULES.has(path.slice(5)))) return path;
  return null;
}
function contentType(path) {
  if (path.endsWith(".html")) return "text/html; charset=utf-8";
  if (path.endsWith(".css")) return "text/css; charset=utf-8";
  if (path.endsWith(".json")) return "application/json; charset=utf-8";
  if (path.endsWith(".xml")) return "application/xml; charset=utf-8";
  if (path.endsWith(".txt")) return "text/plain; charset=utf-8";
  if (path.endsWith(".png")) return "image/png";
  if (path.endsWith(".ico")) return "image/x-icon";
  return "application/octet-stream";
}
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed", { status: 405, headers: { allow: "GET, HEAD" } });
    }
    const path = assetPath(url.pathname);
    if (path === "__redirect__") {
      return Response.redirect(url.origin + url.pathname.replace(/\/$/, "") + "/" + url.search, 308);
    }
    if (!path) return new Response("Not found", { status: 404, headers: { "x-robots-tag": "noindex" } });

    const cacheUrl = new URL(url.pathname, url.origin);
    const cacheKey = new Request(cacheUrl.toString(), { method: "GET" });
    const cached = await caches.default.match(cacheKey);
    if (cached) return request.method === "HEAD" ? new Response(null, cached) : cached;

    const upstream = await fetch(SOURCE_BASE + path, { redirect: "manual" });
    if (!upstream.ok) return new Response("Not found", { status: upstream.status === 404 ? 404 : 502 });
    const headers = new Headers({
      "content-type": contentType(path),
      "cache-control": "public, max-age=0, s-maxage=300",
      "x-robots-tag": "noindex, nofollow",
      "x-content-type-options": "nosniff",
    });
    const response = new Response(request.method === "HEAD" ? null : upstream.body, { status: 200, headers });
    if (request.method === "GET") ctx.waitUntil(caches.default.put(cacheKey, response.clone()));
    return response;
  },
};
