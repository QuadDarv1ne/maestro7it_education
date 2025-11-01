# Документация API веб-приложения Chess Stockfish

Этот документ описывает эндпоинты WebSocket API, используемые в веб-приложении Chess Stockfish.

## События WebSocket

### От клиента к серверу

#### `init_game`
Инициализация новой игры.

**Полезная нагрузка:**
```json
{
  "color": "white|black",
  "level": 0-20
}
```

**Ответ:**
- `game_initialized` при успешном выполнении
- `error` при ошибке

#### `make_move`
Сделать ход в текущей игре.

**Полезная нагрузка:**
```json
{
  "move": "e2e4"  // Формат UCI
}
```

**Ответ:**
- `position_update` при успешном выполнении
- `invalid_move` для недопустимых ходов
- `game_over` если игра завершена
- `error` при ошибке

#### `takeback_move`
Отменить последний ход.

**Полезная нагрузка:** Нет

**Ответ:**
- `position_update` при успешном выполнении
- `error` при ошибке

#### `analyze_position`
Анализ текущей позиции.

**Полезная нагрузка:**
```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  // Необязательно, использует текущую позицию, если не указано
}
```

**Ответ:**
- `analysis_result` при успешном выполнении
- `error` при ошибке

#### `save_game`
Сохранить текущее состояние игры.

**Полезная нагрузка:** Нет

**Ответ:**
- `game_saved` при успешном выполнении
- `error` при ошибке

#### `load_game`
Загрузить сохраненное состояние игры.

**Полезная нагрузка:**
```json
{
  "game_state": "base64_encoded_game_state"
}
```

**Ответ:**
- `game_loaded` при успешном выполнении
- `error` при ошибке

#### `save_preferences`
Сохранить настройки пользователя.

**Полезная нагрузка:**
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

**Ответ:**
- `preferences_saved` при успешном выполнении
- `error` при ошибке

#### `load_preferences`
Загрузить настройки пользователя.

**Полезная нагрузка:** Нет

**Ответ:**
- `preferences_loaded` при успешном выполнении
- `error` при ошибке

### От сервера к клиенту

#### `connected`
Отправляется при установлении соединения WebSocket.

**Полезная нагрузка:**
```json
{
  "status": "success",
  "message": "Connected successfully"
}
```

#### `game_initialized`
Отправляется при успешной инициализации новой игры.

**Полезная нагрузка:**
```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "player_color": "white|black"
}
```

#### `position_update`
Отправляется при обновлении позиции на доске.

**Полезная нагрузка:**
```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
  "ai_move": "e7e5",  // Присутствует, если это ход ИИ
  "last_move": "e2e4",  // Присутствует, если это ход игрока
  "takeback": true  // Присутствует, если это отмена хода
}
```

#### `game_over`
Отправляется при завершении игры.

**Полезная нагрузка:**
```json
{
  "result": "checkmate|stalemate",
  "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
  "winner": "white|black",  // Присутствует при мате
  "last_move": "e2e4"  // Последний ход, завершивший игру
}
```

#### `invalid_move`
Отправляется при попытке сделать недопустимый ход.

**Полезная нагрузка:**
```json
{
  "move": "e2e5",
  "message": "Invalid move"
}
```

#### `analysis_result`
Отправляется в ответ на запрос анализа.

**Полезная нагрузка:**
```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
  "evaluation": {
    "type": "cp|mate",
    "value": 0.25  // Сантепешки или ходы до мата
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
Отправляется при успешном сохранении игры.

**Полезная нагрузка:**
```json
{
  "success": true,
  "game_state": "base64_encoded_game_state",
  "message": "Game saved successfully"
}
```

#### `game_loaded`
Отправляется при успешной загрузке игры.

**Полезная нагрузка:**
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
Отправляется при успешном сохранении настроек.

**Полезная нагрузка:**
```json
{
  "success": true,
  "message": "Preferences saved successfully"
}
```

#### `preferences_loaded`
Отправляется при успешной загрузке настроек.

**Полезная нагрузка:**
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
Отправляется при возникновении ошибки.

**Полезная нагрузка:**
```json
{
  "message": "Error description"
}
```

#### `enable_start_button`
Отправляется для повторного включения кнопки начала игры после ошибки.

**Полезная нагрузка:** Нет

## HTTP-эндпоинты

### `GET /`
Отправка главной страницы приложения.

### `GET /health`
Эндпоинт проверки состояния.

**Ответ:**
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
Статистика пула соединений.

**Ответ:**
```json
{
  "status": "success",
  "connection_pooling_enabled": true,
  "pool_stats": {},
  "timestamp": 1234567890
}
```

## Форматы данных

### FEN (нотация Форсайта-Эдвардса)
Стандартная шахматная нотация позиции, используемая в приложении.

### Формат хода UCI
Ходы представлены в формате UCI (например, "e2e4", "g1f3").

### Сериализация состояния игры
Состояния игры сериализуются с помощью pickle и кодируются в base64 для хранения и передачи.