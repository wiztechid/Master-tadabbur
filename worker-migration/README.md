# TadabburLife Worker Migration

GitHub remains the versioned source of truth. Cloudflare Workers Static Assets will serve the public website after its preview and release gates pass.

## Current staging status

- The staging branch contains a strict public asset allowlist and a GitHub Actions build gate.
- SOP, QC logs, SEO governance, keyword research, ownership audits, drafts, and archival master files stay out of the public bundle.
- Session content prepared for Worker publication must follow [the Worker Session Publication Standard](SESSION-PUBLICATION-STANDARD.md), together with the Master SOP and publication regression SOP.
- A temporary preview Worker is live at `https://tadabburlife-preview-proxy.wiztechid.workers.dev/`. It serves the public allowlisted paths from the staging branch, adds `noindex`, and does not touch production DNS. This verifies routes and reader behavior but is not yet a self-contained static asset bundle. Cloudflare Workers Builds is still not configured because its required dedicated build credential is not available through the connected plugin scope.
- No custom domain or DNS route is configured by this migration. The existing site remains on its current host.

## Public asset boundary

The build script includes the public homepage, legal pages, all 51 Indonesian and 51 English session pages, reader modules, stylesheet, public reflection cards, sitemap, robots, and ads.txt. It excludes internal SOP and authoring materials, including the Worker Session Publication Standard.

## Release flow

1. Attach a dedicated Cloudflare Workers Build credential and configure branch previews for this repository.
2. Require the allowlisted bundle build and existing content/QC checks to pass.
3. Review every session against the Worker Session Publication Standard and compare the Worker preview against current production, including all 102 public session URLs, reader behavior, sitemap, canonical tags, and mobile layout.
4. Merge only after preview parity; deploy the main branch to the Worker’s workers.dev address first.
5. Configure the custom domain only after the production Worker and rollback path have been verified.

The admin authoring interface and dedicated D1 draft database are a separate follow-on phase. Admin publishing must create a GitHub branch/PR, preserve the same QC and release gates, and must not publish straight to production.
