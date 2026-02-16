#!/bin/bash
# Test runner script

set -e

echo "🧪 Running tests..."

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
fi

# Run pytest with coverage
pytest tests/ \
    --cov=app \
    --cov-report=html \
    --cov-report=term-missing \
    --verbose \
    "$@"

echo ""
echo "✅ Tests completed!"
echo "📊 Coverage report: htmlcov/index.html"
