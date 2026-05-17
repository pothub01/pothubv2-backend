#!/usr/bin/env python3
"""PotHub Backend — Flask + SQLite REST API"""

import os
import json
import sqlite3
import hashlib
import secrets
import datetime
from flask import Flask, request, jsonify, g, send_from_directory, render_template
from flask_cors import CORS

# ── Configuration ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'pothub.db')
PRODUCTS_JSON = os.path.join(BASE_DIR, 'data', 'products.json')

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['DATABASE'] = DB_PATH

# Enable CORS for all API routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ── Database Helpers ──
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    
    # Products Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            original INTEGER,
            category TEXT NOT NULL,
            tags TEXT NOT NULL,
            rating REAL NOT NULL,
            reviews INTEGER NOT NULL DEFAULT 0,
            stock INTEGER NOT NULL DEFAULT 0,
            sku TEXT UNIQUE NOT NULL,
            icon TEXT,
            badge TEXT,
            description TEXT,
            colors TEXT,
            sizes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            address TEXT,
            city TEXT,
            province TEXT,
            zip_code TEXT,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    """)
    
    # Orders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            email TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            address_line1 TEXT,
            address_line2 TEXT,
            city TEXT,
            province TEXT,
            zip_code TEXT,
            country TEXT DEFAULT 'Philippines',
            delivery_method TEXT,
            payment_method TEXT,
            subtotal INTEGER NOT NULL,
            shipping INTEGER NOT NULL,
            discount INTEGER DEFAULT 0,
            total INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Order Items Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            color TEXT,
            size TEXT,
            icon TEXT,
            sku TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    
    # Reviews Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            user_name TEXT,
            rating INTEGER NOT NULL,
            title TEXT,
            body TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
    """)
    
    # Blog Posts Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blog_posts (
            id INTEGER PRIMARY KEY,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            excerpt TEXT,
            content TEXT,
            icon TEXT,
            author TEXT,
            date TEXT,
            read_time TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Newsletter Subscribers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Contact Messages Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT NOT NULL,
            topic TEXT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    db.commit()
    db.close()
    print("Database initialized successfully")

