# 🌿 PotHub Backend

A complete Flask + SQLite backend for the PotHub plant pot e-commerce application.

## Features

- **REST API** with 20+ endpoints
- **SQLite Database** with full schema
- **User Authentication** (register/login/profile)
- **Product Management** with filtering, sorting, search
- **Order Processing** with stock management
- **Blog System** with categories and tags
- **Newsletter Subscriptions**
- **Contact Form** storage
- **Product Reviews** with rating aggregation
- **CORS enabled** for frontend integration

## Quick Start

```bash
# Make startup script executable and run
chmod +x start.sh
./start.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 app.py
```

The server will start on `http://localhost:5000`.

## API Endpoints

### Health
- `GET /api/health` — Health check

### Products
- `GET /api/products` — List all products (supports filtering, sorting, pagination)
- `GET /api/products/<id>` — Get single product with reviews
- `GET /api/products/categories` — Get category counts
- `GET /api/products/featured` — Featured products
- `GET /api/products/bestsellers` — Bestselling products
- `GET /api/products/new` — New arrivals
- `GET /api/products/related/<id>` — Related products

### Auth
- `POST /api/auth/register` — Register new user
- `POST /api/auth/login` — Login user
- `GET /api/auth/me` — Get current user
- `PUT /api/auth/profile` — Update profile

### Orders
- `POST /api/orders` — Create order
- `GET /api/orders/<order_number>` — Get order details
- `GET /api/orders/user/<email>` — Get user orders

### Blog
- `GET /api/blog` — List blog posts
- `GET /api/blog/<id>` — Get single post

### Reviews
- `POST /api/reviews` — Submit review
- `GET /api/reviews/<product_id>` — Get product reviews

### Other
- `POST /api/subscribe` — Newsletter signup
- `POST /api/contact` — Contact form
- `POST /api/cart` — Validate cart items
- `GET /api/stats` — Store statistics

## Query Parameters

### Products
- `category` — Filter by category (ceramic, terracotta, hanging, concrete, luxury, eco)
- `tag` — Filter by tag
- `q` — Search query
- `min_price` / `max_price` — Price range
- `min_rating` — Minimum rating
- `in_stock` — Only in-stock items
- `sort` — Sort order: `featured`, `price-asc`, `price-desc`, `rating`, `reviews`, `new`
- `limit` / `offset` — Pagination

## Database Schema

### Tables
- **products** — Product catalog with stock, ratings, categories
- **users** — Registered users with profile data
- **orders** — Order records with shipping details
- **order_items** — Individual items per order
- **reviews** — Product reviews with ratings
- **blog_posts** — Blog articles
- **subscribers** — Newsletter subscribers
- **contact_messages** — Contact form submissions

## File Structure

```
backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── start.sh              # Startup script
├── data/
│   ├── products.json      # Product seed data
│   └── pothub.db          # SQLite database (auto-created)
├── templates/             # HTML templates
│   ├── index.html
│   ├── shop.html
│   ├── product.html
│   ├── cart.html
│   ├── checkout.html
│   └── ...
└── static/
    ├── css/
    │   ├── style.css
    │   └── responsive.css
    └── js/
        ├── app.js
        └── components.js
```

## Environment Variables

- `FLASK_ENV` — Set to `development` for debug mode
- `FLASK_PORT` — Server port (default: 5000)
- `SECRET_KEY` — Auto-generated on startup

## Notes

- Database is auto-initialized on first run
- Products are seeded from `data/products.json`
- Blog posts and reviews are seeded automatically
- Passwords are hashed with SHA-256 + salt
- CORS is enabled for all `/api/*` routes
