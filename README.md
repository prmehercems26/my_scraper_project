# Books to Scrape — Book Discovery

This repository contains the Books to Scrape project: a Flask web app that collects book information, saves selected fields to Supabase, and presents the results in an interactive browser interface.

## Purpose

The app demonstrates a small data-collection workflow: retrieve book listings, save structured book data in a database, and let a user browse and filter the results.

## Data collection

The app requests the catalog at [Books to Scrape](https://books.toscrape.com/), then extracts each selected book's title, GBP price, availability, cover image URL, and product-page URL. It fetches each product page to obtain a short description snippet for the results page. The number of books can be set from 1 to 50; the current implementation reads from the catalog's first page.

## Data persistence

The app inserts the title, price, availability, image URL, and product URL into the `public.books` table in Supabase. Supabase is used to keep the scraped records beyond the current browser session. Descriptions are returned to the browser for display but are intentionally not inserted, so the app remains compatible with an existing table that does not have a `description` column. Each scrape adds rows; it does not deduplicate earlier results.

## User interaction

1. Open the app and enter a Supabase project URL, publishable/anon key, and database password.
2. Choose how many books to retrieve and select **Find books**.
3. Browse the returned cards or use **Search books by name** to filter the current results.
4. Select **Supabase settings** to update the connection.

The project URL and publishable/anon key are saved in browser local storage. The database password is kept in page memory only and must be entered again after a reload.

## Setup and configuration

### Requirements

- Python 3.10 or newer
- A Supabase project
- Internet access to Books to Scrape and Supabase

### Install and run

Open PowerShell in this repository:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, allow it for the current terminal session and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Open <http://127.0.0.1:5000>. Supabase credentials are entered in the app; no local `.env` file is required. Use only a publishable key (or legacy anon key), never a secret or service-role key. The database setup uses the EU-West Supavisor transaction pooler on port `6543`; the username is derived from the project URL. If using a project in another region, update `DATABASE_POOLER_HOST` in `app.py`.

On the first insert, if the table or insert permissions are missing, the app attempts to create/configure `public.books` through the database pooler. That setup path requires the database password and network access to port 6543. Existing tables can be used without a schema change for the description feature.

## Short demo walkthrough

Run the app, connect a demo Supabase project, set the count to `5`, and select **Find books**. The page displays five book cards with cover images, prices, availability, and description snippets. Type part of a title into **Search books by name** to narrow the visible cards. The scraped records should also appear in the project's `public.books` table.

## API

`POST /api/scrape` accepts JSON:

```json
{
  "limit": 5,
  "supabase_url": "https://your-project.supabase.co",
  "supabase_key": "sb_publishable_placeholder",
  "database_password": "your-database-password"
}
```

The response contains the scraped books, including a description snippet. The password is sent to the local Flask backend for the request and is not stored in browser local storage.

## Learning and challenge

One important design lesson was to keep the data shown in the interface separate from the fields stored in the database. Product descriptions are available on individual detail pages, while the existing Supabase table may not have a matching column. Sending the new field to Supabase caused a schema mismatch, so descriptions are now returned for display without changing the existing table.

Another challenge was that Supabase's REST API and its PostgreSQL transaction pooler serve different purposes. Normal inserts use the REST API; the pooler is only needed for table setup or permission repair. Keeping those paths separate avoids requiring a database connection for every scrape.

## Limitations and assistance

### Limitations

- Only the first catalog page is searched, and the search field filters the books fetched for the current request; it does not search the full catalog or database history.
- Repeated scrapes append rows without deduplication. The app does not load previously saved rows into the interface.
- Book details depend on the external site's availability and page structure.
- The demo insert policy grants the `anon` role insert access. This is suitable only for a throwaway/demo project, not production data.
- Creating or repairing the table still depends on database access through the configured pooler. If that host or port is unreachable, setup cannot complete.
- The Flask development server is intended for local use only. Do not expose it directly to the public internet.
- This repository does not currently include an automated test suite.

### AI and external resources

GitHub Copilot assisted with implementation, debugging, and documentation. The scraped catalog and book descriptions come from [Books to Scrape](https://books.toscrape.com/). The app uses Flask, Requests, Beautiful Soup, psycopg2, and the Supabase Python client; see `requirements.txt`.

## Audit

See [`AUDIT.md`](AUDIT.md) for the sanitized publication-readiness review, findings, and remaining actions.