def seed_products():
    if not os.path.exists(PRODUCTS_JSON):
        print("products.json not found, skipping seed")
        return
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] > 0:
        print("Products already seeded")
        db.close()
        return
    with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
        products = json.load(f)
    for p in products:
        cursor.execute("""
            INSERT INTO products 
            (id, name, price, original, category, tags, rating, reviews, stock, sku, icon, badge, description, colors, sizes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p["price"], p.get("original"), p["category"],
            json.dumps(p.get("tags", [])), p["rating"], p.get("reviews", 0),
            p.get("stock", 0), p["sku"], p.get("icon", ""), p.get("badge"),
            p.get("desc", ""), json.dumps(p.get("colors", [])), json.dumps(p.get("sizes", []))
        ))
    db.commit()
    db.close()
    print(f"Seeded {len(products)} products")

def seed_blog_posts():
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM blog_posts")
    if cursor.fetchone()[0] > 0:
        db.close()
        return
    posts = [
        (1, "Interior Styling", "10 Ways to Style Pots in a Small Living Room",
         "Small spaces deserve big plant energy. Here is how to use pots strategically...",
         "<p>Small living rooms present a unique challenge...</p>", "🏠", "Anna R.", "May 10, 2026", "5 min", json.dumps(["styling","indoor"])),
        (2, "Plant Decor", "The Art of Grouping Plants: The Rule of Three",
         "Grouping plants in odd numbers creates visual balance...",
         "<p>When arranging plants, odd numbers create...</p>", "🌿", "Marco S.", "May 5, 2026", "4 min", json.dumps(["decor","styling"])),
        (3, "Gardening Tips", "Why Terracotta is the Best Pot Material for Most Plants",
         "Terracotta has been used for centuries and for good reason...",
         "<p>Terracottas breathability makes it ideal...</p>", "🏺", "Liza T.", "Apr 28, 2026", "6 min", json.dumps(["terracotta","care"])),
        (4, "Pot Maintenance", "How to Clean Your Ceramic Pots Without Damaging the Glaze",
         "A clean pot is a happy pot. We walk you through the safest methods...",
         "<p>Regular maintenance keeps your pots looking...</p>", "✨", "Carlo L.", "Apr 20, 2026", "3 min", json.dumps(["care","ceramic"])),
        (5, "Home Inspiration", "The Minimalist Home: How Plants Bring Warmth to Clean Spaces",
         "Nordic-inspired interiors thrive on the contrast...",
         "<p>Minimalism does not mean cold. Plants add...</p>", "⬜", "Anna R.", "Apr 14, 2026", "7 min", json.dumps(["minimalist","styling"])),
        (6, "Gardening Tips", "Choosing the Right Pot Size for Your Plant: A Complete Guide",
         "Pot size matters more than most people think...",
         "<p>Too big and your plant drowns; too small...</p>", "📏", "Liza T.", "Apr 7, 2026", "5 min", json.dumps(["tips","care"])),
        (7, "Sustainability", "Our Journey to Zero-Plastic Packaging",
         "In 2024 we committed to eliminating all plastic...",
         "<p>Our sustainability journey began with...</p>", "🌍", "Carlo L.", "Mar 30, 2026", "8 min", json.dumps(["eco","sustainability"])),
        (8, "Plant Decor", "Hanging Planters: The Vertical Garden Revolution",
         "When floor space runs out, go up! Hanging planters...",
         "<p>Vertical gardening is transforming...</p>", "🪴", "Marco S.", "Mar 22, 2026", "4 min", json.dumps(["hanging","decor"]))
    ]
    cursor.executemany("""
        INSERT INTO blog_posts (id, category, title, excerpt, content, icon, author, date, read_time, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, posts)
    db.commit()
    db.close()
    print(f"Seeded {len(posts)} blog posts")

def seed_reviews():
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM reviews")
    if cursor.fetchone()[0] > 0:
        db.close()
        return
    reviews = [
        (1, "Maria Santos", 5, "Absolutely stunning", "The craftsmanship is exceptional and it arrived perfectly packaged."),
        (1, "Juan Reyes", 5, "Great quality", "Ordered 3 pots and all were delivered in 2 days. Outstanding!"),
        (1, "Andrea Lim", 4, "Beautiful design", "Slightly smaller than expected but still very happy."),
        (2, "Paolo Mendoza", 5, "Perfect terracotta", "Exactly what I needed for my succulents."),
        (3, "Sarah Chen", 5, "Love the macramé", "Beautiful hanging basket, sturdy and well-made."),
        (4, "David Park", 4, "Solid concrete", "Heavy and durable. Looks great on my balcony."),
        (5, "Emma Wilson", 5, "Sleek and modern", "The matte black finish is gorgeous."),
        (6, "James Lee", 5, "Luxury piece", "The oak planter is a true statement piece."),
        (7, "Lisa Wang", 5, "Gold rim beauty", "Photos do not do it justice. Stunning in person."),
        (8, "Tom Garcia", 4, "Elegant marble", "Heavy and beautiful. Great quality.")
    ]
    cursor.executemany("""
        INSERT INTO reviews (product_id, user_name, rating, title, body)
        VALUES (?, ?, ?, ?, ?)
    """, reviews)
    db.commit()
    db.close()
    print(f"Seeded {len(reviews)} reviews")

def hash_password(password):
    salt = secrets.token_hex(16)
    hash_value = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${hash_value}"

def verify_password(stored, provided):
    salt, hash_value = stored.split("$")
    return hashlib.sha256((provided + salt).encode()).hexdigest() == hash_value

def generate_token():
    return secrets.token_urlsafe(32)

# ── Health Check ──
@app.route("/api/health", methods=["GET"])
def health_check():
    try:
        db = get_db()
        db.execute("SELECT 1")
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        return jsonify({"status": "healthy", "database": "connected", "products": product_count, "timestamp": datetime.datetime.now().isoformat()})
    except Exception as e:
        import traceback
        return jsonify({"status": "unhealthy", "error": str(e), "traceback": traceback.format_exc()}), 503

@app.route("/api/debug", methods=["GET"])
def debug_info():
    """Diagnostic endpoint to check DB state."""
    try:
        db = get_db()
        cursor = db.cursor()

        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]

        # Check products
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]

        # Check first product raw data
        cursor.execute("SELECT id, name, tags, colors, sizes FROM products LIMIT 1")
        first = cursor.fetchone()
        first_product = dict(first) if first else None

        return jsonify({
            "tables": tables,
            "product_count": product_count,
            "first_product": first_product,
            "db_path": DB_PATH,
            "db_exists": os.path.exists(DB_PATH)
        })
    except Exception as e:
        import traceback
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

