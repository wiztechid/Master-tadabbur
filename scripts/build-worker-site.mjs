import { cp, mkdir, readdir, rm, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.join(root, "dist");

const rootFiles = [
  "index.html",
  "robots.txt",
  "sitemap.xml",
  "ads.txt",
  "favicon.ico",
  "favicon-16.png",
  "favicon-32.png",
  "favicon-192.png",
  "favicon-512.png",
  "apple-touch-icon.png",
];

const publicDirectories = [
  "about",
  "contact",
  "cookies",
  "disclaimer",
  "privacy",
  "terms",
  "tadabbur",
  "en/tadabbur",
  "assets",
  "og/reflection",
];

async function exists(target) {
  try {
    await stat(target);
    return true;
  } catch {
    return false;
  }
}

async function copyDirectory(relativePath) {
  const source = path.join(root, relativePath);
  if (await exists(source)) {
    await cp(source, path.join(output, relativePath), { recursive: true });
  }
}

await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });

for (const file of rootFiles) {
  const source = path.join(root, file);
  if (await exists(source)) {
    await cp(source, path.join(output, file));
  }
}

for (const directory of publicDirectories) {
  await copyDirectory(directory);
}

const dataOutput = path.join(output, "data");
await mkdir(dataOutput, { recursive: true });
const dataSource = path.join(root, "data");
for (const file of await readdir(dataSource)) {
  if (file === "quran-progress.json" || /^sessions-.*\.html$/.test(file)) {
    await cp(path.join(dataSource, file), path.join(dataOutput, file));
  }
}

const required = [
  "index.html",
  "robots.txt",
  "sitemap.xml",
  "ads.txt",
  "assets/css/session-landing-v1.css",
  "data/quran-progress.json",
  "data/sessions-001-017.html",
  "data/sessions-018-032.html",
  "data/sessions-033-034.html",
  "data/sessions-035-051.html",
  "data/sessions-035-051-part2.html",
  "data/sessions-035-051-part3.html",
  "data/sessions-035-051-part4.html",
  "about/index.html",
  "contact/index.html",
  "cookies/index.html",
  "disclaimer/index.html",
  "privacy/index.html",
  "terms/index.html",
  ...Array.from({ length: 51 }, (_, i) => String(i + 1).padStart(3, "0"))
    .flatMap((session) => [
      `tadabbur/${session}/index.html`,
      `en/tadabbur/${session}/index.html`,
    ]),
];
for (const file of required) {
  if (!(await exists(path.join(output, file)))) {
    throw new Error(`Required public asset missing: ${file}`);
  }
}

const forbidden = [
  "mastersoptadabbur.md",
  "CURRENT-STATUS.md",
  "CHANGELOG.md",
  "CNAME",
  "seo",
  "Tadabbur_AlQuran_Master_Sesi_001-019_OWNER_V22-1.html",
  "Tadabbur_AlQuran_Master_Sesi_001-019_PUBLIC_V22.html",
  "index_fixed.html",
  "owner_index_fixed.html",
  "data/ayat-ownership.json",
  "data/session-049-draft.html",
  "data/session-050-draft.html",
  "data/session-051-draft.html",
  "owner",
  ".github",
  "docs",
];
for (const file of forbidden) {
  if (await exists(path.join(output, file))) {
    throw new Error(`Private or source-only file leaked into dist: ${file}`);
  }
}

let fileCount = 0;
let totalBytes = 0;
async function measure(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      await measure(fullPath);
    } else {
      fileCount++;
      totalBytes += (await stat(fullPath)).size;
    }
  }
}
await measure(output);

console.log(
  `Built ${fileCount} public files (${(totalBytes / 1024 / 1024).toFixed(2)} MiB); private SOP, SEO governance, owner data, and drafts excluded.`,
);
