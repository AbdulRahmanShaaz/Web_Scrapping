import argparse
import logging
import textwrap
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

BASE_URL = "https://quotes.toscrape.com/"
DEFAULT_OUTPUT_DIR = Path("web_scrapping/quotes")
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
TIMEOUT = 10


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def fetch_quotes(session: requests.Session, maximum: int) -> list[tuple[str, str]]:
    response = session.get(BASE_URL, timeout=TIMEOUT)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    quote_cards = soup.select("div.quote")[:maximum]

    quotes = []
    for card in quote_cards:
        text = card.select_one("span.text").get_text(strip=True).strip("“”")
        author = card.select_one("small.author").get_text(strip=True)
        quotes.append((text, author))

    logging.info("Fetched %d quotes", len(quotes))
    return quotes


def create_image(text: str, author: str, output_path: Path) -> None:
    width, height = 900, 480
    background_color = "#f8f4e6"
    text_color = "#222222"
    accent_color = "#4a5568"

    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    wrapped_text = textwrap.fill(text, width=56)
    author_text = f"— {author}"

    current_y = 80
    draw.text((60, current_y), wrapped_text, font=font, fill=text_color)
    current_y += wrapped_text.count("\n") * 18 + 60
    draw.text((60, current_y), author_text, font=font, fill=accent_color)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    logging.info("Saved quote image: %s", output_path)


def main() -> int:
    configure_logging()
    parser = argparse.ArgumentParser(description="Generate styled quote images from quotes.toscrape.com.")
    parser.add_argument("--count", type=int, default=5, help="Number of quotes to fetch")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory to save PNG images")
    args = parser.parse_args()

    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        quotes = fetch_quotes(session, args.count)
    except requests.RequestException as exc:
        logging.error("Failed to fetch quotes: %s", exc)
        return 1

    output_dir = Path(args.output_dir)
    for index, (text, author) in enumerate(quotes, start=1):
        filename = output_dir / f"quote_{index:02d}.png"
        create_image(text, author, filename)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())