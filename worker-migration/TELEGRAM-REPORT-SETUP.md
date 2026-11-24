# Telegram publication report setup

The Worker publish workflow sends a private report to **@WissWebBot** after each main-branch Worker deployment attempt. The report includes success/failure, the Worker URL, commit short SHA, and the GitHub Actions run.

## Required repository secrets

In GitHub, open **Settings → Secrets and variables → Actions → New repository secret** and add:

- `CLOUDFLARE_API_TOKEN`: account-scoped token with the Cloudflare **Edit Cloudflare Workers** permission.
- `CLOUDFLARE_ACCOUNT_ID`: Cloudflare account ID for the TadabburLife Worker.
- `TELEGRAM_BOT_TOKEN`: token for **@WissWebBot**. Never put this value in a commit or chat message.
- `TELEGRAM_CHAT_ID`: numeric ID of the owner's private chat with the bot.

Open **@WissWebBot** in Telegram and press **Start** before using the private chat. Configure the bot token and chat ID only in GitHub Actions secrets. If the Telegram secrets are missing, deployment may still succeed, but the report step will be skipped and logged as a warning.

## Deployment behavior

- A push to `main` that changes public site content or Worker build/config files runs the publication workflow.
- The workflow reruns Qur'an progress, ayat ownership, bilingual reader parity, session-template, and public bundle checks before deployment.
- The first deployment target is `https://tadabburlife-site.wiztechid.workers.dev/`. The Worker adds `X-Robots-Tag: noindex, nofollow` on `workers.dev` so it remains a validation endpoint.
- This does not move `tadabburlife.com` or change DNS. Production-domain cutover remains a separate release after Worker preview parity and rollback verification.
- The Telegram step runs after a success or failure and cannot roll back an already completed deployment.
