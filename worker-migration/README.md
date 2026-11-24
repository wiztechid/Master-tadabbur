# TadabburLife Worker Migration

GitHub remains the versioned source of truth. Cloudflare Workers Static Assets will serve the public website after its preview and release gates pass.

## Current staging status

- The staging branch contains a strict public asset allowlist and a GitHub Actions build gate.
- Internal SOP, QC logs, SEO governance, keyword research, ownership audits, drafts, and archival master files stay out of the public bundle.
- Session content prepared for Worker publication must follow [the Worker Session Publication Standard](SESSION-PUBLICATION-STANDARD.md), together with the Master SOP and publication regression SOP.
- The Worker preview is live at `https://tadabburlife-preview-proxy.wiztechid.workers.dev/`; it serves allowlisted paths from the staging branch, adds `noindex`, and does not touch production DNS.
- The new main-branch publish workflow builds and checks the allowlisted site, deploys it to the separate `tadabburlife-site.wiztechid.workers.dev` validation URL, and reports the result to the owner’s private Telegram chat. It requires the secrets listed in [Telegram report setup](TELEGRAM-REPORT-SETUP.md).
- No custom domain or DNS route is configured by this migration. The current public site remains on its existing host until Worker parity and rollback are verified.

## Public asset boundary

The build script includes the public homepage, legal pages, all 51 Indonesian and 51 English session pages, reader modules, stylesheet, public reflection cards, sitemap, robots, and ads.txt. It excludes internal SOP and authoring materials, including the Worker Session Publication Standard and Telegram setup documentation.

## Release flow

1. Configure the scoped Cloudflare and Telegram secrets listed in [Telegram report setup](TELEGRAM-REPORT-SETUP.md).
2. Require the existing content/QC checks and the Worker publication workflow checks to pass.
3. Compare the Worker validation URL with current production, including all 102 public session URLs, reader behavior, sitemap, canonical tags, and mobile layout.
4. Merge approved content to `main`; the Worker workflow checks and deploys the separate `workers.dev` validation site, then sends the private Telegram report.
5. Configure the custom domain only after the full preview parity and rollback path have been verified.

The admin authoring interface and dedicated D1 draft database remain a separate follow-on phase. Until then, content is edited through Git branches and PRs; the Worker does not accept direct content edits.
