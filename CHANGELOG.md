# TadabburLife — Project Changelog

Records material verified changes to TadabburLife.

This document does not replace Git history. Routine commits, minor copy adjustments, and work that has not yet been implemented or verified are not recorded here.

---

## 2026-09-23

### [SEO] Post-Dedup Deep Live SERP Revalidation — Sessions 004, 007, 011, 016, 043, 044 — PASS
- Revalidated **6 sessions × ID/EN = 12 landing targets** after the ayat-ownership deduplication remap.
- Restored the published corpus to **47 / 47 Deep Live SERP aligned sessions = 94 / 94 session-language targets**.
- Session **004** now owns only **An-Nisa/Quran 4:135** on justice even against self-interest; Session 023 exclusively owns 4:58 on returning trusts.
- Session **007** owns **At-Tahrim/Quran 66:8** on taubat nasuha / sincere repentance; Session 031 exclusively owns Az-Zumar 39:53 on despair after sin and Allah's mercy.
- Session **011** owns **Al-Isra/Quran 17:36** on not following what is unknown and accountability of hearing/sight/heart; Session 042 exclusively owns Al-Hujurat 49:6 on tabayyun / verification of incoming reports.
- Session **016** remains a no-ayat nightly-muhasabah companion linking to owner Session 030 for Al-Hashr 59:18.
- Session **043** owns only **Luqman/Quran 31:19** on measured walking and lowering the voice; Session 027 exclusively owns 31:18 on arrogance/contempt.
- Session **044** remains a no-ayat daily time-audit companion linking to owner Session 010 for Al-'Asr 103:1–3.
- Sharpened title/H1/meta for **004, 011, and 044** based on the post-dedup live intent.
- Added/normalized exactly one post-dedup SERP answer block across all 12 ID/EN targets.
- Removed stale schema-keyword references to former duplicate ayat/themes and refreshed owner↔companion cannibalization guards.
- Updated demand evidence to **`deep-live-serp-validated-2026-09-23-post-dedup`**.
- Added research record **`seo/post-dedup-deep-serp-004-007-011-016-043-044-2026-09-23.md`**.
- Added persistent targeted live validator **`.github/scripts/live_post_dedup_serp_qc.py`** + **`.github/workflows/live-post-dedup-serp-qc.yml`**.
- Final targeted live QC: **12 / 12 HTTP 200, 12 / 12 PASS, 0 failures, 0 owner-guard issues**, with propagation passing on the first attempt.

### [Homepage / UX] Back-to-Top Scroll Polish — PASS
- Changed the floating ↑ control to remain hidden while `scrollY < 400` and fade in once the reader reaches `scrollY >= 400`.
- Added fade/translate transition, disabled pointer interaction while hidden, and respected `prefers-reduced-motion`.
- Added accessible button labeling and retained smooth-scroll return to the page top.
- Extended live homepage browser QC to verify hidden-at-top → visible-after-400 → hidden-after-return behavior.
- Latest live browser QC passed all tested desktop/tablet/mobile ID/EN profiles with no overflow or browser errors.

### [Homepage / Live QC] Qur'an Progress Propagation & Visual Regression — PASS
- Verified the custom domain after deployment; the new Qur'an-coverage homepage state propagated successfully on the **first live check**.
- Verified **HTTP 200**, localized progress copy, **75 / 6,236** ayat coverage, **1.2%**, and supporting **47 sessions**.
- Browser QC passed **5 / 5 profiles**: desktop ID, tablet ID, mobile ID, desktop EN, and mobile EN.
- Verified no horizontal overflow, no console/page errors, and a rendered progress-bar ratio matching the calculated **1.2027%** coverage.
- Visually reviewed representative live screenshots for desktop ID, mobile ID, and mobile EN; no clipping or broken responsive layout was found.
- Added persistent browser QC: **`.github/scripts/live_homepage_progress_qc.mjs`** + **`.github/workflows/live-homepage-progress-qc.yml`**, with latest evidence under **`.github/qc-state/homepage-live/`**.
- Aligned the live QC report with ayat-ownership schema v2: **75 owned unique ayat + 11 cross-reference occurrences = 86 historical reference occurrences represented**.

