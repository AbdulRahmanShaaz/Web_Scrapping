# Web Scraping Practice Projects

Small Python web scraping scripts for practicing `requests`, BeautifulSoup, CSV/JSON output, image downloading, and simple scheduled data collection.

## Scripts

- `scrapping_wikki_headings.py` scrapes H2 headings from the Python Wikipedia page.
- `hacker_news_csv.py` saves the top Hacker News story titles and links to CSV.
- `MultiPage_Scrapping.py` scrapes book titles and prices from Books to Scrape across multiple pages.
- `Download_image_rawCode.py` downloads sample book cover images from Books to Scrape.
- `generate_images_quotes.py` turns quotes from Quotes to Scrape into PNG images.
- `day_08.py` and `crypto_price_tracker.py` fetch cryptocurrency market data from CoinGecko.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run Examples

```bash
python scrapping_wikki_headings.py
python hacker_news_csv.py
python MultiPage_Scrapping.py
python Download_image_rawCode.py
python generate_images_quotes.py
```

Some scripts create output files such as CSV, JSON, images, or local databases. Those generated files are ignored by git.

## Notes

Please scrape politely: respect each website's terms, use reasonable request rates, and avoid sending unnecessary traffic.
