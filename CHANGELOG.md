# TadabburLife — Project Changelog

Records material verified changes to TadabburLife.

This document does not replace Git history. Routine commits, minor copy adjustments, and work that has not yet been implemented or verified are not recorded here.

---

## 2026-09-22

### [SEO] Deep Live SERP + Cannibalization — Sessions 013–016 — PASS
- Completed independent **Indonesian + English live-SERP research** for Sessions **013–016**.
- Advanced Deep Live SERP coverage from **12 / 47** to **16 / 47 sessions** = **32 / 94 session-language targets**.
- Upgraded `demand_evidence` for 013–016 ID + EN to `deep-live-serp-validated-2026-09-22`.
- Added explicit `search_territory` and `cannibalization_guard` fields to the bilingual keyword registry.
- Session **013** now owns **anger restraint + forgiveness** around Ali 'Imran/Quran 3:134; Session 014 retains speech/word-choice intent.
- Session **014** now owns **speaking what is best / avoiding discord** around Al-Isra/Quran 17:53; Session 013 retains anger-management intent.
- Session **015** now owns **unsupported suspicion → tajassus/fault-finding → backbiting** around Al-Hujurat/Quran 49:12. Session 005 remains mocking/offensive names, Session 011 news-before-sharing, and Session 042 information-before-decision.
- Session **016** now owns **nightly/daily muhasabah and self-accountability before sleep**. Session 030 retains the separate Al-Hashr/Quran 59:18 territory of preparing provision for the Hereafter.
- Updated evidence-backed title/H1/meta for all **8** ID/EN landings.
- Added exactly one concise reader-first direct-answer block to each of the eight landing pages.
- Preserved Quran/hadith sacred-source text and did not rewrite the locked reflection/practical-action meaning layer.
- Re-normalized Article/Breadcrumb schema and OG/Twitter metadata after the editorial SEO changes.
- Re-synchronized `seo/keyword-map.json` implementation snapshots.
- Updated keyword-map validators so the research boundary is now **001–016 Deep validated / 017–047 directional**.
- Added research record `seo/deep-serp-013-016-2026-09-22.md`.
- Added targeted live validator `.github/scripts/live_deep_serp_013_016_qc.py` and workflow `.github/workflows/live-deep-serp-013-016-qc.yml`.
- Final targeted live batch QC: **8 / 8 HTTP 200, 8 / 8 PASS, 0 failures** for title/H1/meta ↔ map, canonical, OG, Article schema, answer-block presence, evidence status, search territory, and cannibalization guard.
- Full post-batch registry QC also passed: **94 / 94 source implementation PASS**, **94 / 94 live map↔landing PASS**, **47 / 47 related parity**, **16 Deep / 31 directional**, and **0 research-boundary issues**.
- Active Deep SERP priority advances to **Sessions 017–020 bilingual**.

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

### [Reader / Regression] Live Reader Browser QC — PASS
- Added Chromium/Playwright browser regression at `.github/scripts/live_reader_regression.mjs` and `.github/workflows/live-reader-regression.yml`.
- Exercised the complete active reader corpus at **three viewports**: desktop, tablet, and mobile.
- Verified **94 / 94** session-language states on desktop, **94 / 94** on tablet, and **94 / 94** on mobile = **282 / 282** corpus viewport checks.
- Verified no tested horizontal-overflow regression and no browser console/page errors in the tested profiles.
- Fixed reader URL-state drift so session navigation and language switching synchronize the browser query/hash; refresh now preserves the current session/language.
- Journey/Mission views now clear stale session query state.
- Replaced the previous pseudo-random QR-like canvas with a standards-compliant QR encoder.
- Verified the generated ID and EN Reflection Card QR canvases by decoding them back to the exact interactive-reader deep links.
- Changed Reflection Card share filenames from legacy `master-tadabbur-...` to `tadabburlife-...`.
- Aligned Reflection Card share text to the canonical public session landing while preserving the QR as a direct interactive-reader deep link.
- Verified completion/read progress persistence, Journey Mission persistence, Focus Mode persistence, Previous/Next behavior, ID↔EN switching, and refresh behavior.
- Verified **8 / 8** representative public landing CTAs (Sessions 001, 013, 025, 047 × ID/EN) correctly enter the intended interactive reader state.
- Captured and visually reviewed representative desktop/tablet/mobile reader screenshots plus a Reflection Card screenshot.
- Marked **G7 Live Reader / Regression = PASS**.

