import json
import sqlite3
from datetime import datetime
from langchain_core.tools import tool
from db import get_conn

# ─── PRODUCTS ────────────────────────────────────────────────


@tool
def list_products(dummy: str = "") -> str:
    """List all available products with id, name, price, category, and stock."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, name, description, price, category, stock FROM products"
    ).fetchall()
    conn.close()
    if not rows:
        return "No products in the store."
    return json.dumps([dict(r) for r in rows], indent=2)


@tool
def search_products(query: str) -> str:
    """Search products by name or category keyword."""
    conn = get_conn()
    like = f"%{query}%"
    rows = conn.execute(
        "SELECT id, name, description, price, category, stock FROM products "
        "WHERE name LIKE ? OR category LIKE ? OR description LIKE ?",
        (like, like, like)
    ).fetchall()
    conn.close()
    if not rows:
        return f"No products found for '{query}'."
    return json.dumps([dict(r) for r in rows], indent=2)


@tool
def get_product_by_id(product_id: str) -> str:
    """Get a single product's details by its numeric ID."""
    conn = get_conn()
    row = conn.execute(
        "SELECT id, name, description, price, category, stock FROM products WHERE id=?",
        (int(product_id),)
    ).fetchone()
    conn.close()
    if not row:
        return f"No product found with id {product_id}."
    return json.dumps(dict(row))


# ─── USERS ───────────────────────────────────────────────────

@tool
def list_users(dummy: str = "") -> str:
    """List all registered users with their id, name, email, and phone."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, full_name, email, phone FROM users").fetchall()
    conn.close()
    if not rows:
        return "No users registered."
    return json.dumps([dict(r) for r in rows], indent=2)


@tool
def get_user_by_id(user_id: str) -> str:
    """Get a user's details by their numeric ID."""
    conn = get_conn()
    row = conn.execute(
        "SELECT id, full_name, email, phone FROM users WHERE id=?",
        (int(user_id),)
    ).fetchone()
    conn.close()
    if not row:
        return f"No user found with id {user_id}."
    return json.dumps(dict(row))


@tool
def search_users(query: str) -> str:
    """Search users by name or email."""
    conn = get_conn()
    like = f"%{query}%"
    rows = conn.execute(
        "SELECT id, full_name, email, phone FROM users "
        "WHERE full_name LIKE ? OR email LIKE ?",
        (like, like)
    ).fetchall()
    conn.close()
    if not rows:
        return f"No user found matching '{query}'."
    return json.dumps([dict(r) for r in rows], indent=2)


# ─── ORDERS ──────────────────────────────────────────────────

@tool
def list_orders(dummy: str = "") -> str:
    """List all orders with user and product details."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT o.id, u.full_name, u.email, p.name AS product,
               o.quantity, o.total_price, o.status, o.address, o.created_at
        FROM orders o
        JOIN users u ON u.id = o.user_id
        JOIN products p ON p.id = o.product_id
        ORDER BY o.id DESC
    """).fetchall()
    conn.close()
    if not rows:
        return "No orders placed yet."
    return json.dumps([dict(r) for r in rows], indent=2)


@tool
def get_order_by_id(order_id: str) -> str:
    """Get a single order's details by its numeric ID."""
    conn = get_conn()
    row = conn.execute("""
        SELECT o.id, u.full_name, u.email, p.name AS product,
               o.quantity, o.total_price, o.status, o.address, o.created_at
        FROM orders o
        JOIN users u ON u.id = o.user_id
        JOIN products p ON p.id = o.product_id
        WHERE o.id = ?
    """, (int(order_id),)).fetchone()
    conn.close()
    if not row:
        return f"No order found with id {order_id}."
    return json.dumps(dict(row))


@tool
def get_orders_by_user(user_id: str) -> str:
    """Get all orders placed by a specific user ID."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT o.id, p.name AS product, o.quantity, o.total_price,
               o.status, o.address, o.created_at
        FROM orders o
        JOIN products p ON p.id = o.product_id
        WHERE o.user_id = ?
        ORDER BY o.id DESC
    """, (int(user_id),)).fetchall()
    conn.close()
    if not rows:
        return f"No orders found for user id {user_id}."
    return json.dumps([dict(r) for r in rows], indent=2)


@tool
def create_order(order_json: str) -> str:
    """
    Place a new order. Expects a JSON string with:
    - user_id (int)
    - product_id (int)
    - quantity (int)
    - address (str)

    Before calling this tool you MUST confirm all four values with the user.
    """
    try:
        data = json.loads(order_json)
        user_id = int(data["user_id"])
        product_id = int(data["product_id"])
        quantity = int(data["quantity"])
        address = str(data["address"])
    except (KeyError, ValueError) as e:
        return f"Invalid order data: {e}. Need user_id, product_id, quantity, address."

    conn = get_conn()

    user = conn.execute(
        "SELECT id, full_name FROM users WHERE id=?", (user_id,)).fetchone()
    if not user:
        conn.close()
        return f"User id {user_id} not found."

    product = conn.execute(
        "SELECT id, name, price, stock FROM products WHERE id=?", (product_id,)
    ).fetchone()
    if not product:
        conn.close()
        return f"Product id {product_id} not found."
    if product["stock"] < quantity:
        conn.close()
        return (f"Insufficient stock. Only {product['stock']} units of "
                f"'{product['name']}' available.")

    total_price = round(product["price"] * quantity, 2)
    created_at = datetime.utcnow().isoformat()

    conn.execute(
        "INSERT INTO orders (user_id, product_id, quantity, total_price, status, address, created_at) "
        "VALUES (?,?,?,?,?,?,?)",
        (user_id, product_id, quantity, total_price,
         "confirmed", address, created_at)
    )
    conn.execute(
        "UPDATE products SET stock = stock - ? WHERE id=?", (quantity,
                                                             product_id)
    )
    conn.commit()
    order_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()

    return (
        f"✅ Order #{order_id} placed!\n"
        f"   Customer : {user['full_name']}\n"
        f"   Product  : {product['name']} x{quantity}\n"
        f"   Total    : ${total_price}\n"
        f"   Address  : {address}\n"
        f"   Status   : confirmed"
    )


# ─── FAQ ─────────────────────────────────────────────────────

@tool
def get_faq_answer(question: str) -> str:
    """Answer shipping, returns, payment, and policy questions from FAQs."""
    import os
    faq_path = os.path.join(os.path.dirname(__file__), "data", "faqs.json")
    with open(faq_path) as f:
        faqs = json.load(f)
    q = question.lower()
    for item in faqs:
        if any(kw in q for kw in item["keywords"]):
            return item["answer"]
    return "I don't have a specific answer for that. Please contact support@store.com."


tools = [
    list_products,
    search_products,
    get_product_by_id,
    list_users,
    get_user_by_id,
    search_users,
    list_orders,
    get_order_by_id,
    get_orders_by_user,
    create_order,
    get_faq_answer,
]
