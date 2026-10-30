# Book Scraper

A Flask web app that scrapes book titles, GBP prices, and availability from [Books to Scrape](https://books.toscrape.com/) and stores the results in a Supabase PostgreSQL database.

## Features

- Responsive browser interface styled for mobile viewing
- Interactive book cards with cover images and stock status
- Short product-description snippets and in-browser book-name search
- Loading states and animated result cards
- In-app Supabase connection setup; credentials stay in the current browser
- Configurable number of books to scrape
- Scraped results displayed in the browser
- Book data inserted into a Supabase `books` table
- Supabase `books` table integration using a publishable/anon key

## Requirements

- Python 3.10 or newer
- A Supabase project
- Internet access

## Installation

1. Open PowerShell in the project directory.

2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks script execution, allow scripts for the current terminal session:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

## Supabase Setup

The first time you open the app, enter the project URL, publishable/anon key, and database password. The URL and key are saved in browser local storage; later visits ask only for the database password.

The app tries to insert through the Supabase API first. Book descriptions are shown in the results but are not added to the existing database schema. If `public.books` is missing or Supabase reports that the `anon` role cannot insert, it connects through the existing EU-West transaction pooler on port `6543` to create the table or repair its insert grants and policy. The Postgres username is derived from the project URL; the password stays in page memory.

If you change Supabase projects or regions, update `DATABASE_POOLER_HOST` in `app.py` to that project's transaction pooler host.

## Security Warning

Never enter a Supabase **secret** or **service-role** key in the app. Those keys bypass Row Level Security. The app accepts only publishable keys and legacy anon JWTs. The demo insert policy allows anyone with the publishable/anon key to add rows, so use a throwaway/demo project; for production, replace it with authenticated-user policies and add Supabase Auth. Do not expose the Flask app over an untrusted network without HTTPS.

If a database password was ever committed to a public repository, rotate it in Supabase; deleting it from the latest source does not remove it from Git history.

## Running the App

Start the Flask development server:

```powershell
python app.py
```

Open <http://127.0.0.1:5000> in your browser.

Connect your Supabase project, enter a number from 1 to 50, and select **Find books**. The app requests books and their description snippets from `https://books.toscrape.com/`, inserts them into Supabase, and displays the results. Search the loaded results by book name using the search field. Use **Supabase settings** to update the connection.

## API Endpoint

### `POST /api/scrape`

Request body:

```json
{
  "limit": 5,
  "supabase_url": "https://your-project.supabase.co",
  "supabase_key": "sb_publishable_...",
  "database_password": "..."
}
```

Success response:

```json
{
  "success": true,
  "data": [
    {
      "title": "Book title",
      "price_gbp": 51.77,
      "availability": "In stock",
      "description": "A short preview of the book description..."
    }
  ]
}
```
