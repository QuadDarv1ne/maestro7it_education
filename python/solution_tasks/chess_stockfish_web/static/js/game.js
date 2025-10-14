let board = null;
let socket = io({
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    reconnectionAttempts: 5
});
let playerColor = 'white';
let gameActive = false;
let gameHistory = [];
let moveSound = null;
let reconnecting = false;

// Add connection error handling
socket.on('connect', () => {
    console.log('WebSocket connected');
    document.getElementById('status').innerText = 'Готовы начать игру!';
});

socket.on('connected', (data) => {
    console.log('Server confirmed connection:', data);
    document.getElementById('status').innerText = 'Готовы начать игру!';
});

socket.on('connect_error', (error) => {
    console.error('WebSocket connection error:', error);
    document.getElementById('status').innerText = '⚠️ Ошибка подключения: ' + error.message;
    
    // Re-enable start button
    const startBtn = document.getElementById('start');
    startBtn.disabled = false;
    startBtn.textContent = 'Начать игру';
});

socket.on('disconnect', (reason) => {
    console.log('WebSocket disconnected:', reason);
    document.getElementById('status').innerText = '⚠️ Отключено: ' + reason;
    
    // Re-enable start button
    const startBtn = document.getElementById('start');
    if (startBtn) {
        startBtn.disabled = false;
        startBtn.textContent = 'Начать игру';
    }
    
    // Show reconnecting message
    setTimeout(() => {
        document.getElementById('status').innerText = '🔁 Переподключение...';
        reconnecting = true;
    }, 2000);
});

socket.on('reconnect', (attemptNumber) => {
    console.log('WebSocket reconnected after', attemptNumber, 'attempts');
    document.getElementById('status').innerText = '🔄 Переподключено!';
    reconnecting = false;
    
    // Briefly show success message
    setTimeout(() => {
        if (gameActive) {
            document.getElementById('status').innerText = playerColor === 'white' ? 
                'Ваш ход: белые' : 'Ход компьютера: черные';
        } else {
            document.getElementById('status').innerText = 'Готовы начать игру!';
        }
    }, 2000);
});

socket.on('reconnect_attempt', (attemptNumber) => {
    console.log('WebSocket reconnect attempt:', attemptNumber);
    document.getElementById('status').innerText = `🔁 Попытка переподключения (${attemptNumber})`;
});

socket.on('reconnect_failed', () => {
    console.log('WebSocket reconnect failed');
    document.getElementById('status').innerText = '❌ Не удалось переподключиться';
    reconnecting = false;
});

document.getElementById('start').addEventListener('click', () => {
    playerColor = document.getElementById('color').value;
    const level = document.getElementById('level').value;
    
    console.log('Starting game with color:', playerColor, 'level:', level);
    
    // Validate level input
    if (level < 0 || level > 20) {
        alert('Уровень должен быть от 0 до 20');
        return;
    }
    
    // Disable start button and show loading state
    const startBtn = document.getElementById('start');
    startBtn.disabled = true;
    startBtn.textContent = 'Загрузка...';
    
    // Update status to show we're initializing
    document.getElementById('status').innerText = '⏳ Инициализация игры...';
    
    // Emit init_game event
    socket.emit('init_game', { color: playerColor, level: parseInt(level) });
    console.log('Sent init_game event');
});

// Add reset button functionality
function addResetButton() {
    // Remove existing reset button if it exists
    const existingResetBtn = document.getElementById('reset');
    if (existingResetBtn) {
        existingResetBtn.remove();
    }
    
    const resetBtn = document.createElement('button');
    resetBtn.id = 'reset';
    resetBtn.textContent = 'Новая игра';
    resetBtn.addEventListener('click', () => {
        if (board) {
            board.destroy();
            board = null;
        }
        document.getElementById('setup').style.display = 'block';
        document.getElementById('board').style.display = 'none';
        gameActive = false;
        gameHistory = [];
        
        // Remove reset button
        const resetBtn = document.getElementById('reset');
        if (resetBtn) {
            resetBtn.remove();
        }
        
        document.getElementById('status').innerText = 'Готовы начать игру!';
    });
    document.querySelector('.container').insertBefore(resetBtn, document.getElementById('status'));
}

