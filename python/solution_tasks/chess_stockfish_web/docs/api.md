# Chess Stockfish Web API Documentation

This document describes the WebSocket API endpoints used by the Chess Stockfish Web application.

## WebSocket Events

### Client to Server

#### `init_game`
Initialize a new game.

**Payload:**
```json
{
  "color": "white|black",
  "level": 0-20
}
```

**Response:**
- `game_initialized` on success
- `error` on failure

#### `make_move`
Make a move in the current game.

**Payload:**
```json
{
  "move": "e2e4"  // UCI format
}
```

**Response:**
- `position_update` on success
- `invalid_move` for invalid moves
- `game_over` if the game ends
- `error` on failure

#### `takeback_move`
Take back the last move.

**Payload:** None

**Response:**
- `position_update` on success
- `error` on failure

#### `analyze_position`
Analyze the current position.

**Payload:**
```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  // Optional, uses current position if not provided
}
```

**Response:**
- `analysis_result` on success
- `error` on failure

#### `save_game`
Save the current game state.

**Payload:** None

**Response:**
- `game_saved` on success
- `error` on failure

#### `load_game`
Load a saved game state.

**Payload:**
```json
{
  "game_state": "base64_encoded_game_state"
}
```

**Response:**
- `game_loaded` on success
- `error` on failure

#### `save_preferences`
Save user preferences.

**Payload:**
```json
{
  "preferences": {
    "soundEnabled": true,
    "autoFlipBoard": false,
    "showPossibleMoves": true,
    "animationSpeed": 300,
    "defaultDifficulty": 5,
    "defaultColor": "white"
  }
}
```

**Response:**
- `preferences_saved` on success
- `error` on failure

#### `load_preferences`
Load user preferences.

**Payload:** None

**Response:**
- `preferences_loaded` on success
- `error` on failure

### Server to Client

#### `connected`
Sent when the WebSocket connection is established.

**Payload:**
```json
{
  "status": "success",
  "message": "Connected successfully"
}
```

#### `game_initialized`
Sent when a new game is successfully initialized.

**Payload:**
```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "player_color": "white|black"
}
```

#### `position_update`
Sent when the board position is updated.

**Payload:**
```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
  "ai_move": "e7e5",  // Present if it's an AI move
  "last_move": "e2e4",  // Present if it's a player move
  "takeback": true  // Present if it's a takeback move
}
```

#### `game_over`
Sent when the game ends.

**Payload:**
```json
{
  "result": "checkmate|stalemate",
  "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
  "winner": "white|black",  // Present for checkmate
  "last_move": "e2e4"  // Last move that ended the game
}
```

#### `invalid_move`
Sent when an invalid move is attempted.

**Payload:**
```json
{
  "move": "e2e5",
  "message": "Invalid move"
}
```

#### `analysis_result`
Sent in response to an analysis request.

**Payload:**
```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
  "evaluation": {
    "type": "cp|mate",
    "value": 0.25  // Centipawns or moves to mate
  },
  "best_move": "e7e5",
  "top_moves": [
    {
      "Move": "e7e5",
      "Centipawn": 25
    }
  ]
}
```

#### `game_saved`
Sent when a game is successfully saved.

**Payload:**
```json
{
  "success": true,
  "game_state": "base64_encoded_game_state",
  "message": "Game saved successfully"
}
```

#### `game_loaded`
Sent when a game is successfully loaded.

**Payload:**
```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
  "player_color": "white",
  "skill_level": 5,
  "game_history": [],
  "message": "Game loaded successfully"
}
```

#### `preferences_saved`
Sent when preferences are successfully saved.

**Payload:**
```json
{
  "success": true,
  "message": "Preferences saved successfully"
}
```

#### `preferences_loaded`
Sent when preferences are successfully loaded.

**Payload:**
```json
{
  "preferences": {
    "soundEnabled": true,
    "autoFlipBoard": false,
    "showPossibleMoves": true,
    "animationSpeed": 300,
    "defaultDifficulty": 5,
    "defaultColor": "white"
  }
}
```

#### `error`
Sent when an error occurs.

**Payload:**
```json
{
  "message": "Error description"
}
```

#### `enable_start_button`
Sent to re-enable the start button after an error.

**Payload:** None

## HTTP Endpoints

### `GET /`
Serve the main application page.

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy|unhealthy",
  "active_games": 0,
  "tracked_sessions": 0,
  "cache_stats": {},
  "performance_metrics": {},
  "error_stats": {},
  "pool_stats": {}
}
```

### `GET /pool-stats`
Connection pool statistics.

**Response:**
```json
{
  "status": "success",
  "connection_pooling_enabled": true,
  "pool_stats": {},
  "timestamp": 1234567890
}
```

## Data Formats

### FEN (Forsyth-Edwards Notation)
Standard chess position notation used throughout the application.

### UCI Move Format
Moves are represented in UCI format (e.g., "e2e4", "g1f3").

### Game State Serialization
Game states are serialized using pickle and encoded in base64 for storage and transmission.