# ── Products API ──
@app.route("/api/products", methods=["GET"])
def get_products():
    db = get_db()
    cursor = db.cursor()
    category = request.args.get("category", "all")
    tag = request.args.get("tag")
    search = request.args.get("q")
    min_price = request.args.get("min_price", type=int)
    max_price = request.args.get("max_price", type=int)
    min_rating = request.args.get("min_rating", type=float)
    in_stock = request.args.get("in_stock", type=bool)
    sort = request.args.get("sort", "featured")
    limit = request.args.get("limit", type=int)
    offset = request.args.get("offset", 0, type=int)
    
    query = "SELECT * FROM products WHERE 1=1"
    params = []
    
    if category and category != "all":
        query += " AND category = ?"
        params.append(category)
    if tag:
        query += " AND tags LIKE ?"
        params.append(f'%"{tag}"%')
    if search:
        query += " AND (name LIKE ? OR category LIKE ? OR description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    if min_price is not None:
        query += " AND price >= ?"
        params.append(min_price)
    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)
    if min_rating is not None:
        query += " AND rating >= ?"
        params.append(min_rating)
    if in_stock:
        query += " AND stock > 0"
    
    sort_map = {"price-asc": "price ASC", "price-desc": "price DESC", "rating": "rating DESC", "reviews": "reviews DESC", "new": "created_at DESC", "featured": "id ASC"}
    query += f" ORDER BY {sort_map.get(sort, 'id ASC')}"
    
    if limit:
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    products = []
    for row in rows:
        products.append({
            "id": row["id"], "name": row["name"], "price": row["price"],
            "original": row["original"], "category": row["category"],
            "tags": json.loads(row["tags"]) if row["tags"] else [],
            "rating": row["rating"], "reviews": row["reviews"],
            "stock": row["stock"], "sku": row["sku"], "icon": row["icon"],
            "badge": row["badge"], "desc": row["description"],
            "colors": json.loads(row["colors"]) if row["colors"] else [],
            "sizes": json.loads(row["sizes"]) if row["sizes"] else [],
            "created_at": row["created_at"]
        })
    
    return jsonify({"products": products, "count": len(products), "filters": {"category": category, "tag": tag, "search": search, "sort": sort}})

@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "Product not found"}), 404
    
    cursor.execute("SELECT * FROM reviews WHERE product_id = ? ORDER BY created_at DESC", (product_id,))
    review_rows = cursor.fetchall()
    reviews = [{"id": r["id"], "user_name": r["user_name"], "rating": r["rating"], "title": r["title"], "body": r["body"], "date": r["created_at"]} for r in review_rows]
    
    product = {
        "id": row["id"], "name": row["name"], "price": row["price"],
        "original": row["original"], "category": row["category"],
        "tags": json.loads(row["tags"]) if row["tags"] else [],
        "rating": row["rating"], "reviews": row["reviews"],
        "stock": row["stock"], "sku": row["sku"], "icon": row["icon"],
        "badge": row["badge"], "desc": row["description"],
        "colors": json.loads(row["colors"]) if row["colors"] else [],
        "sizes": json.loads(row["sizes"]) if row["sizes"] else [],
        "reviews_list": reviews, "created_at": row["created_at"]
    }
    return jsonify(product)

