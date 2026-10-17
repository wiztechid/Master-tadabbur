# TadabburLife — Publication SOP & Regression Gate v1.2

Updated: 2026-10-17. Baseline incident: Session 049 / PR #32.

## Release contract (fail closed)
Do not merge or publish while any required integrity check fails, while changed-commit checks are pending, or when the required visual/link checks have not been completed. A passing static test is not proof of browser rendering. Keep production unchanged until gates are met.

## Single source of truth
- `data/quran-progress.json`: ordered published session inventory, primary owned ayat, crossReferences.
- `data/ayat-ownership.json`: exact owner for each ayat; no duplicate primary ownership.
- `data/sessions-*.html`: bilingual reader content; every published session must have ID `article.session` and EN `article.en-session`, each with `data-session-number="N"`.
- `index.html`: `const TOTAL=N`; progress counters and hero must reflect actual unique ayat count, total sessions, and rounded coverage.
- `tadabbur/index.html` and `en/tadabbur/index.html`: crawlable index entries, session counts, page title and description must match the published inventory.
- `tadabbur/NNN/index.html`, `en/tadabbur/NNN/index.html`: landing pages with correct canonical, hreflang, visible content and owner cross-reference links.
- `sitemap.xml` and `seo/keyword-map.json`: both language paths and unique search intents; check for cannibalization.

## Canonical landing template contract

- `docs/SESSION-LANDING-TEMPLATE-v1.md` is the required contract for every generated or manually maintained session landing. The article content may differ by session; the HTML head, metadata, schema, navigation, trust destinations, responsive behavior, and ad boundaries must satisfy the contract.
- Run `python3 .github/scripts/session_template_contract_qc.py` on every PR that changes a session landing or its template rules. It checks all 98 published landings, not only the changed page.
- OG/Twitter title and description, canonical, reciprocal hreflang, Article + BreadcrumbList JSON-LD, author/publisher identity, responsive viewport/CSS, legal destinations, and absence of ad loader on session landings are required. Social image metadata is required only when a matching verified image asset exists; never point to a missing image.
- For visual mobile regression, use the representative preview at 375px/390px for sessions 001, 048, and 049 in both languages, including programmatic horizontal-overflow assertions. A screenshot artifact still requires visual inspection; screenshots alone do not prove a pass.
- Sacred text, established translation, hadith quotations/references, and session meaning are outside this template patch scope. Any source correction follows the verified source-correction workflow and Sacred Diff.

## Before committing a new session
1. Check full verse ownership across ALL reader modules; do not reuse owned verses as primary. Register reused verses as explicit crossReferences with correct ownerSession.
2. Review tafsir, Arabic, translations and quotation boundaries. A link labelled “read verse” must point to the verse, not a tafsir commentary page; keep tafsir links distinct.
3. Keep draft and reader module content identical. Preserve reader class contract: ID `session`, EN `en-session`; verify each language has exactly one matching article.
4. For each crossReference, add a visible link to the owner's landing page in the reader article AND the matching language landing page. Use `data-owner-session="N"` markers; don't add decorative or dead controls.
5. Update both crawlable indexes with `NNN/` links, counts, titles and descriptions. Update homepage `TOTAL`, `stat-sessions`, `stat-ayat`, `quran-progress-text`, and progress bar using the same registry. Example Session 049: 49 sessions, 79 unique owned ayat, 79/6236 = 1.3% (one decimal).
6. Update sitemap, canonical/hreflang and SEO keyword map. Check navigation/footer and the reader's session selection on both languages.

## Required CI and validation
- Run `python3 .github/scripts/quran_progress_qc.py` and `python3 .github/scripts/ayat_ownership_qc.py` locally or through existing lightweight PR checks. Both must pass **on the latest commit**.
- Check that reader draft and module articles are byte-identical for the new session; check unique IDs, required owner links, canonical/hreflang, sitemap and both index listings.
- Inspect rendered ID/EN landing pages and interactive reader on desktop/mobile, test navigation, internal links and visible overflow. If browser verification is unavailable, record **VISUAL PENDING**, not GREEN.
- After each fix, confirm checks for the NEW head SHA; older successful runs are not evidence for the current head.
- GitHub Mode Hemat WIZ: lightweight integrity checks on PR; deep/full audits only once after a substantive batch, manually/on demand. Avoid duplicate reruns.

## Release evidence and rollback
Record PR, branch, head SHA, integrity check conclusions, static checks, browser observations, any known limitations, and publication decision. Merge only when all mandatory gates are GREEN and publication is authorized. On post-merge regression, revert the release commit or deploy the last known-good version; never mask a failing integrity gate.

## Incident prevention: Session 049
Observed failures: homepage displayed 48/76 while metadata was 49/79; EN reader used `session` instead of `en-session`; missing explicit owner links; bilingual crawlable indexes omitted Session 049; primary verse links were mistakenly pointed at tafsir pages. These are now mandatory prepublication checks.
