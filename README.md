# Web Scrapping Suite

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI Status](https://github.com/AbdulRahmanShaaz/Web_Scrapping/actions/workflows/ci.yml/badge.svg)](https://github.com/AbdulRahmanShaaz/Web_Scrapping/actions)

A comprehensive collection of professional-grade web scraping solutions showcasing real-world data extraction patterns, multi-page pagination, API integration, and file format conversion.

## 🎯 Features

- **Multi-source data collection** from Wikipedia, Hacker News, public APIs, and e-commerce sites
- **Multiple output formats**: CSV, JSON, PNG images
- **Pagination handling** for large datasets
- **API integration** (CoinGecko, public web APIs)
- **Image processing** with PIL
- **Error handling & retry logic**
- **Professional git history** with 11+ semantic commits
- **GitHub Actions CI/CD** pipeline included

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
python scrapping_wikki_headings.py
```

### Hacker News Top Stories
Fetch top Hacker News stories and export to CSV:
```bash
python hacker_news_csv.py
# Output: hn_top20.csv
```

### Multi-Page Books Scraper
Scrape book data across multiple pages with pagination:
```bash
python MultiPage_Scrapping.py
# Demonstrates: pagination, data aggregation, structured output
```

### Download Book Covers
Download book cover images with automatic retry:
```bash
python Download_image_rawCode.py
# Output: scrapped_images/ folder
```

### Generate Quote Images
Convert quotes to PNG images with custom styling:
```bash
python generate_images_quotes.py
# Output: quotes/ folder with PNG files
```

### Crypto Price Tracker
Fetch live cryptocurrency prices from CoinGecko API:
```bash
python crypto_price_tracker.py
python day_08.py
```

## 🔧 Technical Details

### Libraries Used
- **requests** - HTTP requests & API calls
- **BeautifulSoup4** - HTML parsing
- **Pillow (PIL)** - Image processing
- **csv** - Data export
- **json** - JSON serialization

### Key Patterns Implemented
- HTML parsing with CSS selectors
- Pagination & session management
- API integration & response handling
- File I/O (CSV, JSON, images)
- Error handling & logging
- Rate limiting (polite scraping)

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