@app.route("/api/products/categories", methods=["GET"])
def get_categories():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT category, COUNT(*) as count FROM products GROUP BY category")
    rows = cursor.fetchall()
    categories = [{"name": row["category"], "count": row["count"]} for row in rows]
    return jsonify({"categories": categories})

@app.route("/api/products/featured", methods=["GET"])
def get_featured():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE badge IS NOT NULL ORDER BY id LIMIT 8")
    rows = cursor.fetchall()
    products = []
    for row in rows:
        products.append({
            "id": row["id"], "name": row["name"], "price": row["price"],
            "original": row["original"], "category": row["category"],
            "tags": json.loads(row["tags"]) if row["tags"] else [],
            "rating": row["rating"], "reviews": row["reviews"],
            "stock": row["stock"], "sku": row["sku"], "icon": row["icon"],
            "badge": row["badge"], "desc": row["description"],
            "colors": json.loads(row["colors"]) if row["colors"] else [],
            "sizes": json.loads(row["sizes"]) if row["sizes"] else []
        })
    return jsonify({"products": products})

@app.route("/api/products/bestsellers", methods=["GET"])
def get_bestsellers():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products ORDER BY reviews DESC LIMIT 8")
    rows = cursor.fetchall()
    products = []
    for row in rows:
        products.append({
            "id": row["id"], "name": row["name"], "price": row["price"],
            "original": row["original"], "category": row["category"],
            "tags": json.loads(row["tags"]) if row["tags"] else [],
            "rating": row["rating"], "reviews": row["reviews"],
            "stock": row["stock"], "sku": row["sku"], "icon": row["icon"],
            "badge": row["badge"], "desc": row["description"],
            "colors": json.loads(row["colors"]) if row["colors"] else [],
            "sizes": json.loads(row["sizes"]) if row["sizes"] else []
        })
    return jsonify({"products": products})

@app.route("/api/products/new", methods=["GET"])
def get_new_arrivals():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE tags LIKE '%new%' ORDER BY id DESC LIMIT 8")
    rows = cursor.fetchall()
    products = []
    for row in rows:
        products.append({
            "id": row["id"], "name": row["name"], "price": row["price"],
            "original": row["original"], "category": row["category"],
            "tags": json.loads(row["tags"]) if row["tags"] else [],
            "rating": row["rating"], "reviews": row["reviews"],
            "stock": row["stock"], "sku": row["sku"], "icon": row["icon"],
            "badge": row["badge"], "desc": row["description"],
            "colors": json.loads(row["colors"]) if row["colors"] else [],
            "sizes": json.loads(row["sizes"]) if row["sizes"] else []
        })
    return jsonify({"products": products})

@app.route("/api/products/related/<int:product_id>", methods=["GET"])
def get_related(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT category, tags FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    if not row:
        return jsonify({"products": []})
    category = row["category"]
    tags = json.loads(row["tags"]) if row["tags"] else []
    tag_pattern = f'"{tags[0]}"' if tags else "%"
    cursor.execute("SELECT * FROM products WHERE id != ? AND (category = ? OR tags LIKE ?) ORDER BY rating DESC LIMIT 4", (product_id, category, tag_pattern))
    rows = cursor.fetchall()
    products = []
    for row in rows:
        products.append({
            "id": row["id"], "name": row["name"], "price": row["price"],
            "original": row["original"], "category": row["category"],
            "tags": json.loads(row["tags"]) if row["tags"] else [],
            "rating": row["rating"], "reviews": row["reviews"],
            "stock": row["stock"], "sku": row["sku"], "icon": row["icon"],
            "badge": row["badge"], "desc": row["description"],
            "colors": json.loads(row["colors"]) if row["colors"] else [],
            "sizes": json.loads(row["sizes"]) if row["sizes"] else []
        })
    return jsonify({"products": products})

# ── Auth API ──
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")
    phone = data.get("phone", "")
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        return jsonify({"error": "Email already registered"}), 409
    password_hash = hash_password(password)
    cursor.execute("INSERT INTO users (email, password_hash, first_name, last_name, phone) VALUES (?, ?, ?, ?, ?)", (email, password_hash, first_name, last_name, phone))
    db.commit()
    user_id = cursor.lastrowid
    token = generate_token()
    return jsonify({"success": True, "message": "Account created successfully", "user": {"id": user_id, "email": email, "name": f"{first_name} {last_name}".strip()}, "token": token}), 201

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    if not row or not verify_password(row["password_hash"], password):
        return jsonify({"error": "Invalid email or password"}), 401
    cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (row["id"],))
    db.commit()
    token = generate_token()
    return jsonify({"success": True, "user": {"id": row["id"], "email": row["email"], "name": f"{row['first_name'] or ''} {row['last_name'] or ''}".strip(), "first_name": row["first_name"], "last_name": row["last_name"], "phone": row["phone"]}, "token": token})

