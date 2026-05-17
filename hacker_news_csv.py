import requests
from bs4 import BeautifulSoup
import csv
import os
import wget
HN_URL='https://news.ycombinator.com/'
CSV_FILE="hn_top20.csv"
def fetch_top_post(url):
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()
    except requests.RequestException as e :
        print(f"Network Error \n {e}")
        return []
    soup = BeautifulSoup(response.text,'html.parser')
    post_links= soup.select('span.titleline > a')[:20]
    posts = []
    for post in post_links:
        title=post.get_text(strip=True)
        link=post['href']
        # print(f"Title: {title}\nLink: {link}\n")
        posts.append({'title':title,'link':link})

    return posts
def save_to_csv(posts,filename):
    if not posts:
        print("No posts found.")
        return
    with open(filename,'w',newline='',encoding='utf-8') as csvfile:
        fieldnames = ['title', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(posts)
        print(f"Data saved to {filename} 🙋‍♂️🙋‍♂️🙋‍♂️")

def main():
    print("scrapping the HN portal")
    posts = fetch_top_post(HN_URL)
    save_to_csv(posts,CSV_FILE)

if __name__ == "__main__":
    main()



