# TadabburLife — Project Changelog

Records material verified changes to TadabburLife.

This document does not replace Git history. Routine commits, minor copy adjustments, and work that has not yet been implemented or verified are not recorded here.

---

## 2026-09-22

### [Domain / SEO] TadabburLife Custom-Domain Baseline
- Established `https://tadabburlife.com/` as the canonical public host for the active TadabburLife corpus.
- Verified 47 Indonesian + 47 English public session landings = **94 session-language targets**.
- Verified the repository sitemap inventory at **103 canonical public URLs**: homepage, ID/EN hubs, 94 session landings, and 6 public information/legal pages.
- Verified `robots.txt` allows public crawling, blocks `/owner/`, and references the custom-domain sitemap.
- Confirmed the 94 session landings have the source-level technical baseline for self-referencing canonical, reciprocal ID/EN hreflang, x-default, index/follow, title, meta description, and H1.

### [UI / Trust] Public Information & Legal Pages
- Restyled About, Privacy Policy, Cookie Policy, Terms, Disclaimer, and Contact to the TadabburLife visual system instead of plain browser-default HTML.
- Preserved bilingual Indonesian/English content while removing redundant ID/EN selector pills from those six pages.
- Removed small hero kicker labels such as “TENTANG PROYEK” from the six information pages for a cleaner visual hierarchy.
- Replaced the user-facing GitHub contact route with **`info@tadabburlife.com`** on the Contact page.
- Kept canonical, indexability, metadata, and structured-page signals intact during the visual update.

### [SEO / Technical] 94-Landing Schema Normalization — PASS
- Normalized structured data across all **94** Indonesian + English session landings.
- Standardized each landing to exactly one valid `Article` JSON-LD object and one valid `BreadcrumbList`.
- Standardized `headline`, `description`, `inLanguage`, canonical `url`, `mainEntityOfPage`, `author`, `publisher`, and `isPartOf`.
- Preserved existing `alternativeHeadline` and `keywords` when they were already present rather than inventing new editorial SEO data.
- Used a schema-only rewrite with a hard safety assertion that the entire page body remain byte-for-byte unchanged.
- Source QC verified **94 / 94 bodies unchanged**, **94 / 94 Article schemas valid**, **94 / 94 BreadcrumbList schemas valid**, and **0 JSON-LD parse errors**.
- GitHub Pages successfully deployed the normalized corpus.
- Live custom-domain schema QC verified **94 / 94 URLs HTTP 200** and **94 / 94 schema PASS**, with **0 failures**.
- Added reusable automation: `.github/scripts/normalize_schema.py`, `.github/workflows/normalize-schema.yml`, `.github/scripts/live_schema_qc.py`, and `.github/workflows/live-schema-qc.yml`.
- Marked **G3 Schema Normalization = PASS**.
- Moved active Green-Gate priority to **Internal-Link Parity → Keyword-Map ↔ Landing Sync**.

### [Technical / P0] Live 103-URL Crawl QC — PASS
- Added permanent public-network crawler at `.github/scripts/live_crawl_qc.py`.
- Added GitHub Actions workflow `.github/workflows/live-crawl-qc.yml` so the custom-domain crawl is repeatable and auditable.
- Verified the live sitemap contains **103 / 103** intended public URLs.
- Verified **103 / 103** sitemap URLs return HTTP **200**.
- Verified **0** sitemap-URL redirects.
- Verified **0** canonical mismatches/missing canonicals.
- Verified **0** `noindex` pages in the sitemap inventory.
- Verified **0** soft-404 suspects.
- Verified live `robots.txt` and `sitemap.xml` both return HTTP 200 and robots points to the custom-domain sitemap while blocking `/owner/`.
- Verified no stale `Master Tadabbur` branding or legacy `wiztechid.github.io/Master-tadabbur` URL issue was detected by the crawl checks.
- Verified Contact live output contains **`info@tadabburlife.com`** and no longer uses the old GitHub repository contact wording.
- Recorded public-run response-time observation of approximately **70 ms min / 130 ms median / 211 ms p95 / 336 ms max** across the 103 sitemap pages; this is not a Core Web Vitals measurement.
- Marked **P0 Live 103-URL Crawl QC = PASS**.
- Technical Green Gate remains open for remaining schema normalization, internal-link parity, keyword-map ↔ landing synchronization, and reader/live regression checks.

