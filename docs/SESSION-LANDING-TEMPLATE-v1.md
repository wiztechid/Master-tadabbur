# TadabburLife — Session Landing Template Contract

**Version:** 1.4  
**Date:** 2026-10-18  
**Status:** FROZEN  
**Authority:** subordinate to `mastersoptadabbur.md` and the Absolute Sacred Lock.

## Freeze record

- **Freeze ID:** SESSION-LANDING-v1.4
- **Frozen on:** 2026-10-18, after the authorized Arabic glyph-fallback thaw passed release gates.
- **Reference visual:** Session 013's deep-green featured Qur'an module, gold heading, and green verse panel with gold border.
- **Locked asset:** `assets/css/session-landing-v1.css` (Git blob SHA `153087a92bde745d47470d9c82ebff1ea5384036`; contract QC pins this exact asset).
- **Scope:** all 98 published bilingual session pages and future session landing pages. The shared stylesheet cache key is `?v=1.4`.
- **Verified release:** PR #65, merge commit `34296cda73d760f55b06c6b11dab8c27f7d2b462`. Contract QC passed for 98/98 pages; the representative mobile preview passed 12 checks at 375px and 390px across sessions 001, 048, and 049 in Indonesian and English. Production spot-checks on sessions 001 and 027 confirmed connected white Arabic text on the green ayah panel in both Indonesian and English, with language-switch and session navigation available.
- **Locked Arabic treatment:** Noto Naskh Arabic is loaded with `display=swap` for `.ayah` and `p[lang="ar"]`, with a generic serif fallback. Arabic remains white; the ayah panel remains green with its gold border. Font size, line-height, layout, spacing, navigation, and other colors remain unchanged.
- **Thaw rule:** change the frozen visual contract only after an explicit user instruction. Then update the stylesheet, cache key, freeze record, and QC together; pass corpus-wide QC, mobile preview, and live production verification before refreezing. Article content may still be edited when the shared visual contract is preserved.

## Purpose

This document defines the fixed shared contract for Indonesian and English session landing pages. Session-specific article content remains independently authored. Layout, navigation, technical metadata, schema, legal destinations, and ad boundaries follow this contract.

## Required document head

Every `tadabbur/NNN/index.html` and `en/tadabbur/NNN/index.html` must provide:

- Correct document language and mobile viewport.
- One descriptive title, one meta description, and exactly one H1.
- A self-referencing canonical URL.
- Reciprocal `id`, `en`, and `x-default` hreflang links. The Indonesian canonical is the x-default destination.
- Open Graph type, site name, locale, title, description, and canonical URL.
- Twitter card, title, and description matching the page language.
- Article JSON-LD with headline, description, language, canonical URL, WebPage main entity, named author, and TadabburLife publisher.
- BreadcrumbList JSON-LD with the home page and the current session.
- OG/Twitter image tags only when a verified corresponding image asset exists in the repository. Never reference a missing asset. Publication dates are optional and must use a verified date; never infer or backdate them.

## Required page structure

Keep the visual and navigation order consistent:

1. Breadcrumb and language switch.
2. One page H1 and concise session identifier.
3. The session article with its published source blocks intact.
4. Practical reflection/action blocks appropriate to that session.
5. Reader CTA, previous/next navigation, and related/owner links where applicable.
6. Six trust/legal destinations: About, Privacy, Cookies, Terms, Disclaimer, and Contact.

The article's headings, examples, explanations, and reflection are session-specific. Shared layout must not create repeated filler or change a session's meaning.

## Shared visual template

- Every bilingual session landing links to the shared stylesheet at `assets/css/session-landing-v1.css?v=1.4` using the correct relative path, and loads the Google Fonts Noto Naskh Arabic stylesheet with `display=swap`.
- Inline page styles are removed from session landing pages. Shared shell, cards, typography, Qur'an display, calls to action, related links, and responsive behavior are maintained in the shared stylesheet.
- Primary Qur'an modules use the deep green featured-card shell from Session 013; ayahbox blocks and Arabic verse paragraphs keep their deep green background and gold border; Arabic verse text is white for readable contrast and uses Noto Naskh Arabic with a serif fallback. The multi-verse Quranic anchors on Session 049 follow the same featured-card treatment.
- **Interactive reader parity:** The homepage reader injects these same session modules, so its primary verse cards must retain the same frozen v1.4 treatment: deep-green featured shell, gold heading, green ayah panel with gold border, and white Arabic in Noto Naskh Arabic. Session 049's three Arabic excerpts (`p[lang="ar"]`) use the matching green/gold panel and white type. Sessions 016 and 044 remain cross-references and must not gain duplicated ayat. The reader's dashboard and navigation shell remain independent.
- Session-specific article content and modules remain in each page; compatibility selectors keep legacy session modules readable.

## Responsive and monetization rules

- Include a viewport declaration and use the shared mobile breakpoints; avoid horizontal overflow at 375px and 390px.
- Session landing pages remain free of AdSense loader/units unless a separately approved change updates this contract and passes mobile/accidental-click QC.
- Do not place an ad inside or beside Qur'an, translation, tafsir, hadith, answer blocks, navigation, reader controls, or reflection/action controls.
- The homepage loader does not mean an ad unit is active. Confirm actual placements separately before changing the launch matrix.
- Keep legal/trust pages ad-free.

## Sacred-content boundary

This template is structural. It must never rewrite, paraphrase, reorder, translate, normalize, or silently correct the established Arabic Qur'an text, verse identity, published Qur'an translation, quoted hadith, or verified religious references. A source correction follows the verified source-correction process and requires Sacred Diff. Keep article-body changes out of template-only patches.

## Required release checks

- Run `python3 .github/scripts/session_template_contract_qc.py` for all 98 published bilingual landings. Verify the Google Fonts request and local fallback family.
- Run the representative mobile preview for sessions 001, 048, and 049 in ID/EN at 375px and 390px; verify no horizontal overflow and visually inspect screenshots.
- After deployment, verify the updated template on representative Indonesian and English production pages; record the tested commit and observed Arabic contrast/glyph rendering.
- Preserve lightweight pull-request checks. Run the heavier full release gate once after a substantial batch, not repeatedly after small edits.
- Record exact tested commit SHA and any visual limitation. A source-level pass is not a visual pass.
