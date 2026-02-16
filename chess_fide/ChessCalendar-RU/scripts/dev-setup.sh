#!/bin/bash
# Development environment setup script

set -e

echo "🛠️  Setting up development environment..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[SETUP]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check Python version
log "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    log "Python version: $PYTHON_VERSION"
else
    warning "Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Create virtual environment
log "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    log "Virtual environment created"
else
    log "Virtual environment already exists"
fi

# Activate virtual environment
log "Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# Upgrade pip
log "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
log "Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
log "Installing development dependencies..."
pip install pytest pytest-cov black flake8 mypy

# Create .env if not exists
if [ ! -f ".env" ]; then
    log "Creating .env file..."
    cp .env.example .env
    log "⚠️  Please edit .env file and set SECRET_KEY!"
else
    log ".env file already exists"
fi

# Create necessary directories
log "Creating directories..."
mkdir -p logs backups instance data/tournaments data/users

# Initialize database
log "Initializing database..."
python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database initialized')
" || warning "Database initialization failed"

# Setup pre-commit hooks (optional)
log "Setting up git hooks..."
if [ -d ".git" ]; then
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Run linting before commit
echo "Running linters..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
black --check app/ || exit 1
flake8 app/ --max-line-length=120 || exit 1
echo "✅ Linting passed"
EOF
    chmod +x .git/hooks/pre-commit
    log "Git hooks installed"
fi

echo ""
log "========================================="
log "✅ Development environment setup complete!"
log "========================================="
echo ""
log "Next steps:"
log "1. Activate virtual environment: source venv/bin/activate"
log "2. Edit .env file and set SECRET_KEY"
log "3. Start Redis: redis-server"
log "4. Start Celery: celery -A app.celery_app worker --loglevel=info"
log "5. Start Flask: python run.py"
echo ""
log "Or use Docker:"
log "  ./scripts/start-all.sh"
