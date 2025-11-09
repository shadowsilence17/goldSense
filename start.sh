#!/bin/bash
# Startup script for DigitalOcean App Platform

echo "🚀 Starting Gold Price Prediction App..."
echo "📍 Current directory: $(pwd)"
echo "📂 Directory contents:"
ls -la

echo ""
echo "🐍 Python version:"
python --version

echo ""
echo "📦 Checking imports..."
python -c "import app; print('✅ app module found')" || exit 1
python -c "from webapp.app import app; print('✅ Flask app found')" || exit 1

echo ""
echo "🔧 Starting Gunicorn..."
echo "📡 Port: ${PORT:-8080}"
echo "🎯 Workers: 2"

exec gunicorn --bind "0.0.0.0:${PORT:-8080}" app:app \
  --workers 2 \
  --timeout 120 \
  --log-level info \
  --access-logfile - \
  --error-logfile - \
  --preload
