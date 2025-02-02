import sqlite3

def create_stock_portfolio_database():
    conn = sqlite3.connect("stock_transactions.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stock_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            ticker TEXT NOT NULL,
            units REAL NOT NULL,
            price REAL NOT NULL,
            action TEXT NOT NULL CHECK (action IN ('Buy', 'Sell')),
            total_value REAL
        )
        """
    )

    # cursor.execute(""" DROP TABLE STOCK_TRANSACTIONS""")

    conn.commit()
    conn.close()

    print("Sucess")

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

def create_current_holdings():
    conn = sqlite3.connect('current_holdings.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS CURRENT_HOLDINGS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        units REAL NOT NULL
        )
        """
    )

    # cursor.execute(""" DROP TABLE CURRENT_HOLDINGS""")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    # create_stock_portfolio_database()
    # create_watchlist_database()
    create_current_holdings()