# TadabburLife — Session Landing Template Contract

**Version:** 1.1  
**Date:** 2026-10-17  
**Status:** ACTIVE CONTRACT — REQUIRED FOR ALL PUBLISHED SESSIONS  
**Authority:** subordinate to `mastersoptadabbur.md` and the Absolute Sacred Lock.

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

- Every bilingual session landing links to the single shared stylesheet at `assets/css/session-landing-v1.css?v=1.1` using the correct relative path.
- Inline page styles are removed from session landing pages. Shared shell, cards, typography, Qur'an display, calls to action, related links, and responsive behavior are maintained in the shared stylesheet.
- Primary Qur'an verse blocks use the same deep green background and gold border, including legacy ayahbox blocks and Arabic verse paragraphs.
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

- Run `python3 .github/scripts/session_template_contract_qc.py` for all 98 published bilingual landings.
- Run the representative mobile preview for sessions 001, 048, and 049 in ID/EN at 375px and 390px; verify no horizontal overflow and visually inspect screenshots.
- Preserve lightweight pull-request checks. Run the heavier full release gate once after a substantial batch, not repeatedly after small edits.
- Record exact tested commit SHA and any visual limitation. A source-level pass is not a visual pass.