### [SEO / Technical] Technical Green Gate — PASS
- Reconciled the accumulated evidence for G1–G7 and closed the TadabburLife technical-integrity Green Gate.
- G1 is explicitly scoped as **regression-integrity against the locked repository/content baseline**, not an independent theological re-verification of every religious source.
- G6 corpus-wide technical QC is closed using the 103-URL live crawl, 94-landing canonical/hreflang/indexability checks, internal-link parity, and static share/image validation.
- Current result: **SEO Architecture / Technical Integrity = PASS**.
- Deep SERP remains a separate research track; this technical PASS does **not** upgrade Sessions 013–047 from directional mapping to Deep SERP validation.
- Active priority now moves to **Deep Live SERP Batch 013–016 bilingual**.

### [Share / Visual] Reflection Card → 94 Branded OG Images — PASS
- Promoted **Reflection Card** to the single visual source of truth for session sharing.
- Added automated landscape social derivatives for the active corpus: **47 ID + 47 EN = 94 unique OG images**.
- Generated assets at `/og/reflection/{id|en}/{session}.png`.
- Standardized image format/dimensions to **PNG 1200×630** for crawler/social-preview compatibility.
- Reused the same Reflection Card data rules as the interactive reader: session title, reflection quote, Journey Mission/practical action, language, session number, and TadabburLife green/gold branding.
- Added `og:image`, `og:image:secure_url`, `og:image:type`, width/height, alt text, `twitter:image`, and Twitter image alt to all 94 landings.
- Upgraded Twitter/X cards from `summary` to **`summary_large_image`**.
- Verified all **94 landing pages HTTP 200**, all **94 image URLs HTTP 200**, all **94 files actual PNG 1200×630**, all **94 image URLs unique**, and **0 failures**.
- Verified generated image-size range at approximately **121 KB–188 KB**.
- Performed visual sample QC on **ID 001, EN 013, ID 025, EN 047**; hierarchy, crop safety, language/session identity, and brand rendering passed.
- Added generator/attachment/live-QC automation: `.github/scripts/generate_reflection_og.py`, `.github/scripts/attach_reflection_og.py`, `.github/workflows/generate-reflection-og.yml`, `.github/scripts/live_reflection_og_qc.py`, and `.github/workflows/live-reflection-og-qc.yml`.
- Updated existing metadata audit/live validators so Reflection Card OG images are now a required baseline.
- Marked **Reflection Card OG Image Coverage = PASS 94/94 source + live**.

### [Governance] Master SOP v1.3
- Defined Reflection Card as the canonical share-visual source of truth.
- Required static pre-rendered OG derivatives because social crawlers cannot depend on browser-side JavaScript rendering.
- Established the current share-image baseline as one unique **PNG 1200×630** asset per session-language pair.
- Required OG/Twitter image regeneration + corpus-wide/live QC whenever Reflection Card data or visual language changes materially.
- Explicitly prohibited creating new religious claims, reflection meaning, or practical actions only for social-card visuals.

### [SEO / Technical] Metadata Technical Integrity + OG/Share — PASS
- Audited all **94** Indonesian + English session landings for title, H1, meta description, canonical, language, Open Graph, Twitter/X, and schema synchronization.
- Initial audit found **50** landings missing Twitter/X summary metadata, **35** missing `og:site_name`, **11** Twitter-title mismatches, **12** Twitter-description mismatches, and **34** objectively truncated meta descriptions.
- Also repaired **8** objectively thin English meta descriptions.
- Standardized all 94 landings to `og:type=article`, `og:site_name=TadabburLife`, language-correct `og:locale`, H1-synchronized OG/Twitter titles, meta-synchronized OG/Twitter descriptions, canonical-synchronized `og:url`, and `twitter:card=summary`.
- Repaired broken/thin meta descriptions only from H2/paragraph text already present on the same page; no new search-intent positioning was invented.
- Updated `Article.headline` / `Article.description` schema in lockstep with repaired metadata.
- Re-synchronized `seo/keyword-map.json` implementation snapshots after metadata repair.
- Preserved session body content byte-for-byte: **94 / 94 bodies unchanged**.
- Source QC: **94 / 94 metadata/OG/share PASS**, **42 description repairs** total (**34 truncation + 8 thin**), **0 failures**.
- Live custom-domain QC: **94 / 94 HTTP 200**, **94 / 94 metadata/OG/share PASS**, **0 failures**.
- The former EN Session 013 mid-word meta description defect is fixed.
- The current baseline intentionally uses text-summary social cards; `og:image` is not yet published on session landings and is treated as an optional image-rich preview enhancement rather than a technical-integrity blocker.
- Added reusable automation: `.github/scripts/audit_metadata_og.py`, `.github/workflows/audit-metadata-og.yml`, `.github/scripts/normalize_metadata_og.py`, `.github/workflows/normalize-metadata-og.yml`, `.github/scripts/live_metadata_og_qc.py`, and `.github/workflows/live-metadata-og-qc.yml`.
- Marked **G2 Metadata / Signal Integrity = PASS**.
- Moved active Green-Gate priority to **Live Reader / Regression QC**.

