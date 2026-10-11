import { chromium } from "playwright";

const base = (process.env.BASE_URL || "https://tadabburlife.com").replace(/\/$/, "");
const session = String(process.env.SESSION || "48").padStart(3, "0");
const n = Number(session);

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

async function assertOk(response, label) {
  assert(response, label + ": no response");
  assert(response.status() < 400, label + ": HTTP " + response.status());
}

async function gotoReader(page, lang = "id") {
  const response = await page.goto(base + "/?session=" + n + "&lang=" + lang, { waitUntil: "domcontentloaded" });
  await assertOk(response, "reader " + lang);
  const active = lang === "en" ? "#en-s" + n + ".active" : "#s" + n + ".active";
  await page.locator(active).waitFor({ state: "visible", timeout: 15000 });
  return active;
}

async function checkInternalLinks(page, context, path, label, expectedCanonical) {
  await assertOk(await page.goto(base + path, { waitUntil: "domcontentloaded" }), label);
  assert(await page.locator("h1").count() === 1, label + " must have exactly one H1");
  const canonical = await page.locator('link[rel="canonical"]').getAttribute("href");
  assert(canonical === expectedCanonical, label + " canonical mismatch: " + canonical);
  const robots = (await page.locator('meta[name="robots"]').getAttribute("content").catch(() => "")) || "";
  assert(!/noindex/i.test(robots), label + " unexpectedly contains noindex");

  const urls = await page.locator("a[href]").evaluateAll((nodes, origin) => {
    const out = [];
    for (const a of nodes) {
      const raw = a.getAttribute("href");
      if (!raw || raw.startsWith("#") || raw.startsWith("mailto:") || raw.startsWith("javascript:")) continue;
      const u = new URL(raw, origin);
      if (u.origin === origin) out.push(u.href.split("#")[0]);
    }
    return [...new Set(out)];
  }, base);

  for (const url of urls) {
    const response = await context.request.get(url, { failOnStatusCode: false, timeout: 15000 });
    assert(response.status() < 400, label + " broken link " + url + " -> HTTP " + response.status());
  }
  return urls.length;
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext();
const page = await context.newPage();

try {
  // Load the requested Indonesian reader session.
  let active = await gotoReader(page, "id");
  assert((await page.locator(active + " .session-head h2").innerText()).length > 10, "Session title missing");

  const totalText = await page.locator("#stat-sessions").innerText();
  const total = Number(totalText.replace(/[^0-9]/g, ""));
  assert(Number.isFinite(total) && total >= n, "Invalid total session count: " + totalText);

  // Navigation semantics: latest gets a plain status label; older sessions get a real Next button.
  if (n === total) {
    assert(await page.locator(active + " .session-nav .session-end").count() === 1, "Latest-session status label missing");
    assert(await page.locator(active + ' .session-nav button:has-text("' + session + ' →")').count() === 0, "Inactive latest-session button still visible");
  } else {
    const nextLabel = String(n + 1).padStart(3, "0") + " →";
    const next = page.locator(active + " .session-nav button").filter({ hasText: nextLabel });
    assert(await next.count() === 1, "Next-session button missing for non-latest session");
    await next.click();
    await page.locator("#s" + (n + 1) + ".active").waitFor({ state: "visible" });
    active = await gotoReader(page, "id");
  }

  // Previous navigation when applicable.
  if (n > 1) {
    const prev = page.locator(active + " .session-nav button").filter({ hasText: "← " + String(n - 1).padStart(3, "0") });
    assert(await prev.count() === 1, "Previous-session button missing");
    await prev.click();
    await page.locator("#s" + (n - 1) + ".active").waitFor({ state: "visible" });
    active = await gotoReader(page, "id");
  }

  // Middle Journey/Daftar control returns to index view.
  const middle = page.locator(active + " .session-nav button").filter({ hasText: "Daftar" });
  assert(await middle.count() === 1, "Journey/Daftar button missing");
  await middle.click();
  await page.locator("#home").waitFor({ state: "visible" });
  assert(await page.locator(active).isHidden(), "Session remained visible after Journey/Daftar");
  active = await gotoReader(page, "id");

  // Language controls.
  await page.locator('button[data-lang-btn="en"]').click();
  await page.locator("#en-s" + n + ".active").waitFor({ state: "visible" });
  await page.locator('button[data-lang-btn="id"]').click();
  await page.locator("#s" + n + ".active").waitFor({ state: "visible" });
  active = "#s" + n + ".active";

  // Continue returns to the current/last session.
  await page.locator('button[onclick="goLast()"]').click();
  await page.locator(active).waitFor({ state: "visible" });

  // Mission view.
  await page.locator('button[onclick="missionView()"]').click();
  await page.locator("#missionView.active-view").waitFor({ state: "visible" });
  await gotoReader(page, "id");
  active = "#s" + n + ".active";

  // Focus mode toggles.
  const focus = page.locator("button.focus-btn");
  await focus.click();
  assert(await page.locator("body").evaluate(el => el.classList.contains("focus-reading")), "Focus mode did not activate");
  await focus.click();
  assert(!(await page.locator("body").evaluate(el => el.classList.contains("focus-reading"))), "Focus mode did not deactivate");

  // Open All expands all details in the active session.
  await page.locator('button:has-text("Open All")').click();
  const visibleDetails = page.locator(active + " details");
  const detailCount = await visibleDetails.count();
  for (let i = 0; i < detailCount; i++) {
    assert(await visibleDetails.nth(i).evaluate(el => el.open), "Open All left a details element closed");
  }

  // Completion button changes state in this isolated browser context.
  const done = page.locator(active + " .finish-reflection-wrap button");
  assert(await done.count() === 1, "Completion button missing");
  await done.click();
  assert(await done.evaluate(el => el.classList.contains("done")), "Completion button did not enter done state");

  // Back-to-top must work.
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(250);
  const top = page.locator("button.top");
  await top.click();
  await page.waitForTimeout(500);
  assert(await page.evaluate(() => window.scrollY < 50), "Back-to-top did not return near page top");

  // Static bilingual pages: canonical/indexability + internal destinations.
  const idPath = "/tadabbur/" + session + "/";
  const enPath = "/en/tadabbur/" + session + "/";
  const idCanonical = base + idPath;
  const enCanonical = base + enPath;

  const idCount = await checkInternalLinks(page, context, idPath, "ID static", idCanonical);
  if (n > 1) assert(await page.locator('a[href="../' + String(n - 1).padStart(3, "0") + '/"]').count() >= 1, "ID static Previous link missing");
  assert(await page.locator('link[rel="alternate"][hreflang="en"]').getAttribute("href") === enCanonical, "ID hreflang EN mismatch");

  const enCount = await checkInternalLinks(page, context, enPath, "EN static", enCanonical);
  if (n > 1) assert(await page.locator('a[href="../' + String(n - 1).padStart(3, "0") + '/"]').count() >= 1, "EN static Previous link missing");
  assert(await page.locator('link[rel="alternate"][hreflang="id"]').getAttribute("href") === idCanonical, "EN hreflang ID mismatch");

  console.log("PASS TadabburLife manual UI smoke");
  console.log("Session:", session, "of", total);
  console.log("Checked static internal URLs:", idCount + enCount);
} finally {
  await browser.close();
}
