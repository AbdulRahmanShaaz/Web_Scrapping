import time
from datetime import datetime
import requests
import matplotlib.pyplot as plt
import schedule
import sqlite3


API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 10,
    'page': 1,
    'sparkline': False
}

# 🔥 In-memory storage (replace with DB later)
price_store = {}   # {coin_id: [(timestamp, price), ...]}

def create_table():
    con = sqllite3.connect("crypto.db")
    cur = con.cursor()


def fetch_crypto_data():

    try:
        print("🌐 Fetching crypto data...")
        response = requests.get(API_URL, params=PARAMS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Fetch failed: {e}")
        return []


def store_data(data):
    timestamp = datetime.now()

    for coin in data:
        coin_id = coin["id"]
        price = coin["current_price"]

        if coin_id not in price_store:
            price_store[coin_id] = []

        price_store[coin_id].append((timestamp, price))

    print(f"💾 Stored data at {timestamp.strftime('%H:%M:%S')}")


# Scheduled job
def job():
    data = fetch_crypto_data()
    if data:
        store_data(data)


def plot_graph(coin_id):
    if coin_id not in price_store or not price_store[coin_id]:
        print(f"⚠️ No data available for '{coin_id}'")
        return

    times = [t for t, _ in price_store[coin_id]]
    prices = [p for _, p in price_store[coin_id]]

    plt.figure(figsize=(10, 5))
    plt.plot(times, prices, marker='o')
    plt.title(f"{coin_id.upper()} Price Over Time")
    plt.xlabel("Time")
    plt.ylabel("Price (USD)")
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.gcf().autofmt_xdate()
    plt.show()


def main():
    print("🚀 Crypto Tracker Started\n")

    # 🔥 Run once immediately
    job()

    # 🔥 Schedule hourly
    schedule.every().hour.do(job)

    # 🔥 Show available coins (initial snapshot)
    data = fetch_crypto_data()
    print("\n📊 Available coin IDs:")
    for coin in data:
        print(f"- {coin['id']}")

    # 🔥 Ask user
    choice = input("\n📈 Do you want to plot a graph? (yes/no): ").strip().lower()

    if choice == "yes":
        coin_id = input("Enter coin ID: ").strip().lower()
        plot_graph(coin_id)

    print("\n⏳ Scheduler running... (Ctrl+C to stop)\n")

    # 🔥 Keep scheduler alive
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()