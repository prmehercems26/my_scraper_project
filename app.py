import os

from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
import psycopg2

app = Flask(__name__)

# --- Configuration (Update these with your details) ---

# 1. Database Connection String (for creating the table)
# Set DATABASE_URL to a PostgreSQL or Supabase pooler connection string.
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Supabase API Credentials (for inserting and reading data)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client | None = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def ensure_table_exists():
    """Connects directly to PostgreSQL to ensure the table exists before scraping."""
    conn = None
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title TEXT,
                price_gbp NUMERIC,
                availability TEXT
            );
            ALTER TABLE books DISABLE ROW LEVEL SECURITY;
        """)
        conn.commit()
    except Exception as e:
        print(f"Database setup error: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

@app.route('/')
def home():
    # Serves the frontend UI
    return render_template('index.html')

@app.route('/api/scrape', methods=['POST'])
def run_scraper():
    # 1. Ensure the table exists in Supabase
    if not supabase:
        return jsonify({
            "success": False,
            "error": "Supabase credentials are not configured"
        }), 500

    try:
        ensure_table_exists()
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    # 2. Get the requested number of books from the frontend
    data = request.json
    limit = int(data.get('limit', 5))

    # 3. Scrape the website
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"success": False, "error": "Failed to fetch page"}), 500

    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    
    scraped_data = []
    for index, book in enumerate(books):
        if index >= limit:
            break
            
        title = book.h3.a['title']
        price = float(book.find('p', class_='price_color').text.replace('Â£', '').replace('£', ''))
        availability = book.find('p', class_='instock availability').text.strip()
        
        scraped_data.append({
            'title': title,
            'price_gbp': price,
            'availability': availability
        })

    # 4. Push the live data to Supabase
    if scraped_data:
        try:
            supabase.table("books").insert(scraped_data).execute()
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    # 5. Return the data to the frontend to display
    return jsonify({"success": True, "data": scraped_data})

if __name__ == '__main__':
    app.run(debug=True)