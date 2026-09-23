import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT = process.cwd();
const OUT = path.join(ROOT, '.github', 'qc-state', 'homepage-live');
fs.mkdirSync(OUT, { recursive: true });

const progressData = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'quran-progress.json'), 'utf8'));

function expandRef(ref) {
  const m = String(ref).match(/^(\d+):(\d+)(?:-(\d+))?$/);
  if (!m) throw new Error('Invalid ayat ref: ' + ref);
  const s = Number(m[1]), a = Number(m[2]), b = Number(m[3] || m[2]);
  return Array.from({ length: b - a + 1 }, (_, i) => `${s}:${a + i}`);
}

const seen = new Set();
let ownedAyatOccurrences = 0;
let crossReferenceOccurrences = 0;
for (const session of progressData.sessions || []) {
  for (const ref of session.ayat || []) {
    const verses = expandRef(ref);
    ownedAyatOccurrences += verses.length;
    verses.forEach(v => seen.add(v));
  }
  for (const cross of session.crossReferences || []) {
    crossReferenceOccurrences += expandRef(cross.ayat).length;
  }
}
const expected = {
  discussed: seen.size,
  total: Number(progressData.quranTotalAyat),
  sessions: (progressData.sessions || []).length,
};
expected.pct = expected.discussed / expected.total * 100;
expected.idText = `${expected.discussed} dari ${new Intl.NumberFormat('id-ID').format(expected.total)} ayat • ${new Intl.NumberFormat('id-ID',{minimumFractionDigits:1,maximumFractionDigits:1}).format(expected.pct)}% cakupan Al-Qur'an`;
expected.enText = `${expected.discussed} of ${new Intl.NumberFormat('en-US').format(expected.total)} verses • ${new Intl.NumberFormat('en-US',{minimumFractionDigits:1,maximumFractionDigits:1}).format(expected.pct)}% Qur’an coverage`;

const profiles = [
  { name: 'desktop-id', width: 1440, height: 1100, lang: 'id' },
  { name: 'tablet-id', width: 1024, height: 1200, lang: 'id' },
  { name: 'mobile-id', width: 390, height: 844, lang: 'id' },
  { name: 'desktop-en', width: 1440, height: 1100, lang: 'en' },
  { name: 'mobile-en', width: 390, height: 844, lang: 'en' },
];

const browser = await chromium.launch({ headless: true });
const report = {
  generatedAt: new Date().toISOString(),
  url: 'https://tadabburlife.com/',
  expected: {
    ...expected,
    schemaVersion: progressData.schemaVersion,
    countMode: progressData.countMode,
    ownedAyatOccurrences,
    crossReferenceOccurrences,
    totalReferenceOccurrences: ownedAyatOccurrences + crossReferenceOccurrences,
  },
  propagationAttempts: 0,
  propagated: false,
  profiles: [],
  overallPass: false,
};

async function liveHasExpected() {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  try {
    await page.goto('https://tadabburlife.com/?qc=' + Date.now(), { waitUntil: 'networkidle', timeout: 30000 });
    const txt = (await page.locator('#quran-progress-text').textContent({ timeout: 5000 }).catch(() => ''))?.trim() || '';
    return txt === expected.idText;
  } catch {
    return false;
  } finally {
    await ctx.close();
  }
}

for (let i = 1; i <= 12; i++) {
  report.propagationAttempts = i;
  if (await liveHasExpected()) {
    report.propagated = true;
    break;
  }
  if (i < 12) await new Promise(r => setTimeout(r, 20000));
}

