# Little Play Lab - portable source code

This package is a standalone Node.js / Next.js version of the colourful kids printable website. It runs independently of ChatGPT Sites. It includes the complete UI, server endpoints, SQLite database adapter, schema migration, original illustration assets, protected PDF bytes, original PDF files and PDF generation scripts.

## Included

- Responsive home page, searchable activity library, previews and age/category filters
- Parent sign up / sign in / sign out, salted password hashes and HttpOnly sessions
- Persistent accounts, orders and download history
- Six original packs, 19 printable A4 pages (three free packs, 10 free pages)
- Illustrated flower counting, garden colouring, animal memory cards and more
- Starter, INR 199 Play Pack, INR 999 Annual Explorer pricing
- Razorpay server-created orders, signature verification and captured-payment checks
- Signed captured-payment/refund webhooks
- Dockerfile and Docker Compose deployment configuration

## Run locally (Node.js 24 or newer)

```sh
npm ci
npm run dev
```

Open http://localhost:3000. SQLite initializes itself in `data/play-lab.sqlite` on the first account API request. The migration files in `drizzle/` are applied once and tracked in the local database. No external database account is required.

For a production build:

```sh
npm run build
npm start
```

## Docker deployment

```sh
cp .env.example .env
# Edit .env with your payment settings when you are ready.
docker compose up -d --build
```

The website runs on port 3000. The `play_data` volume keeps account data outside the application container. Do not delete this volume during upgrades. Set up HTTPS with your own domain and reverse proxy before accepting real customer registrations. Preserve the original Host header in your reverse proxy configuration so origin checks can validate browser requests.

## AWS deployment path

This version can run on one AWS Lightsail Linux **instance** or EC2 Linux instance with Docker and durable disk storage. Upload the extracted project, install Docker and its Compose plugin, and use the Docker command above. Add a static IP/domain and a reverse proxy with HTTPS. Open ports 80/443 publicly and keep the application/database access restricted to the server.

SQLite is a single-instance database in this implementation. Keep a persistent disk/volume and backups. Do not run independent replicas using separate SQLite files. Moving to AWS App Runner, Lambda, managed container services or multiple instances requires adapting the database to durable shared storage such as PostgreSQL/RDS. This package does not claim compatibility with those deployments without that change. AWS infrastructure has not been provisioned or tested in your account.

AWS references:
- https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-faq-block-storage.html
- https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-connecting-container-service-to-database.html

For backups, use SQLite's online backup API or a consistent disk snapshot; copying only the live `.sqlite` file while WAL writes are running can miss data.

## Razorpay setup

Set these server secrets in `.env` for Docker or `.env.local` for local Next.js:

```text
RAZORPAY_KEY_ID=your_test_key_id
RAZORPAY_KEY_SECRET=your_test_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
```

Never put secrets in `NEXT_PUBLIC_*` variables or commit real credentials. Configure automatic payment capture in Razorpay. Configure a webhook URL of `https://your-domain/api/webhook` for `payment.captured` and `refund.processed`, with the same webhook secret.

A payment is accepted only after server-side verification of signature, order ownership, captured status, amount and INR currency. Captured-payment webhooks recover a purchase if checkout closes before the browser callback. Repeated callbacks do not grant repeated access periods. A full refund event revokes the corresponding purchase.

Test payments, failed/cancelled checkout and webhooks with test-mode keys before switching to live credentials. No live transactions have been tested. Checkout shows a clear unavailable message until keys are supplied; free account downloads work without them.

## Pricing and content edits

`lib/catalog.ts` contains titles, categories, ages, page counts and payment amounts. Amounts use paise. Update UI pricing descriptions in `app/page.tsx` when changing plans. Annual Explorer currently provides 365 days after a one-time payment with no automatic renewal; Play Pack has no expiry for the six current packs. It is not a recurring Razorpay Subscription.

PDFs are kept outside `public/`. Downloads are delivered only after a server session/entitlement check. Public first-page PNG previews are intentionally visible to everyone. To regenerate PDFs, install Python `reportlab`, `Pillow` and system Poppler, then run:

```sh
python3 scripts/content/create-pdfs.py
python3 scripts/content/embed-pdfs.py
```

The second command refreshes the embedded server PDF data. Do not expose `private-pdfs/` through a static web server.

## Before operating publicly

Replace provisional privacy/terms with your final operator details, support contact, refund policy and data deletion process. Password recovery and email verification have not been implemented. Add account recovery before taking ongoing customer purchases. Store no children's personal details in these adult accounts.

Sessions expire after seven days. Authentication attempts are limited by email and IP. Set `TRUST_PROXY=true` only if your reverse proxy removes incoming client-supplied `X-Forwarded-For` values and writes a trusted client IP. Otherwise the server-wide IP attempt bucket is deliberately conservative.

## Validation

The production Next.js build and TypeScript validation were run. Account, download protections and payment-not-configured paths were tested. Payment-provider transactions, Docker image execution and deployment in your AWS account still need testing after credentials and hosting are configured.

Original generated illustrations are included under `public/art/`. No customer data, passwords or payment credentials are included in this source package.
