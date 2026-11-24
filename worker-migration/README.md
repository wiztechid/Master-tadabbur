# TadabburLife Worker Migration

GitHub remains the versioned source of truth. Cloudflare Workers Static Assets will serve the public website after its preview and release gates pass.

## Current staging status

- The staging branch contains a strict public asset allowlist and a GitHub Actions build gate.
- SOP, QC logs, SEO governance, keyword research, ownership audits, drafts, and archival master files stay out of the public bundle.
- Cloudflare Workers Build configuration is not yet attached to the Worker. The Cloudflare plugin connection can inspect and edit Worker resources, but cannot create the dedicated API token required by Workers Builds.
- No custom domain or DNS route is configured by this migration. The existing site remains on its current host.

## Public asset boundary

The build script includes the public homepage, legal pages, all 51 Indonesian and 51 English session pages, reader modules, stylesheet, public reflection cards, sitemap, robots, and ads.txt. It excludes internal SOP and authoring materials.

## Release flow

1. Attach a dedicated Cloudflare Workers Build credential and configure branch previews for this repository.
2. Require the allowlisted bundle build and existing content/QC checks to pass.
3. Compare the Worker preview against current production, including all 102 public session URLs, reader behavior, sitemap, canonical tags, and mobile layout.
4. Merge only after preview parity; deploy the main branch to the Worker’s workers.dev address first.
5. Configure the custom domain only after the production Worker and rollback path have been verified.

The admin authoring interface and dedicated D1 draft database are a separate follow-on phase. Admin publishing should create a GitHub branch/PR and preserve the same QC and release gates; it must not publish straight to production.
