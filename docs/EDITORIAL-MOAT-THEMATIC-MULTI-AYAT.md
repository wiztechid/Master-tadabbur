# TadabburLife — Editorial Moat: Thematic Multi-Ayat (v1.0)

Effective: 2026-10-14. Scope: all new Indonesian and English sessions.

## Core rule
A session may explain multiple relevant Qur'an verses under ONE coherent topic. Every verse selected for primary exegesis must be unowned across all prior sessions. One verse has exactly one primary owner session across the entire bilingual corpus. Indonesian and English editions share that owner; they do not count as separate sessions.

## Pre-publication gate (fail closed)
1. Fetch latest main and read `data/ayat-ownership.json`, `data/quran-progress.json`, all relevant sessions, and current drafts/PRs.
2. Expand each proposed range into individual surah:ayah keys; compare every key against the ownership registry and prior primary exposition, including overlapping ranges. Any already-owned verse is excluded from NEW primary exegesis.
3. Existing verses may appear only as brief supporting cross-references linking to their owner session, without repeating detailed tafsir; record `ownerSession` in crossReferences. Do not claim them as new coverage.
4. Check semantic overlap and cannibalization of the topic, not merely verse numbers. Require a distinct reader intent and substantial new practical value.
5. For all new primary verses, verify Arabic text, translation and context with authoritative sources; distinguish direct tafsir from editorial reflection, use recognized tafsir and avoid unsupported religious claims.
6. Build coherent long-form Indonesian and English versions with one H1, accurate title/meta/canonical/schema where applicable, accessible reading UX, working internal references, sitemap/indexability and actual publication date (no backdating).
7. Update both ownership and progress registries atomically with the session. Run only existing lightweight QC on content changes. If ownership conflict, content, links, or validators fail: BLOCKED; do not publish.
8. After publication, check new live URL, canonical and indexability lightly. Heavy browser/UI smoke remains manual/on-demand only for substantive or interactive changes and AdSense resubmission.

## Scheduling and scope
At most one TadabburLife session per scheduled run, and only after CLEAR & CLEAN. ErrorHarbor is out of scope for this editorial update; do not change existing GitHub workflow triggers or schedules. If no qualifying session is found, publish nothing and report blockers.

## Example only (not preapproved)
Theme: inviting with wisdom. Candidate verses: 16:125, 20:44, 3:159. Each must pass latest ownership, semantic overlap and source review before being selected; no verse is reserved by this example.
