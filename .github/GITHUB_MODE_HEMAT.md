# GitHub Mode Hemat WIZ

Baseline for `wiztechid/Master-tadabbur`.

## Automatic CI
Only lightweight integrity checks should run automatically on content changes:
- `ayat-ownership-qc.yml`
- `quran-progress-qc.yml`

These checks must stay local/repository-level and avoid browser installation, live-site crawling, mass rebuilds, or write-back commits.

## Manual / on-demand
All live crawls, browser regressions, Deep SERP audits, mass normalizers, OG regeneration, full release gates, batch publishers, and other expensive or write-heavy workflows are `workflow_dispatch` only.

Run heavy validation once after a substantive batch is complete. If it fails, fix issues in a batch using lightweight checks, then rerun the heavy validation once at the end.

## Publishing rule
Audit and local QC first. Publish only when the change is CLEAR & CLEAN. Do not trigger mass rebuilds, backfills, repeated live crawls, or duplicate validation runs for routine article publication.