socket.on('game_initialized', (data) => {
    console.log('Game initialized:', data);
    document.getElementById('setup').style.display = 'none';
    document.getElementById('board').style.display = 'block';
    gameActive = true;
    
    // Clear previous history
    gameHistory = [];

    // Destroy existing board if it exists
    if (board) {
        board.destroy();
    }

    board = Chessboard('board', {
        position: data.fen,
        draggable: true,
        onDragStart: onDragStart,
        onDrop: onDrop,
        onMouseoutSquare: onMouseoutSquare,
        onMouseoverSquare: onMouseoverSquare,
        orientation: data.player_color || playerColor,
        pieceTheme: 'https://unpkg.com/chessboardjs@1.0.0/dist/img/chesspieces/wikipedia/{piece}.png'
    });
    
    // Re-enable start button
    const startBtn = document.getElementById('start');
    startBtn.disabled = false;
    startBtn.textContent = 'Начать игру';
    
    // Add reset button
    addResetButton();
    
    // Update status
    document.getElementById('status').innerText = playerColor === 'white' ? 
        'Ваш ход: белые' : 'Ход компьютера: черные';
});

function onDragStart(source, piece) {
    if (!gameActive) return false;
    // Разрешаем ход только своей фигурой
    const isWhite = piece.startsWith('w');
    const isPlayerWhite = (playerColor === 'white');
    return isPlayerWhite === isWhite;
}

function onDrop(source, target) {
    const move = source + target; // UCI: e2e4
    console.log('Making move:', move);
    
    // Show move processing status
    document.getElementById('status').innerText = '⏳ Обработка хода...';
    
    // Disable board interaction during move processing
    gameActive = false;
    
    socket.emit('make_move', { move: move });
    removeGreySquares();
}

function onMouseoverSquare(square, piece) {
    if (piece) greySquare(square);
}

function onMouseoutSquare(square, piece) {
    removeGreySquares();
}

let greySquares = [];
function greySquare(square) {
    const squareEl = document.querySelector(`#board .square-${square}`);
    if (squareEl) {
        squareEl.style.background = 'rgba(124, 252, 0, 0.5)';
        greySquares.push(square);
    }
}

function removeGreySquares() {
    greySquares.forEach(square => {
        const squareEl = document.querySelector(`#board .square-${square}`);
        if (squareEl) squareEl.style.background = '';
    });
    greySquares = [];
}

// Обработка обновления позиции
socket.on('position_update', (data) => {
    console.log('Position update:', data);
    if (board) {
        board.position(data.fen);
        gameHistory.push(data.fen);
        
        // Re-enable board interaction
        gameActive = true;
        
        // Show AI move if provided
        if (data.ai_move) {
            document.getElementById('status').innerText = `Компьютер сходил: ${data.ai_move}`;
        } else {
            document.getElementById('status').innerText = playerColor === 'white' ? 
                'Ваш ход: белые' : 'Ваш ход: черные';
        }
    }
});

socket.on('game_over', (data) => {
    console.log('Game over:', data);
    gameActive = false;
    if (board) board.position(data.fen);
    
    let msg = '';
    if (data.result === 'checkmate') {
        if (data.winner === playerColor) {
            msg = '🏆 Поздравляем! Вы выиграли!';
        } else {
            msg = '❌ Шах и мат! Вы проиграли.';
        }
    } else if (data.result === 'stalemate') {
        msg = '🤝 Ничья (пат)!';
    }
    
    document.getElementById('status').innerText = msg;
});

socket.on('invalid_move', (data) => {
    console.log('Invalid move:', data);
    
    // Re-enable board interaction
    gameActive = true;
    
    document.getElementById('status').innerText = '❌ ' + (data.message || 'Недопустимый ход');
});

socket.on('error', (data) => {
    console.log('Error:', data);
    
    // Re-enable board interaction and start button
    gameActive = false;
    const startBtn = document.getElementById('start');
    startBtn.disabled = false;
    startBtn.textContent = 'Начать игру';
    
    // Handle specific error types
    let errorMessage = data.message || 'Неизвестная ошибка';
    if (errorMessage.includes('engine')) {
        errorMessage = 'Ошибка движка Stockfish. Попробуйте перезапустить игру.';
    } else if (errorMessage.includes('session')) {
        errorMessage = 'Ошибка сессии. Попробуйте обновить страницу.';
    } else if (errorMessage.includes('overload') || errorMessage.includes('limit')) {
        errorMessage = 'Сервер перегружен. Попробуйте позже.';
    }
    
    document.getElementById('status').innerText = '⚠️ Ошибка: ' + errorMessage;
});