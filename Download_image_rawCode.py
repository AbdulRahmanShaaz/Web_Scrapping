import argparse
import logging
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
DEFAULT_OUTPUT_DIR = Path("web_scrapping/images")
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
TIMEOUT = 10


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def sanitize_filename(filename: str) -> str:
    sanitized = re.sub(r"[^\w\-_. ]", "", filename)
    return sanitized.strip().replace(" ", "_")


def fetch_html(session: requests.Session, url: str) -> str:
    response = session.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    logging.info("Fetched page: %s", url)
    return response.text


def parse_book_data(html: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for book in soup.select("article.product_pod")[:10]:
        title_tag = book.select_one("h3 > a")
        img_tag = book.select_one("img")

        title = title_tag["title"].strip() if title_tag else "untitled"
        image_path = img_tag["src"] if img_tag else ""
        books.append((title, image_path))
    return books


def download_image(session: requests.Session, image_url: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    response = session.get(image_url, timeout=TIMEOUT, stream=True)
    response.raise_for_status()

    with output_path.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                handle.write(chunk)
    logging.info("Saved image: %s", output_path)


def scrape_and_download_images(base_url: str, output_dir: Path) -> None:
    session = requests.Session()
    session.headers.update(HEADERS)

    html = fetch_html(session, base_url)
    books = parse_book_data(html)

    if not books:
        logging.warning("No books found on page: %s", base_url)
        return

    for index, (title, relative_src) in enumerate(books, start=1):
        logging.info("Processing book %d: %s", index, title)
        image_url = urljoin(base_url, relative_src)
        file_name = sanitize_filename(title) or f"book_{index}"
        output_path = output_dir / f"{file_name}.jpg"
        download_image(session, image_url, output_path)

    logging.info("Completed downloading %d images", len(books))


def main() -> int:
    configure_logging()
    parser = argparse.ArgumentParser(description="Download book cover images from books.toscrape.com.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory to save downloaded images")
    args = parser.parse_args()

    try:
        scrape_and_download_images(BASE_URL, Path(args.output_dir))
    except requests.RequestException as exc:
        logging.error("Network request failed: %s", exc)
        return 1
    except Exception as exc:
        logging.error("Unexpected error: %s", exc)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())