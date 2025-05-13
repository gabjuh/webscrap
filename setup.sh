#!/bin/bash

echo "🔧 Creating virtual environment..."
python3 -m venv venv

echo "📦 Activating virtual environment..."
source venv/bin/activate

echo "⬇️ Installing dependencies..."
pip install -r requirements.txt

echo "🌐 Installing Playwright browsers..."
playwright install chromium

echo "✅ Setup complete. You can now run ./run.sh"