### [Technical / P0] Deploy Parity & Cache Verification
- Verified public-content checkpoint `c413b663031913a3661f33a492e303e3cc7490d3` completed a successful GitHub Pages deployment.
- Verified the generated `github-pages` artifact was built from the same SHA as that public-content checkpoint.
- Verified source ↔ deployment-artifact parity for critical public files/structure.
- Classified the earlier stale visual state as pre-final-deployment timing rather than a source/build mismatch.
- Marked **P0 Deploy Parity / Cache = PASS** for public HTML source → GitHub Pages artifact. Subsequent documentation-only commits do not alter that public-page parity checkpoint.
- Kept the overall Technical Green Gate open pending **live 103-URL custom-domain crawl QC** and remaining live regression checks.

### [Governance] Master SOP v1.2
- Added a dedicated **Deploy Parity / Cache QC** gate.
- Required repository source, deployment artifact, and live custom-domain state to be treated as separate verification layers.
- Added deploy-parity verification to the post-deploy workflow and Definition of Done.
- Explicitly prohibited rewriting correct source merely to chase stale browser/edge cache.

## 2026-09-20

### [Governance] Project Governance v1.0
- Added `mastersoptadabbur.md` v1.0 as FROZEN governance.
- Added `CURRENT-STATUS.md` v1.0 as the living project baseline.
- Established repository and live implementation verification as the authority for current implementation status.

### [Governance] Master SOP v1.1 — Sacred Source & SEO-Adaptive Content
- Established Quran text, surah/ayah references, approved Quran translation, and verified hadith text/references as an **Absolute Sacred Lock** against SEO or editorial optimization.
- Allowed verified factual/source corrections through a dedicated source-verification process rather than SEO rewriting.
- Established the explanatory layer as SEO-adaptive to independently validated bilingual keyword targets, search intent, and SERP opportunities.
- Defined reflection, key takeaway, Journey Mission, and practical action as **meaning-constrained** rather than freely SEO-adaptive.
- Established that semantic religious anchor parity is mandatory across languages while explanatory SEO parity is not.
- Added the **Religious Evidence Boundary**: search demand does not create religious evidence.
- Required substantive religious claims in explanatory content to have traceable evidentiary basis.
- Required weak-SERP opportunities to pass relevance, intent-fit, content-value, evidence, and cannibalization safeguards before targeting.

### [Corpus] Published Corpus Baseline
- Verified Sessions 001–047 as the published corpus.
- Verified 47 Indonesian and 47 English session landings.
- Established 94 session-language targets as the active corpus.
- Material beyond Session 047 remains outside the published corpus until publicly released and verified.

### [SEO] Deep Live SERP Validation — Sessions 001–004
- Completed bilingual Deep Live SERP validation.
- Aligned ID and EN metadata/H1 with their validated search territories.
- Maintained independent ID and EN targeting.

### [SEO] Deep Live SERP Validation — Sessions 005–008
- Completed deeper bilingual live-SERP validation.
- Refined search intent and metadata.
- Further narrowed Session 005 English targeting toward mocking people/offensive names to protect search territory.

### [SEO] Deep Live SERP Validation — Sessions 009–012
- Completed deeper bilingual live-SERP validation.
- Aligned ID and EN metadata with validated search territories.
- Applied cannibalization controls against adjacent sessions.

### [SEO] Architecture v1.1 Baseline Audit
- Verified bilingual canonical landing architecture.
- Verified ID/EN/x-default hreflang foundation.
- Verified sitemap and robots foundation.
- Verified bilingual keyword/search mapping through Session 047.
- Confirmed validation depth is not uniform across all 47 sessions.

### [Technical] 94-Landing Audit
- Identified English internal-link parity as a normalization gap.
- Identified structured-data inconsistency across landing generations.
- Identified metadata-quality inconsistency across the corpus.
- Established the evidence base for corpus-wide normalization.

### [Decision] Technical Green Gate
- Separated technical-integrity status from Deep SERP coverage.
- Technical integrity requires corpus-wide normalization, technical QC, and live regression verification.
- Deep SERP coverage remains independently tracked in `CURRENT-STATUS.md`.
