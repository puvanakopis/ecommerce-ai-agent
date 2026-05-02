# E-Commerce AI Agent 🛒

An AI-powered e-commerce assistant that interacts with a live SQLite store database. Built with LangGraph's ReAct agent, it handles product browsing, user lookup, order management, and FAQ responses through natural conversation.

<br>

## 📋 Project Overview

The E-Commerce AI Agent serves as a conversational interface for an online store. It connects to a live SQLite database and enables users to explore products, look up accounts, place orders, and get answers to common store questions — all through a friendly chat experience.

### Key Objectives:
- Provide a natural language interface for browsing and purchasing products
- Enable real-time order placement with step-by-step conversational flow
- Answer common customer questions via an FAQ knowledge base
- Maintain conversation history for context-aware responses

### Database Architecture
- **SQLite** (`ecommerce.db`) — Primary database for products, users, and orders

<br>

## 🛠️ Tech Stack

### Backend
- **Python** — Core language
- **LangGraph** — ReAct agent framework
- **LangChain** — Tool definitions and LLM integration
- **ChatGroq (LLaMA 3.3 70B)** — Language model
- **SQLite** — Lightweight relational database
- **Pydantic** — Data validation

<br>

## ✨ Features

### Product Management
- List all available products with price, category, and stock
- Search products by name, category, or description keyword
- Fetch a single product's full details by ID

### User Management
- List all registered users
- Search users by name or email
- Get a specific user's details by ID

### Order Management
- View all orders with joined user and product details
- Retrieve a single order by ID
- Fetch all orders for a specific user
- Place new orders via guided conversational flow

### FAQ Assistant
- Answers questions about shipping, returns, payments, cancellations, and order tracking
- Keyword-based matching from a structured JSON knowledge base
- Falls back to support contact for unrecognised queries

### Conversational Order Placement
The agent collects all required fields step-by-step before placing an order:
1. **Product** — asks the user to pick from the product list if unsure
2. **User ID** — confirms or looks up by name/email
3. **Quantity** — how many units?
4. **Address** — full delivery address

Once all four fields are confirmed, the agent calls `create_order` and returns a formatted confirmation.

<br>

## 🤖 Agent Architecture

The agent uses a **ReAct (Reasoning + Acting)** loop powered by LangGraph:

1. **User Input** — The user sends a message via the CLI.
2. **History Management** — Full conversation history is passed with every invocation.
3. **Tool Selection** — The LLM decides which tool(s) to call based on the query.
4. **Tool Execution** — The selected tool queries the SQLite database or FAQ file.
5. **Response Generation** — The LLM synthesises tool results into a natural reply.
6. **History Update** — The assistant's reply is appended to history for future context.

### Available Tools

| Tool | Description |
|------|-------------|
| `list_products` | List all products |
| `search_products` | Search by name, category, or description |
| `get_product_by_id` | Fetch a product by numeric ID |
| `list_users` | List all registered users |
| `get_user_by_id` | Fetch a user by numeric ID |
| `search_users` | Search users by name or email |
| `list_orders` | List all orders with full details |
| `get_order_by_id` | Fetch a single order by ID |
| `get_orders_by_user` | Get all orders for a specific user |
| `create_order` | Place a new order (requires all four fields) |
| `get_faq_answer` | Answer shipping, returns, and policy questions |

<br>

## 🗄️ Database Schema

### `products`
```
id          INTEGER PRIMARY KEY AUTOINCREMENT
name        TEXT NOT NULL
description TEXT
price       REAL NOT NULL
category    TEXT
stock       INTEGER DEFAULT 0
```

### `users`
```
id          INTEGER PRIMARY KEY AUTOINCREMENT
full_name   TEXT NOT NULL
email       TEXT UNIQUE NOT NULL
phone       TEXT
```

### `orders`
```
id           INTEGER PRIMARY KEY AUTOINCREMENT
user_id      INTEGER NOT NULL  →  users.id
product_id   INTEGER NOT NULL  →  products.id
quantity     INTEGER NOT NULL
total_price  REAL NOT NULL
status       TEXT DEFAULT 'confirmed'
address      TEXT
created_at   TEXT
```

<br>

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- A [Groq](https://console.groq.com) API key

### Installation

```bash
# Clone the repository
git clone https://github.com/puvanakopis/ecommerce-ai-agent
cd ecommerce-ai-agent

# Create a virtual environment and install dependencies using uv
uv sync```

### Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Run

```bash
python main.py
```

The database is initialised automatically on first run with sample products and users.

<br>

## 📁 Folder Structure

```
ecommerce-ai-agent/
├── data/
│   └── faqs.json          # FAQ knowledge base
├── .gitignore             # Git ignore file
├── .python-version        # Specified Python version for uv
├── agent.py               # Agent builder and reply extractor
├── config.py              # Environment settings
├── db.py                  # SQLite connection and schema init
├── main.py                # CLI entry point
├── models.py              # Pydantic models (formerly schemas.py)
├── prompts.py             # System prompt
├── pyproject.toml         # Project dependencies and config
├── tools.py               # LangChain tool definitions
├── uv.lock                # Locked dependency tree
└── README.md
```

<br>

## 💬 Example Interactions

```
You: Show me all products
Agent: Here are the products currently available in the store: ...

You: I want to order the laptop backpack
Agent: Sure! I'll need a few details. What's your user ID or name?

You: I'm Alice
Agent: Found you — Alice Smith (ID: 1). How many units of the Laptop Backpack would you like?

You: 2
Agent: And what's your delivery address?

You: 123 Main Street, Springfield
Agent: ✅ Order #6 placed!
       Customer : Alice Smith
       Product  : Laptop Backpack x2
       Total    : $99.98
       Address  : 123 Main Street, Springfield
       Status   : confirmed

You: What's your return policy?
Agent: We accept returns within 30 days of delivery. Items must be unused and in original packaging.
```

<br>


## 👤 Author

**Name:** Puvanakopis  
**GitHub:** [@puvanakopis](https://github.com/puvanakopis)  
**LinkedIn:** [Puvanakopis](https://www.linkedin.com/in/puvanakopis/)  
**Email:** puvanakopis@gamil.com


**E-Commerce AI Agent — Smart Shopping, Simplified 🛍️**
