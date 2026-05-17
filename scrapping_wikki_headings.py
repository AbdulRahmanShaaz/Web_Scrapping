import argparse
import logging
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

DEFAULT_URL = "https://en.wikipedia.org/wiki/Python_(programming_language)"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
TIMEOUT = 10


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def validate_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Invalid URL provided")
    return url


def fetch_html(url: str, session: requests.Session | None = None) -> str:
    session = session or requests.Session()
    session.headers.update(HEADERS)
    response = session.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    logging.info("Fetched page successfully: %s", url)
    return response.text


def parse_h2_headings(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    headings = [tag.get_text(strip=True) for tag in soup.find_all("h2") if tag.get_text(strip=True)]
    return headings


def main() -> int:
    configure_logging()

    parser = argparse.ArgumentParser(description="Scrape H2 headings from a Wikipedia page.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Wikipedia page URL to scrape")
    args = parser.parse_args()

    try:
        url = validate_url(args.url)
        html = fetch_html(url)
        headings = parse_h2_headings(html)
    except Exception as exc:
        logging.error("Failed to scrape headings: %s", exc)
        return 1

    logging.info("Found %d H2 headings", len(headings))
    for index, heading in enumerate(headings, start=1):
        print(f"{index:02d}. {heading}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())