# Chess Stockfish Web Application

A web-based chess application that allows users to play against the Stockfish chess engine with a modern, responsive interface.

## Features

### Current Features
- Play chess against the Stockfish engine (levels 0-20)
- Choose your side (white or black)
- Drag-and-drop piece movement
- Responsive design for desktop and mobile
- Move highlighting and game state detection (check, checkmate, stalemate)
- Move history navigation (⏮ ⬅ ➡ ⏭)
- Position analysis and evaluation
- Save/load games
- User settings and personalization
- Enhanced sound and visual effects
- Real-time WebSocket communication

### Recent Improvements
- **Move Highlighting**: Visual highlighting of the last move made
- **Move List Panel**: Display of all moves in algebraic notation
- **Takeback Functionality**: Ability to undo the last move
- **Database Integration**: Models for user accounts and game persistence
- **Docker Support**: Containerization for easy deployment
- **API Documentation**: Comprehensive WebSocket API documentation
- **Testing Framework**: Unit tests for application components
- **CI/CD Pipeline**: GitHub Actions for automated testing

## Technology Stack

- **Backend**: Python, Flask, Flask-SocketIO
- **Frontend**: HTML, CSS, JavaScript, Chessboard.js, Chess.js
- **Chess Engine**: Stockfish
- **Database**: PostgreSQL (planned), SQLite (development)
- **Caching**: Redis (planned)
- **Containerization**: Docker, Docker Compose

## Installation

### Prerequisites
- Python 3.8+
- Stockfish chess engine
- Node.js and npm (for development)

### Quick Start
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd chess_stockfish_web
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Stockfish:
   - **Windows**: Download from https://stockfishchess.org/download/
   - **macOS**: `brew install stockfish`
   - **Linux**: `sudo apt-get install stockfish`

4. Run the application:
   ```bash
   python app_improved.py
   ```

5. Open your browser to http://localhost:5001

### Docker Installation
1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. Access the application at http://localhost:5001

## Usage

1. Select your side (white or black)
2. Choose difficulty level (0-20)
3. Click "Начать игру" to start
4. Drag pieces to make moves
5. Use navigation buttons to review game history
6. Click "Анализ" to analyze the current position
7. Use "Сохранить" and "Загрузить" to save/load games
8. Adjust settings in the "⚙️ Настройки" panel

## API Documentation

See [API Documentation](docs/api.md) for detailed information about WebSocket events and HTTP endpoints.

## Development

### Project Structure
```
chess_stockfish_web/
├── app_improved.py          # Main application
├── models.py                # Database models
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Multi-service configuration
├── README.md                # This file
├── DOCKER_README.md         # Docker setup guide
├── IMPROVEMENT_SUMMARY.md   # Previous improvements
├── IMPROVEMENT_PLAN.md      # Future improvements
├── static/                  # Web assets
│   ├── css/
│   ├── js/
│   └── images/
├── templates/               # HTML templates
├── utils/                   # Utility modules
├── tests/                   # Test suite
├── docs/                    # Documentation
└── .github/workflows/       # CI/CD pipelines
```

### Running Tests
```bash
python -m pytest tests/ -v
```

### Code Quality
```bash
flake8 . --max-complexity=10 --max-line-length=127
```

## Deployment

### Production Deployment
1. Update database credentials in docker-compose.yml
2. Set secure environment variables
3. Configure SSL termination
4. Add monitoring and logging solutions
5. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Stockfish](https://stockfishchess.org/) - Open source chess engine
- [Chessboard.js](https://chessboardjs.com/) - JavaScript chessboard component
- [Chess.js](https://github.com/jhlywa/chess.js) - JavaScript chess library
- [Flask](https://flask.palletsprojects.com/) - Python web framework
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/) - Real-time web framework

## Future Improvements

See [Improvement Plan](IMPROVEMENT_PLAN.md) for a comprehensive roadmap of planned features and enhancements.