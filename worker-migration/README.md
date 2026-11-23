# TadabburLife Worker Migration

This migration keeps GitHub as the versioned source of truth and uses Cloudflare Workers Static Assets for the public website. The domain is not routed to this Worker by this branch.

## Public asset boundary

The build script creates `dist/` from a strict allowlist:
- Public root page, legal pages, session pages, stylesheet, favicons, public reflection cards, sitemap, robots, and ads.txt.
- Reader modules named `sessions-*.html` and `quran-progress.json`.

Internal SOP, QC logs, SEO governance, keyword research, ownership audit data, drafts, and archival master files remain in GitHub and are excluded from the public Worker bundle.

## Release flow

1. Cloudflare Workers Builds creates branch previews on `workers.dev`.
2. Existing repository QC gates remain required.
3. Merge only after preview parity checks.
4. The main branch deploys the Worker to its `workers.dev` address.
5. Attach `tadabburlife.com` only after production parity and rollback checks are complete.

The admin authoring interface and dedicated D1 draft database are a later phase. Publishing from admin should create a GitHub branch/PR; it must not bypass the repository QC and release gates.