### [Corpus / Governance] Ayat Deduplication & Ownership Audit 001–047 — PASS
- Completed a full ayat-ownership audit across Sessions **001–047**, Indonesian + English.
- Historical corpus contained **8 conflict groups / 11 repeated ayat** where the same verse had become a primary anchor in more than one session.
- Adopted the permanent rule **ONE AYAT → ONE PRIMARY OWNER SESSION**.
- Resolved ownership as follows:
  - **An-Nisa 4:58 → S023**; S004 now owns An-Nisa 4:135.
  - **Al-Hujurat 49:12 → S015**; S005 now owns Al-Hujurat 49:11.
  - **Ash-Sharh 94:5–6 → S018**; S006 now owns Al-Baqarah 2:153.
  - **Az-Zumar 39:53 → S031**; S007 now owns At-Tahrim 66:8.
  - **Al-'Asr 103:1–3 → S010**; S044 is now a practical companion/checkpoint.
  - **Al-Hujurat 49:6 → S042**; S011 now owns Al-Isra 17:36.
  - **Al-Hashr 59:18 → S030**; S016 is now a nightly-muhasabah practical companion.
  - **Luqman 31:18 → S027**; S043 now owns Luqman 31:19.
- Removed repeated owner verse/tafsir blocks from the non-owner sessions and added explicit owner cross-reference cards in both ID and EN reader source + affected public landings.
- Added reciprocal related links from owner landings where missing: **S031 ↔ S007, S010 ↔ S044, S042 ↔ S011**.
- Added **`data/ayat-ownership.json`** as the explicit ayat → owner registry.
- Upgraded **`data/quran-progress.json`** to schema v2 / `unique_owned_ayat`; current corpus is **75 unique owned ayat, 0 duplicate primary owners**.
- Added CI guard **`.github/scripts/ayat_ownership_qc.py`** + **`.github/workflows/ayat-ownership-qc.yml`**.
- Updated **Master SOP to v1.4** with the **Ayat Ownership & Deduplication Lock**, mandatory Ayat Ownership Preflight for Session 048+, partial-range overlap rules, companion-session rules, and ownership-migration requirements.
- Added audit record **`seo/ayat-ownership-audit-001-047-2026-09-23.md`**.
- Source-level QC after patch: **75 unique owned ayat, 0 duplicate owners, 0 duplicate Arabic verse segments**, all eight cross-reference relationships present in ID + EN source and public landings.
- Sessions **004, 007, 011, 016, 043, 044** changed materially enough to require a post-dedup live-SERP refresh before their previous Deep status is considered current.

### [Homepage / Data] Qur'an Coverage Progress — IMPLEMENTED
- Replaced the homepage's primary progress denominator from the editorial target of approximately 1,000 sessions to **Qur'an ayat discussed / 6,236 ayat**.
- Current published Sessions 001–047 now resolve to **75 uniquely owned ayat** after the ownership cleanup, producing **1.2% Qur'an coverage**.
- Final ID hero copy: **`75 dari 6.236 ayat • 1,2% cakupan Al-Qur'an`**.
- Final EN hero copy: **`75 of 6,236 verses • 1.2% Qur’an coverage`**.
- Retained **47 sessions** as a supporting statistic rather than the main progress denominator.
- Added **`data/quran-progress.json`** as the normalized progress source of truth; after deduplication it uses `countMode=unique_owned_ayat`.
- Updated homepage runtime so progress bar, localized copy, discussed-ayat count, denominator, and session count are derived from the dataset.
- Added **`.github/scripts/quran_progress_qc.py`** and **`.github/workflows/quran-progress-qc.yml`** to guard dataset/session-count/static-fallback integrity.
- Updated Live Reader Regression triggers so changes to `data/quran-progress.json` also run browser regression.
- The initial homepage-only progress change was followed by the corpus-wide ownership cleanup recorded below.

## 2026-09-22

### [SEO] Deep Live SERP + Cannibalization — Sessions 037–040 — PASS
- Completed independent Indonesian + English Deep Live SERP research for Sessions **037–040**, advancing coverage to **40 / 47 sessions = 80 / 94 session-language targets**.
- Session **037** now owns shura/consultation in shared decision-making under Asy-Syura/Quran 42:38, separated from cooperation-direction (033) and information-verification (042).
- Session **038** now owns the integrated definition of **al-birr / true righteousness** under Al-Baqarah/Quran 2:177, separated from contracts (024), charity multiplication (026), sincerity (039), and Al-Ma'un's ritual-social warning (040).
- Session **039** now owns sincere devotion/ikhlas in worship under Al-Bayyinah/Quran 98:5.
- Session **040** now owns Surah Al-Ma'un's specific connection between final accountability, orphans/poor, heedless or showy prayer, and withholding useful help.
- Added direct-answer blocks and synchronized title/H1/meta for all **8** ID/EN landings.
- Strengthened explicit internal cannibalization guards for **037↔042** and **038↔039/040/024**.
- Preserved sacred Qur'an/hadith source text and the locked reflection/practical-action meaning layer.
- Updated `seo/keyword-map.json`, added `seo/deep-serp-037-040-2026-09-23.md`, and advanced the live keyword-map QC boundary to **001–040 Deep / 041–047 directional**.
- Active Deep SERP priority advances to **Sessions 041–044 bilingual**.