for (const profile of profiles) {
  const context = await browser.newContext({ viewport: { width: profile.width, height: profile.height } });
  const page = await context.newPage();
  const consoleErrors = [];
  const pageErrors = [];
  page.on('console', msg => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });
  page.on('pageerror', err => pageErrors.push(String(err)));

  const row = {
    name: profile.name,
    viewport: { width: profile.width, height: profile.height },
    language: profile.lang,
    status: null,
    checks: {},
    consoleErrors,
    pageErrors,
    pass: false,
  };

  try {
    const response = await page.goto('https://tadabburlife.com/?qc=' + Date.now(), { waitUntil: 'networkidle', timeout: 30000 });
    row.status = response?.status() ?? null;
    if (profile.lang === 'en') {
      await page.locator('[data-lang-btn="en"]').click();
      await page.waitForTimeout(250);
    } else {
      await page.locator('[data-lang-btn="id"]').click();
      await page.waitForTimeout(250);
    }

    const expectedText = profile.lang === 'en' ? expected.enText : expected.idText;
    const actualText = (await page.locator('#quran-progress-text').textContent())?.trim() || '';
    const statAyat = (await page.locator('#stat-ayat').textContent())?.trim() || '';
    const statTotal = (await page.locator('#stat-total').textContent())?.trim() || '';
    const statSessions = (await page.locator('#stat-sessions').textContent())?.trim() || '';
    const docLang = await page.locator('html').getAttribute('lang');
    const topState = async () => page.locator('.top').evaluate(el => {
      const s = getComputedStyle(el);
      return {
        showClass: el.classList.contains('show'),
        opacity: Number(s.opacity),
        visibility: s.visibility,
        pointerEvents: s.pointerEvents,
      };
    });
    const topAtStart = await topState();
    await page.evaluate(() => window.scrollTo(0, 500));
    await page.waitForTimeout(300);
    const topAfter400 = await topState();
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(300);
    const topAfterReturn = await topState();
    const metrics = await page.evaluate(() => {
      const bar = document.querySelector('#quran-progress-bar');
      const track = bar?.parentElement;
      const hero = document.querySelector('.hero');
      const stats = document.querySelector('.stats');
      const bb = bar?.getBoundingClientRect();
      const tb = track?.getBoundingClientRect();
      const hb = hero?.getBoundingClientRect();
      const sb = stats?.getBoundingClientRect();
      return {
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
        barWidth: bb?.width ?? 0,
        trackWidth: tb?.width ?? 0,
        heroWidth: hb?.width ?? 0,
        statsWidth: sb?.width ?? 0,
      };
    });
    const expectedRatio = expected.pct / 100;
    const actualRatio = metrics.trackWidth ? metrics.barWidth / metrics.trackWidth : 0;

    row.checks = {
      http200: row.status === 200,
      progressText: actualText === expectedText,
      discussedAyat: statAyat === String(expected.discussed),
      totalAyat: statTotal.replace(/[.,]/g, '') === String(expected.total),
      sessions: statSessions === String(expected.sessions),
      htmlLang: docLang === (profile.lang === 'en' ? 'en' : 'id'),
      topHiddenAtStart: !topAtStart.showClass && topAtStart.opacity === 0 && topAtStart.visibility === 'hidden' && topAtStart.pointerEvents === 'none',
      topVisibleAfter400: topAfter400.showClass && topAfter400.opacity > 0.95 && topAfter400.visibility === 'visible' && topAfter400.pointerEvents === 'auto',
      topHiddenAfterReturn: !topAfterReturn.showClass && topAfterReturn.opacity === 0 && topAfterReturn.visibility === 'hidden' && topAfterReturn.pointerEvents === 'none',
      noHorizontalOverflow: metrics.scrollWidth <= metrics.clientWidth + 1,
      progressBarRatio: Math.abs(actualRatio - expectedRatio) < 0.002,
      heroVisible: metrics.heroWidth > 0,
      statsVisible: metrics.statsWidth > 0,
      noConsoleErrors: consoleErrors.length === 0,
      noPageErrors: pageErrors.length === 0,
    };
    row.metrics = { ...metrics, expectedRatio, actualRatio, topAtStart, topAfter400, topAfterReturn };
    row.actualText = actualText;
    row.pass = Object.values(row.checks).every(Boolean);

    await page.screenshot({
      path: path.join(OUT, profile.name + '.png'),
      fullPage: true,
    });
  } catch (err) {
    row.error = String(err?.stack || err);
  } finally {
    report.profiles.push(row);
    await context.close();
  }
}

await browser.close();
report.overallPass = report.propagated && report.profiles.every(x => x.pass);
fs.writeFileSync(path.join(OUT, 'latest.json'), JSON.stringify(report, null, 2) + '\n');

const md = [
  '# TadabburLife Live Homepage Progress QC',
  '',
  `Generated: ${report.generatedAt}`,
  `Propagation: ${report.propagated ? 'PASS' : 'FAIL'} after ${report.propagationAttempts} attempt(s)`,
  `Expected: ${expected.idText}`,
  `Supporting sessions: ${expected.sessions}`,
  `Owned ayat / unique: ${ownedAyatOccurrences} / ${expected.discussed}`,
  `Cross-reference occurrences: ${crossReferenceOccurrences}`,
  `Total historical reference occurrences represented: ${ownedAyatOccurrences + crossReferenceOccurrences}`,
  '',
  '| Profile | HTTP | Progress | Stats | ↑ Scroll | Overflow | Bar | Errors | Result |',
  '|---|---:|---:|---:|---:|---:|---:|---:|---:|',
  ...report.profiles.map(r => `| ${r.name} | ${r.checks.http200?'PASS':'FAIL'} | ${r.checks.progressText?'PASS':'FAIL'} | ${r.checks.discussedAyat&&r.checks.totalAyat&&r.checks.sessions?'PASS':'FAIL'} | ${r.checks.topHiddenAtStart&&r.checks.topVisibleAfter400&&r.checks.topHiddenAfterReturn?'PASS':'FAIL'} | ${r.checks.noHorizontalOverflow?'PASS':'FAIL'} | ${r.checks.progressBarRatio?'PASS':'FAIL'} | ${r.checks.noConsoleErrors&&r.checks.noPageErrors?'PASS':'FAIL'} | ${r.pass?'PASS':'FAIL'} |`),
  '',
  `**Overall: ${report.overallPass ? 'PASS' : 'FAIL'}**`,
  ''
].join('\n');
fs.writeFileSync(path.join(OUT, 'SUMMARY.md'), md);

console.log(JSON.stringify(report, null, 2));
process.exit(report.overallPass ? 0 : 1);