@app.route("/api/auth/me", methods=["GET"])
def get_current_user():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email required"}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, email, first_name, last_name, phone, address, city, province, zip_code FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": row["id"], "email": row["email"], "name": f"{row['first_name'] or ''} {row['last_name'] or ''}".strip(), "first_name": row["first_name"], "last_name": row["last_name"], "phone": row["phone"], "address": row["address"], "city": row["city"], "province": row["province"], "zip_code": row["zip_code"]})

@app.route("/api/auth/profile", methods=["PUT"])
def update_profile():
    data = request.get_json()
    if not data or not data.get("email"):
        return jsonify({"error": "Email required"}), 400
    db = get_db()
    cursor = db.cursor()
    fields = []
    values = []
    for field in ["first_name", "last_name", "phone", "address", "city", "province", "zip_code"]:
        if field in data:
            fields.append(f"{field} = ?")
            values.append(data[field])
    if not fields:
        return jsonify({"error": "No fields to update"}), 400
    values.append(data["email"])
    cursor.execute(f"UPDATE users SET {', '.join(fields)} WHERE email = ?", values)
    db.commit()
    return jsonify({"success": True, "message": "Profile updated"})

# ── Orders API ──
@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    required_fields = ["email", "first_name", "last_name", "address_line1", "city", "province", "items"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400
    db = get_db()
    cursor = db.cursor()
    order_num = f"PH-{datetime.datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(3).upper()}"
    subtotal = data.get("subtotal", 0)
    shipping = data.get("shipping", 150)
    discount = data.get("discount", 0)
    total = data.get("total", subtotal + shipping - discount)
    cursor.execute("""
        INSERT INTO orders 
        (order_number, email, first_name, last_name, phone, address_line1, address_line2,
         city, province, zip_code, country, delivery_method, payment_method,
         subtotal, shipping, discount, total, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        order_num, data["email"], data["first_name"], data["last_name"], data.get("phone", ""),
        data["address_line1"], data.get("address_line2", ""), data["city"], data["province"],
        data.get("zip_code", ""), data.get("country", "Philippines"),
        data.get("delivery_method", "standard"), data.get("payment_method", "card"),
        subtotal, shipping, discount, total, "confirmed"
    ))
    order_id = cursor.lastrowid
    for item in data["items"]:
        cursor.execute("""
            INSERT INTO order_items 
            (order_id, product_id, name, price, quantity, color, size, icon, sku)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_id, item.get("id"), item["name"], item["price"], item["qty"],
            item.get("color", ""), item.get("size", ""), item.get("icon", ""), item.get("sku", "")
        ))
        if item.get("id"):
            cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?", (item["qty"], item["id"], item["qty"]))
    db.commit()
    return jsonify({"success": True, "order": {"id": order_id, "order_number": order_num, "total": total, "status": "confirmed", "created_at": datetime.datetime.now().isoformat()}}), 201

