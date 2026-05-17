import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import wget

BASE_URL = "https://books.toscrape.com/"
IMAGES_DIR = "web_scrapping/images"


def sanitize_filename(filename):
    return re.sub(r'[^\w\-_\. ]', '', filename).replace(' ', '_')


def download_image(image_url, title):
    try:
        print(f"🌐 Sending request to: {image_url}")

        response = requests.get(image_url, timeout=10, stream=True)
        response.raise_for_status()

        file_name = sanitize_filename(title) + ".jpg"
        file_path = os.path.join(IMAGES_DIR, file_name)

        print(f"📁 File name: {file_name}")
        print(f"📂 Saving to path: {file_path}")

        with open(file_path, 'wb') as f:
            print("🧩 Starting to write chunks...")

            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"✅ Image downloaded successfully: {title}")

    except Exception as e:
        print(f"❌ Error downloading image: {e}")


def scrape_and_download_images(url):
    print(f"🚀 Starting scraping from: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch page: {e}")
        return

    print("✅ Page fetched successfully")

    soup = BeautifulSoup(response.text, 'html.parser')
    print("🧠 Parsed HTML with BeautifulSoup")

    books = soup.select('article.product_pod')[:10]
    print(f"📚 Total books selected: {len(books)}")

    if not os.path.exists(IMAGES_DIR):
        print(f"📁 Creating directory: {IMAGES_DIR}")
        os.makedirs(IMAGES_DIR)
    else:
        print(f"📁 Directory already exists: {IMAGES_DIR}")

    for index, book in enumerate(books, start=1):
        print("\n" + "=" * 50)
        print(f"🔢 Processing book #{index}")

        title = book.h3.a['title']
        print(f"📖 Title: {title}")

        img_tag = book.find('img')
        if not img_tag:
            print("⚠️ No image tag found, skipping...")
            continue

        relative_image_url = img_tag['src']
        print(f"🔗 Relative image URL: {relative_image_url}")

        image_url = urljoin(BASE_URL, relative_image_url)
        print(f"🌍 Absolute image URL: {image_url}")

        file_name = sanitize_filename(title) + ".jpg"
        file_path = os.path.join(IMAGES_DIR, file_name)

        print(f"📝 Final file name: {file_name}")
        print(f"📂 Final file path: {file_path}")

        print(f"📥 Downloading image for: {title}")

        # download_image(image_url, title)
        wget.download(image_url, out=file_path)

        print(f"✅ Finished processing: {title}")

    print("\n🎉 All done!")


if __name__ == "__main__":
    scrape_and_download_images(BASE_URL)