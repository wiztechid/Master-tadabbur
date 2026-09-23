# TadabburLife — Final Release Gate v1.0

- Tested commit: `9420c58514f05ff7397bad41153c8856fee97bfd`
- Generated: 2026-09-23T08:06:33.996954+00:00
- Duration: 25.41 s
- Checks: 14 / 16 PASS
- Release status: **BLOCKED**

| Gate | Result |
|---|---:|
| source_public_inventory | FAIL |
| keyword_map_source_sync | PASS |
| keyword_map_no_drift_after_sync | PASS |
| source_metadata_og_94 | PASS |
| ayat_ownership_source | PASS |
| quran_progress_source | PASS |
| live_103_url_crawl | PASS |
| live_hreflang_94 | PASS |
| live_keyword_map_94 | PASS |
| live_metadata_og_94 | PASS |
| live_reflection_og_94 | PASS |
| live_schema_94 | FAIL |
| live_internal_links_94 | PASS |
| live_post_dedup_serp_12 | PASS |
| live_reader_regression | PASS |
| live_homepage_progress | PASS |

## Blocking failures

- **source_public_inventory** — ["sitemap_missing:['https://tadabburlife.com/cookie-policy/', 'https://tadabburlife.com/privacy-policy/']", "sitemap_extra:['https://tadabburlife.com/cookies/', 'https://tadabburlife.com/privacy/']", "missing_public_file:privacy-policy/index.html", "missing_public_file:cookie-policy/index.html"]
- **live_schema_94** — {"urls_expected": 94, "urls_checked": 94, "http_200_count": 94, "pass_count": 86, "fail_count": 8, "overall_pass": false}
