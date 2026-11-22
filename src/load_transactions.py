
import csv
import sqlite3
from pathlib import Path

# Find the project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Define where our files live
CSV_PATH = BASE_DIR / "data" / "sample" / "transactions.csv"
DB_PATH = BASE_DIR / "data" / "budget.db"

# Connect to SQLite (creates database if missing)
with sqlite3.connect(DB_PATH) as conn:

    # Create transactions table if it doesn't exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            date TEXT,
            description TEXT,
            amount REAL,
            category TEXT
        )
    """)

    # Read transactions from CSV
    with open(CSV_PATH, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            conn.execute("""
                INSERT OR IGNORE INTO transactions
                (transaction_id, date, description, amount, category)
                VALUES (?, ?, ?, ?, ?)
            """, (
                row["transaction_id"],
                row["date"],
                row["description"],
                float(row["amount"]),
                row["category"]
            ))

    # Count transactions currently in database
    count = conn.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone()[0]

    print(f"Total transactions in database: {count}")
