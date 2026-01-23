# Chess Stockfish Web API Documentation

## Overview

The Chess Stockfish Web API provides endpoints and WebSocket events for interacting with the chess application. This document describes all available HTTP endpoints and WebSocket events.

## HTTP Endpoints

### Authentication Endpoints

#### POST /register
Register a new user account.

**Request Body:**
```json
{
  "username": "string (3-30 chars, alphanumeric and underscore)",
  "email": "string (valid email format)",
  "password": "string (6-128 chars)"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user_id": "integer"
}
```

**Status Codes:**
- 200: Registration successful
- 400: Invalid input data
- 500: Server error

#### POST /login
Authenticate a user and start a session.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "user_id": "integer",
  "username": "string"
}
```

**Status Codes:**
- 200: Login successful
- 401: Invalid credentials
- 500: Server error

#### GET /logout
End the current user session.

**Response:**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

#### GET /profile
Get current user profile information.

**Response:**
```json
{
  "success": true,
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "rating": "integer",
    "games_played": "integer",
    "wins": "integer",
    "losses": "integer",
    "win_rate": "float"
  },
  "recent_games": [
    {
      "id": "integer",
      "result": "string",
      "player_color": "string",
      "skill_level": "integer",
      "start_time": "ISO string",
      "duration": "integer"
    }
  ]
}
```

### Game Endpoints

#### GET /api/puzzles/random
Get a random chess puzzle.

**Query Parameters:**
- `difficulty` (optional): Integer difficulty level
- `category` (optional): String category

**Response:**
```json
{
  "success": true,
  "puzzle": {
    "id": "integer",
    "fen": "string",
    "difficulty": "integer",
    "category": "string",
    "times_solved": "integer",
    "times_failed": "integer"
  }
}
```

#### POST /api/puzzles/solve
Submit a puzzle solution.

**Request Body:**
```json
{
  "puzzle_id": "integer",
  "solution": "array of strings (move notation)",
  "is_correct": "boolean"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Solution recorded successfully"
}
```

#### POST /api/puzzles
Create a new puzzle (admin/restricted).

**Request Body:**
```json
{
  "fen": "string",
  "solution": "string",
  "difficulty": "integer (default 1)",
  "category": "string (default 'tactics')"
}
```

**Response:**
```json
{
  "success": true,
  "puzzle": {
    "id": "integer",
    "fen": "string",
    "difficulty": "integer",
    "category": "string"
  }
}
```

### Health and Status Endpoints

#### GET /health
Check application health status.

**Response:**
```json
{
  "status": "string (healthy|unhealthy)",
  "active_games": "integer",
  "tracked_sessions": "integer",
  "cache_stats": "object",
  "performance_metrics": "object",
  "error_stats": "object",
  "pool_stats": "object"
}
```

#### GET /pool-stats
Get connection pool statistics.

**Response:**
```json
{
  "status": "string",
  "connection_pooling_enabled": "boolean",
  "pool_stats": "object",
  "timestamp": "float"
}
```

#### GET /metrics
Get application metrics in Prometheus format.

**Response:**
```
# Plain text format for Prometheus
cache_hits{cache="..."} ...
active_games_total ...
...
```

#### GET /resource-stats
Get detailed resource usage statistics.

**Response:**
```json
{
  "status": "string",
  "timestamp": "float",
  "resource_stats": "object",
  "current_stats": {
    "active_games": "integer",
    "tracked_sessions": "integer",
    "game_stats": "object",
    "memory_usage": "object",
    "cache_stats": "object",
    "pool_stats": "object",
    "performance_metrics": "object",
    "recent_errors": "array"
  }
}
```

## WebSocket Events

### Client Events (Client → Server)

#### init_game
Initialize a new game session.

**Payload:**
```json
{
  "color": "string ('white' or 'black')",
  "level": "integer (0-20)"
}
```

#### make_move
Make a move in the current game.

**Payload:**
```json
{
  "move": "string (UCI format, e.g. 'e2e4')"
}
```

#### takeback_move
Request to take back the last move.

**Payload:** None

#### analyze_position
Analyze the current position.

**Payload:**
```json
{
  "fen": "string (optional, defaults to current position)"
}
```

#### save_preferences
Save user preferences.

**Payload:**
```json
{
  "preferences": {
    "soundEnabled": "boolean",
    "autoFlipBoard": "boolean",
    "showPossibleMoves": "boolean",
    "animationSpeed": "integer",
    "defaultDifficulty": "integer",
    "defaultColor": "string"
  }
}
```

#### load_preferences
Load user preferences.

**Payload:** None

#### save_game
Save the current game state.

**Payload:** None

#### load_game
Load a saved game state.

**Payload:**
```json
{
  "game_state": "string (serialized game state)"
}
```

#### game_over
Signal that the game is over.

**Payload:**
```json
{
  "result": "string",
  "winner": "string"
}
```

### Server Events (Server → Client)

#### connected
Confirm WebSocket connection.

**Payload:**
```json
{
  "status": "string",
  "message": "string"
}
```

#### game_initialized
Indicate that the game has been successfully initialized.

**Payload:**
```json
{
  "fen": "string",
  "player_color": "string",
  "game_id": "integer (optional)"
}
```

#### position_update
Update the board position after a move.

**Payload:**
```json
{
  "fen": "string",
  "ai_move": "string (optional)",
  "last_move": "string",
  "takeback": "boolean (optional)"
}
```

#### game_over
Indicate that the game has ended.

**Payload:**
```json
{
  "result": "string ('checkmate', 'stalemate', etc.)",
  "fen": "string",
  "winner": "string",
  "last_move": "string"
}
```

#### invalid_move
Indicate that a move was invalid.

**Payload:**
```json
{
  "move": "string",
  "message": "string"
}
```

#### ai_thinking
Provide updates on AI move calculation.

**Payload:**
```json
{
  "status": "string ('calculating', 'complete', 'error')",
  "time": "float (optional, calculation time)"
}
```

#### analysis_result
Return position analysis results.

**Payload:**
```json
{
  "fen": "string",
  "evaluation": "object",
  "best_move": "string",
  "top_moves": "array"
}
```

#### preferences_saved
Confirm that preferences were saved.

**Payload:**
```json
{
  "success": "boolean",
  "message": "string"
}
```

#### preferences_loaded
Return loaded preferences.

**Payload:**
```json
{
  "preferences": "object"
}
```

#### game_saved
Confirm that game was saved.

**Payload:**
```json
{
  "success": "boolean",
  "game_state": "string",
  "message": "string"
}
```

#### game_loaded
Confirm that game was loaded.

**Payload:**
```json
{
  "fen": "string",
  "player_color": "string",
  "skill_level": "integer",
  "game_history": "array",
  "message": "string"
}
```

#### error
Report an error condition.

**Payload:**
```json
{
  "message": "string"
}
```

#### enable_start_button
Enable the start game button (after error recovery).

**Payload:** None

## Error Handling

### HTTP Errors
- 400: Bad Request - Invalid input data
- 401: Unauthorized - Authentication required
- 404: Not Found - Requested resource not found
- 429: Too Many Requests - Rate limit exceeded
- 500: Internal Server Error - Unexpected server error

### WebSocket Errors
Errors are communicated via the `error` event with descriptive messages.

## Rate Limiting

The API implements rate limiting:
- Registration: 5 per minute per IP
- Login: 10 per minute per IP
- General requests: 200 per day, 50 per hour per IP

## Security

- All API endpoints require CSRF protection where applicable
- Input is sanitized to prevent XSS attacks
- SQL injection is prevented through ORM usage
- Passwords are hashed using Werkzeug's secure hashing
- Session cookies are secure and HTTP-only in production

## Versioning

This API follows semantic versioning. Breaking changes will increment the major version number.