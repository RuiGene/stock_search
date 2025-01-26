import sqlite3

def create_stock_portfolio_database():
    conn = sqlite3.connect("stock_transactions.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stock_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            units REAL NOT NULL,
            price REAL NOT NULL,
            buy_sell TEXT NOT NULL CHECK (buy_sell IN ('buy', 'sell')),
            ticker TEXT NOT NULL,
            total_value REAL NOT NULL,
            transaction_fee REAL NOT NULL,
            net_value REAL NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()

def create_watchlist_database():
    conn = sqlite3.connect('watchlist.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            ticker TEXT NOT NULL,
            description TEXT,
            image TEXT
        )
        """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # create_stock_portfolio_database()
    # create_watchlist_database()
