# Web Scrapping Suite

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI Status](https://github.com/AbdulRahmanShaaz/Web_Scrapping/actions/workflows/ci.yml/badge.svg)](https://github.com/AbdulRahmanShaaz/Web_Scrapping/actions)

A polished collection of professional web scraping solutions with modern CLI usage, reusable HTTP sessions, structured exports, and production-ready error handling.

## 🎯 Features

- **Multi-source data collection** from Wikipedia, Hacker News, public APIs, and e-commerce sites
- **Command-line interfaces** for each scraper using `argparse`
- **Structured output formats**: CSV, JSON, PNG images, and SQLite storage
- **Pagination handling** for multi-page scraping
- **API integration** (CoinGecko, public web APIs)
- **Image generation** with Pillow and HTML parsing
- **Robust logging and error handling**
- **GitHub Actions CI** workflow included for dependency install and lint verification

## 📋 Project Structure

```
├── scrapping_wikki_headings.py      # Wikipedia H2 headings extraction
├── hacker_news_csv.py               # Top stories → CSV export
├── MultiPage_Scrapping.py           # Multi-page pagination scraper
├── Download_image_rawCode.py        # Book cover image downloader with retry
├── generate_images_quotes.py        # Quote → PNG image generator
├── crypto_price_tracker.py          # Live crypto prices from CoinGecko API
├── day_08.py                        # Practice example script
├── requirements.txt                 # Project dependencies
├── README.md                        # This file
├── LICENSE                          # MIT License
└── .github/workflows/ci.yml         # GitHub Actions CI pipeline
```

## 🚀 Quick Start

### Prerequisites
- Python 3.6+
- pip or pipenv

### Installation

```bash
# Clone the repository
git clone https://github.com/AbdulRahmanShaaz/Web_Scrapping.git
cd Web_Scrapping

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 📚 Usage Examples

### Wikipedia Headings Scraper
Extract H2 headings from Wikipedia pages:
```bash
python scrapping_wikki_headings.py --url https://en.wikipedia.org/wiki/Web_scraping
```

### Hacker News Top Stories
Fetch top Hacker News stories and export to CSV:
```bash
python hacker_news_csv.py --limit 20 --output hn_top20.csv
```

### Multi-Page Books Scraper
Scrape book data across multiple pages with pagination:
```bash
python MultiPage_Scrapping.py --limit 70 --output output.json
```

### Download Book Covers
Download book cover images with a clean save location:
```bash
python Download_image_rawCode.py --output-dir web_scrapping/images
```

### Generate Quote Images
Convert quotes into styled PNG images:
```bash
python generate_images_quotes.py --count 5 --output-dir web_scrapping/quotes
```

### Crypto Price Tracker
Fetch live cryptocurrency prices and store them in SQLite:
```bash
python crypto_price_tracker.py --run-once
python crypto_price_tracker.py --interval 60 --plot bitcoin
```

## 🔧 Technical Details

### Libraries Used
- **requests** - HTTP requests & session reuse
- **BeautifulSoup4** - HTML parsing
- **Pillow (PIL)** - Image creation and styling
- **matplotlib** - Plotting crypto price history
- **schedule** - periodic background polling
- **sqlite3** - persistent price storage
- **csv** / **json** - structured exports

### Key Patterns Implemented
- HTML parsing with CSS selectors
- CLI-driven workflows using `argparse`
- Reusable `requests.Session` objects and headers
- Pagination & loop protection
- Structured data export to CSV, JSON, images, and SQLite
- Graceful error handling, logging, and HTTP status checks
- Responsible scraping with custom User-Agent and timeouts

## ⚖️ Ethical Scraping Guidelines

This project follows responsible web scraping practices:

✅ **Do:**
- Respect `robots.txt` and website ToS
- Use reasonable request rates (1-2 second delays)
- Include a User-Agent header
- Cache responses when possible
- Handle 429 (rate limit) responses gracefully

❌ **Don't:**
- Scrape sites that explicitly forbid it
- Hammer servers with rapid requests
- Bypass authentication or paywalls
- Republish scraped content without permission

## 📊 Output Files

Generated files are excluded from git (see `.gitignore`):
- `*.csv` - Data tables
- `*.json` - Structured data
- `scrapped_images/` - Downloaded images
- `quotes/` - Generated PNG images
- `__pycache__/` - Python cache

## 🔄 Development & CI/CD

This project includes:
- **GitHub Actions workflow** (`.github/workflows/ci.yml`) that:
  - Installs dependencies
  - Runs code quality checks (flake8)
  - Validates Python syntax

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Abdul Rahman Shaaz** - [GitHub Profile](https://github.com/AbdulRahmanShaaz)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/AbdulRahmanShaaz/Web_Scrapping/issues).

## 📞 Support

For questions or issues, please open a [GitHub issue](https://github.com/AbdulRahmanShaaz/Web_Scrapping/issues/new).

---

**Last Updated:** 2026-05-17
