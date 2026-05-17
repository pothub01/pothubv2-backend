#!/bin/bash
echo "🌿 PotHub Backend Startup"
echo "=========================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "📦 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Initialize database if it doesn't exist
if [ ! -f "data/pothub.db" ]; then
    echo "🗄️  Initializing database..."
    python3 -c "
import sys
sys.path.insert(0, '.')
from app import init_db, seed_products, seed_blog_posts, seed_reviews
init_db()
seed_products()
seed_blog_posts()
seed_reviews()
print('✅ Database initialized and seeded')
"
fi

echo "🚀 Starting PotHub Backend on http://localhost:5000"
echo "📚 API Documentation: http://localhost:5000/api/health"
echo ""
python3 app.py