### [SEO / Technical] Keyword-Map ↔ 94 Landing Sync — PASS
- Upgraded `seo/keyword-map.json` from an ID-heavy implementation registry into a bilingual research + implementation registry covering **47 sessions × 2 languages = 94 landing implementations**.
- Added per-language `implementation.id` and `implementation.en` snapshots sourced from the actual landing files.
- Each implementation snapshot now records canonical URL, reader URL, implemented title, meta description, H1, HTML language, and related-session targets.
- Preserved all existing keyword/search-intent research fields rather than generating new editorial SEO targets.
- Preserved the research boundary exactly: Sessions **001–012** remain Deep Live SERP validated in ID + EN; Sessions **013–047** remain `serp-directional` in ID + EN.
- Did **not** silently upgrade directional sessions to Deep SERP validation.
- Hardened HTML attribute parsing after detecting that a simple regex could truncate meta descriptions containing apostrophes such as `Qur'an`; reran synchronization and verified complete strings.
- Source QC verified **94 / 94 implementation snapshots PASS**, **47 / 47 related-session pair parity**, **0 research-boundary issues**, and **0 post-sync registry issues**.
- Live custom-domain QC verified **94 / 94 HTTP 200** and **94 / 94 keyword-map ↔ live landing PASS**, with **0 failures**.
- Added reusable automation: `.github/scripts/sync_keyword_map.py`, `.github/workflows/sync-keyword-map.yml`, `.github/scripts/live_keyword_map_qc.py`, and `.github/workflows/live-keyword-map-qc.yml`.
- Marked **G5 Keyword Map ↔ Landing Sync = PASS**.
- Synchronization exposed a separate metadata-quality issue rather than a registry mismatch: the current English meta description for Session 013 ends mid-word. This is deferred to the next **Metadata Technical Integrity + OG/Share QC** gate.
- Moved active Green-Gate priority to **Metadata Technical Integrity + OG/Share QC**.

### [SEO / Technical] 94-Landing Internal-Link Parity — PASS
- Normalized functional navigation across all **94** Indonesian + English session landings.
- Added a visible reciprocal **ID ↔ EN** counterpart link in each landing breadcrumb.
- Standardized session navigation to include previous / language-specific Tadabbur hub / next slots where applicable.
- Preserved existing descriptive previous/next anchor wording when already present.
- Verified interactive-reader CTA session/language targets across the full corpus.
- Verified related-session blocks across all landings and found only two historical pair mismatches: Sessions **005** and **006**.
- Aligned the two English related-session graphs to the more mature Indonesian baseline while using destination English H1 text as link labels.
- Preserved session article content byte-for-byte: **94 / 94 article blocks unchanged**.
- Source QC: **94 / 94 structural-link PASS**, **47 / 47 related-session ID/EN pair parity**, **0 pair mismatches**.
- Live custom-domain QC: **94 / 94 HTTP 200**, **94 / 94 structural-link PASS**, **47 / 47 related-pair parity**, **0 failures**.
- Live parity passed on the first propagation check.
- Added reusable automation: `.github/scripts/normalize_internal_links.py`, `.github/workflows/normalize-internal-links.yml`, `.github/scripts/live_internal_links_qc.py`, and `.github/workflows/live-internal-links-qc.yml`.
- Marked **G4 Internal-Link Parity = PASS**.
- Moved active Green-Gate priority to **Keyword-Map ↔ Landing Sync**.

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
