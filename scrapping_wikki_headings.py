import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Python_(programming_language)"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def get_h2_headers(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    h2_tags = soup.find_all("h2")

    headings = [
        h2.get_text(strip=True)
        for h2 in h2_tags
        if h2.get_text(strip=True)  # avoid empty headings
    ]

    return headings


if __name__ == "__main__":
    h2_headers = get_h2_headers(URL)

    print("\n📌 H2 Headings:\n")
    for i, header in enumerate(h2_headers, 1):
        print(f"{i}. {header}")