# Book Scraper

A Flask web app that scrapes book titles, GBP prices, and availability from [Books to Scrape](https://books.toscrape.com/) and stores the results in a Supabase PostgreSQL database.

## Features

- Responsive browser interface styled for mobile viewing
- Interactive book cards with cover images and stock status
- Loading states and in-browser filtering of scraped results
- Configurable number of books to scrape
- Scraped results displayed in the browser
- Book data inserted into a Supabase `books` table
- Automatic creation of the `books` table and PostgreSQL connection setup

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

## Supabase Configuration

Set these environment variables in PowerShell before starting the app:

```powershell
$env:DATABASE_URL = "postgresql://[REDACTED]"
$env:SUPABASE_URL = "https://your-project.supabase.co"
$env:SUPABASE_KEY = "your-supabase-key"
```

- `DATABASE_URL` should be the direct PostgreSQL connection or pooler URL for your database.
- `SUPABASE_URL` is shown in Supabase under **Project Settings > API**.
- `SUPABASE_KEY` should be an appropriate public or server key for the operations this app performs.

The app creates a table named `books` with these columns:

| Column | Type |
| --- | --- |
| `id` | Serial primary key |
| `title` | Text |
| `price_gbp` | Numeric |
| `availability` | Text |

## Security Warning

Do not commit database passwords or Supabase API keys to source control. Remove or replace any credentials already present in `app.py`, and rotate credentials in Supabase if they may have been exposed.

For a safer setup, move the credentials to environment variables and update `app.py` to read them with `os.getenv()`.

## Running the App

Start the Flask development server:

```powershell
python app.py
```

Open <http://127.0.0.1:5000> in your browser.

Enter a number from 1 to 50 and select **Scrape**. The app requests books from `https://books.toscrape.com/`, inserts them into Supabase, and displays the returned results.

## API Endpoint

### `POST /api/scrape`

Request body:

```json
{
  "limit": 5
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
      "availability": "In stock"
    }
  ]
}
```
