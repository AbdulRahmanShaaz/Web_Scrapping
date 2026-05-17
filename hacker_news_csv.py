import argparse
import csv
import logging
from pathlib import Path

import requests
from bs4 import BeautifulSoup

DEFAULT_URL = "https://news.ycombinator.com/"
DEFAULT_OUTPUT_FILE = "hn_top20.csv"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
TIMEOUT = 10


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def fetch_top_posts(session: requests.Session, url: str, limit: int) -> list[dict[str, str]]:
    response = session.get(url, timeout=TIMEOUT)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    post_links = soup.select("span.titleline > a")[:limit]

    posts = [
        {"title": post.get_text(strip=True), "link": post["href"]}
        for post in post_links
    ]

    logging.info("Fetched %d Hacker News posts", len(posts))
    return posts


def save_to_csv(posts: list[dict[str, str]], output_path: Path) -> None:
    if not posts:
        logging.warning("No posts available to save.")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(posts)

    logging.info("Saved Hacker News data to %s", output_path)


def main() -> int:
    configure_logging()

    parser = argparse.ArgumentParser(description="Scrape top Hacker News stories and export them to CSV.")
    parser.add_argument("--limit", type=int, default=20, help="Number of stories to fetch")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_FILE, help="CSV output file")
    args = parser.parse_args()

    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        posts = fetch_top_posts(session, DEFAULT_URL, args.limit)
        save_to_csv(posts, Path(args.output))
    except requests.RequestException as exc:
        logging.error("Failed to fetch Hacker News data: %s", exc)
        return 1
    except Exception as exc:
        logging.error("Unexpected error: %s", exc)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


