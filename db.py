import sqlite3
import json
from datetime import datetime


def add_product(name, description, price, category, stock):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, description, price, category, stock) VALUES (?,?,?,?,?)",
        (name, description, price, category, stock)
    )
    conn.commit()
    conn.close()
    return cur.lastrowid


def add_user(full_name, email, phone):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (full_name, email, phone) VALUES (?,?,?)",
        (full_name, email, phone)
    )
    conn.commit()
    conn.close()
    return cur.lastrowid


def add_order(user_id, product_id, quantity, total_price, status="confirmed", address=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (user_id, product_id, quantity, total_price, status, address, created_at) VALUES (?,?,?,?,?,?,?)",
        (user_id, product_id, quantity, total_price,
         status, address, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return cur.lastrowid


DB_PATH = "ecommerce.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT,
            stock INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            status TEXT DEFAULT 'confirmed',
            address TEXT,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        );
    """)

    # Seed products if empty
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        products = [
            ("Wireless Headphones", "Noise-cancelling Bluetooth headphones",
             59.99, "Electronics", 25),
            ("Running Shoes", "Lightweight breathable running shoes",
             89.99, "Footwear", 40),
            ("Stainless Water Bottle", "1L insulated stainless steel bottle",
             19.99, "Accessories", 100),
            ("Yoga Mat", "Non-slip 6mm thick yoga mat", 29.99, "Sports", 60),
            ("Laptop Backpack", "Waterproof 30L backpack with USB port", 49.99, "Bags", 35),
        ]
        cur.executemany(
            "INSERT INTO products (name, description, price, category, stock) VALUES (?,?,?,?,?)",
            products
        )

    # Seed users if empty
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        users = [
            ("Alice Smith", "alice@example.com", "+1-555-0101"),
            ("Bob Jones",   "bob@example.com",   "+1-555-0202"),
            ("Carol White", "carol@example.com",  "+1-555-0303"),
        ]
        cur.executemany(
            "INSERT INTO users (full_name, email, phone) VALUES (?,?,?)",
            users
        )

    conn.commit()
    conn.close()
    print(" Database initialised (ecommerce.db)")


print(" Data added")
