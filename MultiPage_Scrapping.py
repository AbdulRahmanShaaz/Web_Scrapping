import argparse
import json
import logging
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
START_PAGE = "catalogue/page-1.html"
DEFAULT_OUTPUT_FILE = "output.json"
DEFAULT_TARGET_COUNT = 70
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
TIMEOUT = 10


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def fetch_page(session: requests.Session, url: str) -> str:
    response = session.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    logging.info("Fetched page: %s", url)
    return response.text


def parse_books(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for article in soup.select("article.product_pod"):
        title_tag = article.select_one("h3 > a")
        price_tag = article.select_one("p.price_color")

        title = title_tag["title"].strip() if title_tag else "N/A"
        price = price_tag.get_text(strip=True) if price_tag else "N/A"

        books.append({"title": title, "price": price})
    return books


def find_next_page(html: str, current_url: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    next_link = soup.select_one("li.next > a")
    if not next_link:
        return None
    return urljoin(current_url, next_link["href"])


def save_results(data: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
    logging.info("Saved %d records to %s", len(data), output_path)


def scrape_books(target_count: int) -> list[dict[str, str]]:
    session = requests.Session()
    session.headers.update(HEADERS)

    current_page = urljoin(BASE_URL, START_PAGE)
    visited = set()
    collection: list[dict[str, str]] = []

    while current_page and len(collection) < target_count:
        if current_page in visited:
            logging.warning("Detected repeat page %s, stopping to avoid loop", current_page)
            break

        visited.add(current_page)
        logging.info("Scraping page: %s", current_page)

        html = fetch_page(session, current_page)
        books = parse_books(html)
        if not books:
            logging.warning("No books found on page: %s", current_page)
            break

        collection.extend(books)
        current_page = find_next_page(html, current_page)

    return collection[:target_count]


def main() -> int:
    configure_logging()
    parser = argparse.ArgumentParser(description="Scrape book titles and prices from books.toscrape.com.")
    parser.add_argument("--limit", type=int, default=DEFAULT_TARGET_COUNT, help="Maximum number of books to collect")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_FILE, help="Output JSON file path")
    args = parser.parse_args()

    try:
        books = scrape_books(args.limit)
        if not books:
            logging.error("No book data was collected.")
            return 1
        save_results(books, Path(args.output))
    except requests.RequestException as exc:
        logging.error("Request failed: %s", exc)
        return 1
    except Exception as exc:
        logging.error("Unexpected error: %s", exc)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())