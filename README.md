# ShopeSphere

ShopeSphere is a Django e-commerce app with product browsing, cart/checkout,
order flow, and its own authentication (`authent`) app.

## Project structure

```
ShopeSphere/
├── authent/                     # registration, login, profile
├── base/                        # products, cart, checkout, orders
│   └── management/commands/seed_data.py   # demo-data seeding command
├── myproject/                   # settings, root urls, wsgi/asgi
├── static/                      # css, js, images (source, pre-collectstatic)
│   └── images/default.png        # placeholder product image
├── templates/                    # shared base templates (nav, footer, main)
├── db.sqlite3                    # local-only database (see Database section)
├── manage.py
├── requirements.txt
├── .gitignore
└── .github/workflows/django-tests.yml   # CI: runs the test suite on every push/PR
```

## Local development

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env            # then edit .env, or just export the vars
python manage.py migrate
python manage.py runserver
```

## Seeding demo data

A fresh database (especially a new Postgres one for production) starts
empty. `base/management/commands/seed_data.py` adds sample catalog data so
there's something to click through right away:

```bash
python manage.py migrate
python manage.py seed_data
```

This creates:
- ~12 sample `Product`s across a few categories (some flagged `sale`/`trending`
  so the home page filters have something to show), matched/updated by name
  so it's **safe to run more than once** — it won't create duplicates.
- One `Delivery` pricing row (used by the checkout/payment view), only if
  one doesn't already exist.
- A demo login: **username `demo` / password `demo1234`** — matches the
  app's existing (plaintext-password) login logic, see "Security notes"
  below, so it's for kicking the tyres, not for production use. Change or
  delete it before letting real traffic in.

Run `python manage.py seed_data --flush` to delete the seeded products and
delivery row and re-create them from scratch (your own data — real users,
carts, orders, addresses — is never touched by this command).

Product images use a generated `static/images/default.png` placeholder
(the model's `ImageField` default) since no real product photos were
supplied — swap in real images via Django admin once deployed.

Run this the same way against production: set `DATABASE_URL` locally,
then run `python manage.py migrate && python manage.py seed_data`. It's not
run automatically during the Vercel build, since re-seeding on every deploy
isn't something you generally want happening unattended.

## Running tests

```bash
python manage.py test
```

Basic tests were added for both apps:
- `base/tests.py` — product listing, search filtering, login-gated cart, add-to-cart, and the `seed_data` command (creates data, and is idempotent on a second run).
- `authent/tests.py` — registration (incl. duplicate-username rejection), login success/failure, logout.

These also run automatically in CI (see below).

## Continuous integration

`.github/workflows/django-tests.yml` runs on every push/PR to `main`: it installs
dependencies, runs `manage.py check`, checks for missing migrations, and runs
the test suite. Check the **Actions** tab on GitHub after you push.

## Deploying to Vercel

### 1. Required environment variables

Set these in **Vercel → Project → Settings → Environment Variables** (see
`.env.example` for details):

| Variable | Required | Notes |
|---|---|---|
| `SECRET_KEY` | Yes | Generate with `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DEBUG` | Recommended | Set to `False` in production |
| `DATABASE_URL` | **Yes, effectively** | See "Database" below |
| `ALLOWED_HOSTS` | Optional | `.vercel.app` and the deployment's own `VERCEL_URL` are already allowed automatically |
| `CSRF_TRUSTED_ORIGINS` | Optional (needed for a custom domain) | `https://*.vercel.app` is already trusted automatically |

### 2. Database — action required before this will work on Vercel

Vercel's serverless filesystem is **read-only and ephemeral**, so the
committed `db.sqlite3` cannot be written to in production (writes will
error or silently vanish between requests). You must provision a managed
Postgres database and set `DATABASE_URL`:

- [Vercel Postgres](https://vercel.com/docs/storage/vercel-postgres) (via Neon, integrated in the Vercel dashboard), or
- [Neon](https://neon.tech) / [Supabase](https://supabase.com) directly (both have free tiers)

Then, from your local machine (with `DATABASE_URL` exported), run:

```bash
python manage.py migrate
python manage.py createsuperuser
```

`settings.py` already falls back to SQLite automatically when `DATABASE_URL`
isn't set, so local development is unaffected.

### 3. Static and media files

- CSS/JS under `static/` are collected by `build_files.sh` (runs
  `collectstatic`) during the Vercel build and served via WhiteNoise.
- Product images uploaded through Django admin (`MEDIA_ROOT`) hit the same
  read-only-filesystem problem as SQLite — new uploads won't persist on
  Vercel. Images already in the repo at deploy time will still be served
  fine. If you need users/admins to upload images after deploying, swap the
  `ImageField` storage backend for something like `django-storages` +
  S3/Cloudflare R2/Cloudinary.

### 4. Deploy

```bash
npm i -g vercel     # if you don't have the CLI
vercel login
vercel               # first deploy / link project
vercel --prod         # promote to production
```

Or just import the GitHub repo in the Vercel dashboard — it will pick up
`vercel.json` and `build_files.sh` automatically on every push to `main`.

## Security notes (worth fixing, out of scope for this deploy pass)

- `authent/views.py` currently stores and compares **plaintext passwords**
  (`User.objects.create(..., password=password)` and `data.password==password`)
  instead of Django's `User.objects.create_user()` / `authenticate()`, which
  hash passwords. This works, but is a real security risk — anyone with
  database access sees raw passwords. Recommend switching to
  `create_user()`/`authenticate()` before going live with real users.
- `SECRET_KEY` has a hard-coded fallback in `settings.py` for convenience —
  make sure the `SECRET_KEY` environment variable is actually set in Vercel
  so the fallback is never used in production.