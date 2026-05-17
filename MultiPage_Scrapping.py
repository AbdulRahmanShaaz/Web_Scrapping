import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
START_PAGE = "catalogue/page-1.html"
OUTPUT_FILE = "output.json"
TARGET_COUNT = 70


def scrape_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return [], None

    soup = BeautifulSoup(response.text, 'html.parser')

    books = []

    # ✅ Extract book data properly
    for article in soup.select('article.product_pod'):
        title_tag = article.select_one('h3 > a')
        title = title_tag['title'].strip() if title_tag else 'N/A'

        price_tag = article.select_one('p.price_color')
        price = price_tag.get_text(strip=True) if price_tag else 'N/A'

        books.append({
            "title": title,
            "price": price
        })

    # ✅ Get next page (OUTSIDE loop)
    next_link = soup.select_one('li.next > a')
    next_url = urljoin(url, next_link['href']) if next_link else None

    return books, next_url


def main():
    collection = []
    current_page = urljoin(BASE_URL, START_PAGE)

    visited = set()  # ✅ prevent infinite loops

    while current_page and len(collection) < TARGET_COUNT:
        if current_page in visited:
            break
        visited.add(current_page)

        print(f"📄 Scraping: {current_page}")

        books, next_page = scrape_page(current_page)

        if not books:
            print("⚠️ No books found, stopping...")
            break

        collection.extend(books)
        print(f"✅ Collected so far: {len(collection)}")

        current_page = next_page

    # ✅ Trim to exact count
    collection = collection[:TARGET_COUNT]

    print(f"\n🎯 Total books collected: {len(collection)}")

    # ✅ Save JSON safely
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(collection, f, indent=2, ensure_ascii=False)
        print(f"💾 Data saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")


if __name__ == "__main__":
    main()