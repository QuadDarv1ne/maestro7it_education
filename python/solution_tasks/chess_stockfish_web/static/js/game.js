let board = null;
let socket = io();
let playerColor = 'white';
let gameActive = false;
let gameHistory = [];

document.getElementById('start').addEventListener('click', () => {
    playerColor = document.getElementById('color').value;
    const level = document.getElementById('level').value;
    
    // Validate level input
    if (level < 0 || level > 20) {
        alert('Уровень должен быть от 0 до 20');
        return;
    }
    
    socket.emit('init_game', { color: playerColor, level: level });
});

// Add reset button functionality
function addResetButton() {
    const resetBtn = document.createElement('button');
    resetBtn.id = 'reset';
    resetBtn.textContent = 'Новая игра';
    resetBtn.addEventListener('click', () => {
        location.reload();
    });
    document.querySelector('.container').insertBefore(resetBtn, document.getElementById('status'));
}

socket.on('game_initialized', (data) => {
    document.getElementById('setup').style.display = 'none';
    document.getElementById('board').style.display = 'block';
    gameActive = true;
    
    // Clear previous history
    gameHistory = [];

    board = Chessboard('board', {
        position: data.fen,
        draggable: true,
        onDragStart: onDragStart,
        onDrop: onDrop,
        onMouseoutSquare: onMouseoutSquare,
        onMouseoverSquare: onMouseoverSquare,
        orientation: playerColor
    });
    
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
    if (board) {
        board.position(data.fen);
        gameHistory.push(data.fen);
        
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
    document.getElementById('status').innerText = '❌ ' + (data.message || 'Недопустимый ход');
});

socket.on('error', (data) => {
    document.getElementById('status').innerText = '⚠️ Ошибка: ' + data.message;
});