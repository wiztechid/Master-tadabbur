# Worker Session Publication Standard

**Version:** 1.0  
**Status:** Internal publishing requirement  
**Applies to:** Every new or revised TadabburLife session published through the Worker migration workflow, in Indonesian, English, and the interactive reader.

This standard turns the quality demonstrated by Sessions 006 and the expanded Sessions 050–051 into a repeatable editorial and release checklist. It supplements `mastersoptadabbur.md`, `docs/SESSION-LANDING-TEMPLATE-v1.md`, and `docs/SOP-PUBLICATION-REGRESSION.md`; those higher-level rules remain authoritative.

## 1. Non-negotiable source integrity

Before drafting or editing:

- Identify the session’s primary Qur’an passage, theme, verse owner, and related-session links from the canonical registries.
- Preserve the approved Arabic, verse identity/reference, established translation, and verified hadith text and attribution. These are the Absolute Sacred Lock.
- Distinguish the Qur’an text, translation, tafsir quotation/summary, and the author’s reflection. Do not present editorial reflection as revelation or as a verbatim tafsir.
- Verify religious claims and source links against reliable, identifiable references. Link a complete verse when the page quotes only an excerpt; label verse links and tafsir links accurately.
- Do not claim a guaranteed outcome, invent a reason for a personal event, assign a specific divine response or timeline, shame a reader, or issue a ruling for an individual circumstance.
- Send a suspected source error through the verified source-correction process; never silently rewrite sacred text as an editorial change.

## 2. Content completeness for every session

Each article must be useful as a standalone reading and contain enough explanation to guide the reader through the passage. Use the frozen landing template; completeness is an editorial standard, not permission to redesign the page.

Review these content elements:

1. **Clear title and opening:** State the passage and central question or theme in plain language. Introduce a real reader concern without sensationalism or unsupported claims.
2. **Passage and context:** Present the approved verse or clearly labeled excerpt, translation, and source link. Explain where the passage sits in its surrounding discussion and why that context matters.
3. **Meaningful explanation:** Develop the central message in a coherent sequence. Explain the important parts of the passage and how they relate; avoid merely repeating the translation or listing generic lessons.
4. **Grounded interpretation:** Attribute tafsir-based points and separate them from editorial application. Give the reader boundaries where the verse does not specify an outcome, timing, or personal ruling.
5. **Practical reflection:** Offer specific questions for muhasabah and one realistic action connected to the passage. Make clear when an action is an editorial reflection aid rather than an established worship formula or fatwa.
6. **Takeaway and continuation:** End with a concise, passage-grounded hikmah and a useful connection to the TadabburLife journey. Link relevant owner/related sessions without duplicating another session’s primary verse content.
7. **Appropriate scope:** Include cautions or a referral to a qualified scholar/professional when application depends on a personal religious, medical, safety, or legal circumstance.

A section may be adapted or omitted only when it does not fit the passage; preserve the substance elsewhere and record the editorial reason during review. Do not add filler or pursue a word-count target at the expense of accuracy and clarity.

## 3. Bilingual and reader parity

For each release:

- Maintain equivalent meaning, completeness, cautions, source attribution, and related-session links in Indonesian and English. Natural wording may differ; claims and guidance must not.
- Keep each landing article synchronized with its matching reader module. Preserve the required article classes and session-number attributes.
- Check verse references, link targets, headings, and language-specific canonical/hreflang relationships in both languages.
- Treat the reader as another rendering surface for the same approved content, not as a shortened or independently edited version.

## 4. SEO and frozen template

- Match each page title, description, heading, and search intent to the actual session. Keep metadata unique and accurate; avoid keyword stuffing and unintended cannibalization.
- Preserve the frozen SESSION-LANDING-v1.4 structure, CSS, spacing, typography, navigation, verse card, Arabic treatment, and trust/legal boundaries.
- Content edits do not authorize layout, metadata schema, or shared-template changes. A template change needs the explicit thaw and refreeze process in the Master SOP.
- Keep internal SOPs, drafts, editorial notes, QC evidence, and private research outside the public Worker asset bundle.

## 5. Required publication review

A session is ready for publication only when all applicable items pass on the latest commit:

- Sacred-text and source-reference review, including correct distinction between verse and tafsir links.
- Ayat ownership, cross-reference ownership links, Qur’an progress, and deduplication checks.
- Indonesian/English/reader content parity and completeness review against this standard.
- Session landing template contract, metadata, canonical/hreflang, sitemap, index, and keyword-map checks.
- Required CI checks green for the current head SHA.
- Rendered Indonesian and English landings and reader checked for visible content, working navigation/links, and mobile overflow. If browser review is unavailable, record **VISUAL PENDING** and do not mark the release fully verified.
- Worker bundle/build and route checks pass; preview is compared with the current production page before any Worker release.
- Record branch/PR, head SHA, check results, visual observations, publication decision, and any limitation in the release evidence.

Never publish directly from an authoring screen to production. The future Worker authoring flow must create a Git branch and PR, run these gates, and require review before merge/deploy. Until that workflow exists, this document is the internal standard for work prepared for the Worker migration.

## 6. What Sessions 050–051 add to the quality bar

Use these as examples of passage-specific depth, not copy-and-paste templates:

- **Session 050 (Al-Baqarah 2:186):** read the verse’s movement from the question, to Allah’s nearness and response, to the call to respond and believe; connect prayer with responsible effort without promising a particular outcome. Its “reflection map” is explicitly an editorial aid, not a worship formula or measure of acceptance.
- **Session 051 (Al-Baqarah 2:187):** read permission, pardon, worship boundaries, and taqwa together; distinguish a structural summary from comprehensive fiqh. Direct personal rulings to qualified scholarship.

Future sessions need similarly specific explanation based on their own passage. Reusing these exact headings or claims where they do not fit is not compliance.