@app.route("/api/orders/<order_number>", methods=["GET"])
def get_order(order_number):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_number = ?", (order_number,))
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "Order not found"}), 404
    cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (row["id"],))
    items = cursor.fetchall()
    order = {
        "id": row["id"], "order_number": row["order_number"], "email": row["email"],
        "first_name": row["first_name"], "last_name": row["last_name"], "phone": row["phone"],
        "address": {"line1": row["address_line1"], "line2": row["address_line2"], "city": row["city"], "province": row["province"], "zip_code": row["zip_code"], "country": row["country"]},
        "delivery_method": row["delivery_method"], "payment_method": row["payment_method"],
        "subtotal": row["subtotal"], "shipping": row["shipping"], "discount": row["discount"],
        "total": row["total"], "status": row["status"], "created_at": row["created_at"],
        "items": [{"id": i["id"], "product_id": i["product_id"], "name": i["name"], "price": i["price"], "quantity": i["quantity"], "color": i["color"], "size": i["size"], "icon": i["icon"], "sku": i["sku"]} for i in items]
    }
    return jsonify(order)

@app.route("/api/orders/user/<email>", methods=["GET"])
def get_user_orders(email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM orders WHERE email = ? ORDER BY created_at DESC", (email,))
    rows = cursor.fetchall()
    orders = []
    for row in rows:
        cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (row["id"],))
        items = cursor.fetchall()
        orders.append({"id": row["id"], "order_number": row["order_number"], "total": row["total"], "status": row["status"], "created_at": row["created_at"], "item_count": len(items)})
    return jsonify({"orders": orders})

# ── Blog API ──
@app.route("/api/blog", methods=["GET"])
def get_blog_posts():
    db = get_db()
    cursor = db.cursor()
    category = request.args.get("category")
    tag = request.args.get("tag")
    query = "SELECT * FROM blog_posts WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if tag:
        query += " AND tags LIKE ?"
        params.append(f'%"{tag}"%')
    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    posts = []
    for row in rows:
        posts.append({"id": row["id"], "category": row["category"], "title": row["title"], "excerpt": row["excerpt"], "content": row["content"], "icon": row["icon"], "author": row["author"], "date": row["date"], "read_time": row["read_time"], "tags": json.loads(row["tags"]) if row["tags"] else []})
    return jsonify({"posts": posts, "count": len(posts)})

@app.route("/api/blog/<int:post_id>", methods=["GET"])
def get_blog_post(post_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM blog_posts WHERE id = ?", (post_id,))
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "Post not found"}), 404
    return jsonify({"id": row["id"], "category": row["category"], "title": row["title"], "excerpt": row["excerpt"], "content": row["content"], "icon": row["icon"], "author": row["author"], "date": row["date"], "read_time": row["read_time"], "tags": json.loads(row["tags"]) if row["tags"] else []})

