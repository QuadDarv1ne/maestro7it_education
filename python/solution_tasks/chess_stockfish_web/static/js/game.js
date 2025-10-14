let board = null;
let socket = io();
let playerColor = 'white';
let gameActive = false;

document.getElementById('start').addEventListener('click', () => {
    playerColor = document.getElementById('color').value;
    const level = document.getElementById('level').value;
    
    socket.emit('init_game', { color: playerColor, level: level });
});

socket.on('game_initialized', (data) => {
    document.getElementById('setup').style.display = 'none';
    document.getElementById('board').style.display = 'block';
    gameActive = true;

    board = Chessboard('board', {
        position: data.fen,
        draggable: true,
        onDragStart: onDragStart,
        onDrop: onDrop,
        onMouseoutSquare: onMouseoutSquare,
        onMouseoverSquare: onMouseoverSquare,
        orientation: playerColor
    });
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
    if (board) board.position(data.fen);
});

socket.on('game_over', (data) => {
    gameActive = false;
    if (board) board.position(data.fen);
    let msg = '';
    if (data.result === 'checkmate') msg = '🏆 Шах и мат!';
    else if (data.result === 'stalemate') msg = '🤝 Пат!';
    document.getElementById('status').innerText = msg;
});

socket.on('error', (data) => {
    alert('Ошибка: ' + data.message);
});