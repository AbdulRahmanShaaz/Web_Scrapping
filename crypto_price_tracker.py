import argparse
import logging
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import requests
import schedule

API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": False,
}
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
TIMEOUT = 10
DB_FILE = Path("crypto.db")


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def initialize_database(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prices (
            coin_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            price REAL NOT NULL
        )
        """
    )
    connection.commit()
    return connection


def fetch_crypto_data(session: requests.Session) -> list[dict]:
    response = session.get(API_URL, params=PARAMS, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def store_data(connection: sqlite3.Connection, data: list[dict]) -> None:
    timestamp = datetime.utcnow().isoformat()
    cursor = connection.cursor()
    cursor.executemany(
        "INSERT INTO prices (coin_id, timestamp, price) VALUES (?, ?, ?)",
        [(coin["id"], timestamp, float(coin["current_price"])) for coin in data],
    )
    connection.commit()
    logging.info("Stored %d price records", len(data))


def plot_graph(connection: sqlite3.Connection, coin_id: str) -> None:
    cursor = connection.cursor()
    cursor.execute(
        "SELECT timestamp, price FROM prices WHERE coin_id = ? ORDER BY timestamp",
        (coin_id,),
    )
    rows = cursor.fetchall()
    if not rows:
        logging.warning("No stored price history for %s", coin_id)
        return

    timestamps, prices = zip(*rows)
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, prices, marker="o")
    plt.title(f"{coin_id.upper()} Price History")
    plt.xlabel("Timestamp")
    plt.ylabel("Price (USD)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def scheduled_job(connection: sqlite3.Connection, session: requests.Session) -> None:
    data = fetch_crypto_data(session)
    store_data(connection, data)


def main() -> int:
    configure_logging()

    parser = argparse.ArgumentParser(description="Track cryptocurrency prices using the CoinGecko API and persist them to a database.")
    parser.add_argument("--interval", type=int, default=60, help="Polling interval in minutes")
    parser.add_argument("--plot", help="Plot price history for a coin ID")
    parser.add_argument("--run-once", action="store_true", help="Fetch data once and exit")
    args = parser.parse_args()

    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        connection = initialize_database(DB_FILE)
    except sqlite3.Error as exc:
        logging.error("Failed to initialize database: %s", exc)
        return 1

    try:
        if args.run_once:
            data = fetch_crypto_data(session)
            store_data(connection, data)
            return 0

        scheduled_job(connection, session)
        schedule.every(args.interval).minutes.do(scheduled_job, connection, session)

        if args.plot:
            plot_graph(connection, args.plot)

        logging.info("Scheduler started. Fetching every %d minutes.", args.interval)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except requests.RequestException as exc:
        logging.error("Network error: %s", exc)
        return 1
    except KeyboardInterrupt:
        logging.info("Stopped by user")
        return 0
    except Exception as exc:
        logging.error("Unexpected error: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())