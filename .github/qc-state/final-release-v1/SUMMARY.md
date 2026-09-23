# TadabburLife — Final Release Gate v1.0

- Tested commit: `5b94bd4da925e2b4957f800766dab787dcd3803a`
- Generated: 2026-09-23T08:12:09.893514+00:00
- Duration: 108.65 s
- Checks: 14 / 16 PASS
- Release status: **BLOCKED**

| Gate | Result |
|---|---:|
| source_public_inventory | PASS |
| keyword_map_source_sync | PASS |
| keyword_map_no_drift_after_sync | PASS |
| source_metadata_og_94 | PASS |
| ayat_ownership_source | PASS |
| quran_progress_source | PASS |
| live_103_url_crawl | PASS |
| live_hreflang_94 | PASS |
| live_keyword_map_94 | PASS |
| live_metadata_og_94 | FAIL |
| live_reflection_og_94 | PASS |
| live_schema_94 | PASS |
| live_internal_links_94 | PASS |
| live_post_dedup_serp_12 | FAIL |
| live_reader_regression | PASS |
| live_homepage_progress | PASS |

## Blocking failures

- **live_metadata_og_94** — {"live_checked": 94, "http_200_count": 94, "pass_count": 86, "fail_count": 8, "og_image_count": 94, "overall_pass": false}
- **live_post_dedup_serp_12** — {"generated_at": "2026-09-23T08:11:49Z", "propagated": true, "propagation_attempts": 1, "pages_checked": 12, "http_200": 12, "pass_count": 11, "fail_count": 1, "owner_guard_issues": [], "overall_pass": false}