# ── Newsletter API ──
@app.route("/api/subscribe", methods=["POST"])
def subscribe_newsletter():
    data = request.get_json()
    if not data or not data.get("email"):
        return jsonify({"error": "Email is required"}), 400
    email = data["email"].strip().lower()
    if "@" not in email:
        return jsonify({"error": "Invalid email address"}), 400
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
        db.commit()
        return jsonify({"success": True, "message": "Subscribed successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"success": True, "message": "Already subscribed!"})

# ── Contact API ──
@app.route("/api/contact", methods=["POST"])
def submit_contact():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()
    if not email or not message:
        return jsonify({"error": "Email and message are required"}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO contact_messages (first_name, last_name, email, topic, message) VALUES (?, ?, ?, ?, ?)", (data.get("first_name", ""), data.get("last_name", ""), email, data.get("topic", "General Inquiry"), message))
    db.commit()
    return jsonify({"success": True, "message": "Message sent! We will reply within 24 hours."}), 201

# ── Reviews API ──
@app.route("/api/reviews", methods=["POST"])
def create_review():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    product_id = data.get("product_id")
    rating = data.get("rating")
    if not product_id or not rating:
        return jsonify({"error": "Product ID and rating are required"}), 400
    if not (1 <= rating <= 5):
        return jsonify({"error": "Rating must be between 1 and 5"}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO reviews (product_id, user_name, rating, title, body) VALUES (?, ?, ?, ?, ?)", (product_id, data.get("user_name", "Anonymous"), rating, data.get("title", ""), data.get("body", "")))
    cursor.execute("SELECT COUNT(*) as count, AVG(rating) as avg FROM reviews WHERE product_id = ?", (product_id,))
    row = cursor.fetchone()
    cursor.execute("UPDATE products SET reviews = ?, rating = ? WHERE id = ?", (row["count"], round(row["avg"], 1), product_id))
    db.commit()
    return jsonify({"success": True, "message": "Review submitted!"}), 201

@app.route("/api/reviews/<int:product_id>", methods=["GET"])
def get_product_reviews(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reviews WHERE product_id = ? ORDER BY created_at DESC", (product_id,))
    rows = cursor.fetchall()
    reviews = [{"id": r["id"], "user_name": r["user_name"], "rating": r["rating"], "title": r["title"], "body": r["body"], "date": r["created_at"]} for r in rows]
    return jsonify({"reviews": reviews, "count": len(reviews)})

# ── Cart API ──
@app.route("/api/cart", methods=["POST"])
def save_cart():
    data = request.get_json()
    if not data or "items" not in data:
        return jsonify({"error": "No cart data provided"}), 400
    db = get_db()
    cursor = db.cursor()
    validated_items = []
    for item in data["items"]:
        cursor.execute("SELECT id, name, price, stock, icon, sku FROM products WHERE id = ?", (item.get("id"),))
        row = cursor.fetchone()
        if row and row["stock"] >= item.get("qty", 1):
            validated_items.append({"id": row["id"], "name": row["name"], "price": row["price"], "qty": item.get("qty", 1), "color": item.get("color", ""), "size": item.get("size", ""), "icon": row["icon"], "sku": row["sku"], "stock": row["stock"]})
    return jsonify({"success": True, "items": validated_items, "total": sum(i["price"] * i["qty"] for i in validated_items), "count": sum(i["qty"] for i in validated_items)})

# ── Stats API ──
@app.route("/api/stats", methods=["GET"])
def get_stats():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(total) FROM orders")
    revenue = cursor.fetchone()[0] or 0
    return jsonify({"products": product_count, "users": user_count, "orders": order_count, "revenue": revenue, "categories": 6})

# ── Frontend Serving ──
@app.route("/")
def serve_index():
    return render_template("index.html")

@app.route("/<path:path>")
def serve_page(path):
    if path.startswith("api/"):
        return jsonify({"error": "Not found"}), 404
    template_path = os.path.join(BASE_DIR, "templates", path)
    if os.path.exists(template_path) and os.path.isfile(template_path):
        return render_template(path)
    if not path.endswith(".html"):
        template_path = os.path.join(BASE_DIR, "templates", path + ".html")
        if os.path.exists(template_path):
            return render_template(path + ".html")
    static_path = os.path.join(BASE_DIR, "static", path)
    if os.path.exists(static_path):
        return send_from_directory(os.path.join(BASE_DIR, "static"), path)
    return render_template("index.html")


# ── Global Error Handler (logs to stderr for Render) ──
import traceback
import sys

@app.errorhandler(Exception)
def handle_exception(e):
    """Log full traceback and return JSON error."""
    traceback.print_exc()
    return jsonify({
        "error": "Internal server error",
        "message": str(e),
        "type": type(e).__name__
    }), 500
# ── Error Handlers ──
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "message": "The requested resource does not exist"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "message": "Something went wrong"}), 500

# ── Main ──
# ── Initialize on Import (for gunicorn) ──
# This runs when the module is imported by gunicorn
if not os.path.exists(DB_PATH):
    print("🗄️  Database not found. Initializing...")
    init_db()
    seed_products()
    seed_blog_posts()
    seed_reviews()
    print("✅ Database ready")
else:
    print("🗄️  Database exists. Skipping initialization.")

# ── Production Entry Point ──
# Render and other platforms set the PORT environment variable
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") != "production"

    print(f"🌿 PotHub Backend starting on port {port}")
    print(f"📚 API endpoints available at /api/*")
    app.run(debug=debug, host="0.0.0.0", port=port)
