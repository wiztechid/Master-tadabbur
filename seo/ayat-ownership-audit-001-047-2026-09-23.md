# TadabburLife — Ayat Deduplication & Ownership Audit 001–047

**Date:** 23 September 2026  
**Scope:** Sessions 001–047, Indonesian + English reader source and public landings  
**Policy:** ONE AYAT → ONE PRIMARY OWNER SESSION

## Executive result

Historical audit found **8 ownership conflict groups involving 11 repeated ayat**. All conflicts have been resolved so that each ayat has one primary owner. Non-owner sessions now cross-reference the owner instead of repeating the verse/tafsir block.

Current source-level baseline:

- published sessions: **47**
- unique owned ayat: **75**
- primary-owner duplicates: **0**
- companion/practical-checkpoint sessions: **016, 044**
- progress denominator: **75 / 6,236 = 1.2%**
- ownership registry: `data/ayat-ownership.json`
- session declaration source: `data/quran-progress.json`
- anti-duplicate guard: `.github/scripts/ayat_ownership_qc.py`

## Conflict resolution matrix

| Conflict | Primary owner | Non-owner resolution |
|---|---|---|
| An-Nisa 4:58 — S004 / S023 | **S023** | S004 now owns **An-Nisa 4:135** and links to S023 for 4:58. The 4:58 verse/tafsir block was removed from S004. |
| Al-Hujurat 49:12 — S005 / S015 | **S015** | S005 now owns **Al-Hujurat 49:11** only and links to S015 for 49:12. |
| Ash-Sharh 94:5–6 — S006 / S018 | **S018** | S006 now owns **Al-Baqarah 2:153** only and links to S018 for 94:5–6. |
| Az-Zumar 39:53 — S007 / S031 | **S031** | S007 now owns **At-Tahrim 66:8** and links to S031 for 39:53. |
| Al-'Asr 103:1–3 — S010 / S044 | **S010** | S044 is now a **practical time-audit companion** with no new ayat ownership and links to S010. |
| Al-Hujurat 49:6 — S011 / S042 | **S042** | S011 now owns **Al-Isra 17:36** and links to S042 for 49:6. |
| Al-Hashr 59:18 — S016 / S030 | **S030** | S016 is now a **nightly-muhasabah practical companion** with no new ayat ownership and links to S030. |
| Luqman 31:18 — S027 / S043 | **S027** | S043 now owns **Luqman 31:19** only and links to S027 for 31:18. |

## Ownership rules applied

1. A full ayat may have only one primary owner.
2. Partial range overlap counts as a conflict.
3. A non-owner may mention the reference and link to the owner, but may not repeat the Arabic verse block, translation, tafsir, or a second verse-centered answer block.
4. A session that adds only application/practice may exist as a companion, but contributes **0 new ayat** to Qur'an coverage.
5. ID and EN versions share the same ownership.
6. Ownership migration requires simultaneous updates to reader source, public landings, metadata, keyword map, progress data, cross-links, and QC.

## SEO consequence

Ownership cleanup changed the implemented search anchor materially for Sessions **004, 007, 011, 016, 043, 044**. Their historical Deep SERP research remains useful background, but these six sessions require a post-dedup live-SERP refresh before their Deep validation status is treated as current.

Sessions **005** and **006** were narrowed to the search territories they already owned, so their primary intent remains materially aligned with the previous validation.

## Future publication gate — Session 048+

Before a new session is published:

1. declare proposed owned ayat in `data/quran-progress.json`;
2. compare every ayat in every range against `data/ayat-ownership.json`;
3. if any overlap exists, either:
   - choose a different unowned ayat, or
   - make the new session a cross-reference/companion;
4. run `python3 .github/scripts/ayat_ownership_qc.py`;
5. do not publish unless the guard passes.

## QC evidence

Source-level post-patch audit verified:

- **75 unique owned ayat**
- **0 duplicate primary owners**
- **0 duplicate Arabic verse segments across Indonesian primary verse blocks**
- cross-reference markers and owner links present for all eight remapped non-owner sessions in ID + EN reader source
- matching owner links present on all 16 affected public landings
- companion sessions 016 and 044 contain no primary verse feature block

This audit is the ownership baseline for future corpus growth.