### [SEO] Deep Live SERP + Cannibalization — Sessions 033–036 — PASS
- Completed independent Indonesian + English Deep Live SERP research for Sessions **033–036**, advancing coverage to **36 / 47 sessions = 72 / 94 session-language targets**.
- Session **033** now owns cooperation in righteousness and piety versus cooperation in sin/aggression under Al-Ma'idah/Quran 5:2.
- Session **034** now owns dunya-akhirah orientation under Al-Qasas/Quran 28:77, separated from Session 030's provision-for-tomorrow intent.
- Session **035** now owns the general justice + ihsan ethic under An-Nahl/Quran 16:90, separated from Session 020's justice-under-dislike intent and Session 004's trust/justice-in-authority intent.
- Session **036** now owns tabdhir/wasteful spending and responsible direction of wealth under Al-Isra/Quran 17:26–27.
- Added direct-answer blocks and synchronized title/H1/meta for all **8** ID/EN landings.
- Strengthened the **035↔020** cannibalization guard through explicit related-session linking.
- Preserved sacred Quran/hadith source text and the locked reflection/practical-action meaning layer.
- Updated `seo/keyword-map.json`, added `seo/deep-serp-033-036-2026-09-22.md`, and advanced the live keyword-map QC boundary to **001–036 Deep / 037–047 directional**.
- Active Deep SERP priority advances to **Sessions 037–040 bilingual**.


### [SEO] Deep Live SERP + Cannibalization — Sessions 029–032 — PASS
- Completed independent Indonesian + English Deep Live SERP research for Sessions **029–032**, advancing coverage to **32 / 47 sessions = 64 / 94 session-language targets**.
- Session **029** now owns striving for Allah → guidance under Al-Ankabut/Quran 29:69, separated from tawakkul-after-effort (008) and inner-change intent (019).
- Session **030** now owns deeds sent ahead / provision for tomorrow and the Hereafter under Al-Hashr/Quran 59:18, while Session 016 retains nightly/daily muhasabah practice.
- Session **031** now owns sin-related despair → repentance and Allah's mercy under Az-Zumar/Quran 39:53.
- Session **032** now owns burden within capacity + responsibility + prayer under Al-Baqarah/Quran 2:286, with an explicit boundary against telling overwhelmed people to carry everything alone.
- Added direct-answer blocks and synchronized title/H1/meta for all **8** ID/EN landings.
- Preserved sacred Quran/hadith source text and the locked reflection/practical-action meaning layer.
- Updated `seo/keyword-map.json`, added `seo/deep-serp-029-032-2026-09-22.md`, and advanced the live keyword-map QC boundary to **001–032 Deep / 033–047 directional**.
- Active Deep SERP priority advances to **Sessions 033–036 bilingual**.


### [SEO] Deep Live SERP + Cannibalization — Sessions 017–028 — PASS
- Completed independent Indonesian + English Deep Live SERP research for Sessions **017–028**, advancing coverage to **28 / 47 sessions = 56 / 94 session-language targets**.
- Added and validated search territories and cannibalization guards for batches **017–020, 021–024, and 025–028**.
- Sessions 025–028 now own distinct intents: **025 mutual-consent trade (Quran 4:29), 026 charity + multiplied reward (Quran 2:261), 027 arrogance/contempt (Quran 31:18), 028 reconciliation/islah (Quran 49:10)**.
- Added direct-answer blocks and synchronized title/H1/meta for all 025–028 ID + EN landings.
- Hardened the same-verse guard **027↔043**: Session 027 owns arrogance/contempt; Session 043 owns the positive practice of humility in walking and speaking across Quran 31:18–19.
- Corrected Session 043 journey wording so it no longer states that Quran 31:18 had not appeared previously.
- Preserved sacred Quran/hadith source text and the locked reflection/practical-action meaning layer.
- Updated `seo/keyword-map.json`, added `seo/deep-serp-025-028-2026-09-22.md`, and advanced the live keyword-map QC boundary to **001–028 Deep / 029–047 directional**.
- Active Deep SERP priority advances to **Sessions 029–032 bilingual**.


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
