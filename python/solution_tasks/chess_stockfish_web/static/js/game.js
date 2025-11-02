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
let currentHistoryIndex = -1;
let moveSound = null;
let captureSound = null;
let checkSound = null;
let gameOverSound = null;
let reconnecting = false;
let savedGameState = null;
let isFlipped = false;
let userPreferences = {
    soundEnabled: true,
    autoFlipBoard: false,
    showPossibleMoves: true,
    animationSpeed: 300,
    defaultDifficulty: 5,
    defaultColor: 'white'
};
let moveList = []; // Track moves in algebraic notation
let chess = null; // Chess.js instance for validation
let playerTimer = 0; // Player timer in seconds
let aiTimer = 0; // AI timer in seconds
let timerInterval = null;
let currentTurn = 'white'; // Track whose turn it is

// Initialize audio
function initAudio() {
    try {
        // Create audio context
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        const audioCtx = new AudioContext();
        
        // Create simple sound generators
        moveSound = () => {
            if (!userPreferences.soundEnabled) return;
            try {
                const oscillator = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();
                oscillator.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                oscillator.type = 'sine';
                oscillator.frequency.value = 523.25; // C5
                gainNode.gain.value = 0.1;
                oscillator.start();
                setTimeout(() => {
                    oscillator.stop();
                }, 100);
            } catch (e) {
                console.log('Audio error:', e);
            }
        };
        
        captureSound = () => {
            if (!userPreferences.soundEnabled) return;
            try {
                const oscillator = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();
                oscillator.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                oscillator.type = 'square';
                oscillator.frequency.value = 349.23; // F4
                gainNode.gain.value = 0.1;
                oscillator.start();
                setTimeout(() => {
                    oscillator.stop();
                }, 150);
            } catch (e) {
                console.log('Audio error:', e);
            }
        };
        
        checkSound = () => {
            if (!userPreferences.soundEnabled) return;
            try {
                const oscillator = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();
                oscillator.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                oscillator.type = 'sawtooth';
                oscillator.frequency.value = 261.63; // C4
                gainNode.gain.value = 0.1;
                oscillator.start();
                setTimeout(() => {
                    oscillator.stop();
                }, 200);
            } catch (e) {
                console.log('Audio error:', e);
            }
        };
        
        gameOverSound = () => {
            if (!userPreferences.soundEnabled) return;
            try {
                // Play a simple victory/fanfare sound
                const playNote = (frequency, duration, type = 'sine') => {
                    const oscillator = audioCtx.createOscillator();
                    const gainNode = audioCtx.createGain();
                    oscillator.connect(gainNode);
                    gainNode.connect(audioCtx.destination);
                    oscillator.type = type;
                    oscillator.frequency.value = frequency;
                    gainNode.gain.value = 0.1;
                    oscillator.start();
                    setTimeout(() => {
                        oscillator.stop();
                    }, duration);
                };
                
                // Play a simple melody
                playNote(523.25, 200); // C5
                setTimeout(() => playNote(659.25, 200), 200); // E5
                setTimeout(() => playNote(783.99, 400), 400); // G5
            } catch (e) {
                console.log('Audio error:', e);
            }
        };
    } catch (e) {
        console.log('Audio initialization failed:', e);
        // Fallback to console logging
        moveSound = () => console.log('Move sound');
        captureSound = () => console.log('Capture sound');
        checkSound = () => console.log('Check sound');
        gameOverSound = () => console.log('Game over sound');
    }
}

// Initialize audio on first user interaction
document.addEventListener('click', initAudio, { once: true });

// Load user preferences on connect
socket.on('connect', () => {
    console.log('WebSocket connected');
    document.getElementById('status').innerText = 'Готовы начать игру!';
    
    // Load user preferences
    socket.emit('load_preferences');
});

socket.on('connected', (data) => {
    console.log('Server confirmed connection:', data);
    document.getElementById('status').innerText = 'Готовы начать игру!';
});

socket.on('connect_error', (error) => {
    console.error('WebSocket connection error:', error);
    document.getElementById('status').innerText = '⚠️ Ошибка подключения: ' + error.message;
    
    // Show detailed error notification
    showNotification('Ошибка подключения: ' + error.message, 'error');
    
    // Re-enable start button
    const startBtn = document.getElementById('start');
    startBtn.disabled = false;
    startBtn.textContent = 'Начать игру';
});

socket.on('disconnect', (reason) => {
    console.log('WebSocket disconnected:', reason);
    document.getElementById('status').innerText = '⚠️ Отключено: ' + reason;
    
    // Show notification
    showNotification('Отключено: ' + reason, 'warning');
    
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
    
    // Show success notification
    showNotification('Переподключено успешно!', 'success');
    
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
    
    // Show error notification
    showNotification('Не удалось переподключиться. Попробуйте обновить страницу.', 'error');
});

socket.on('enable_start_button', () => {
    console.log('Enabling start button');
    // Re-enable start button
    const startBtn = document.getElementById('start');
    if (startBtn) {
        startBtn.disabled = false;
        startBtn.textContent = 'Начать игру';
    }
});

// Start game button handler
const startBtn = document.getElementById('start');
if (startBtn) {
    startBtn.addEventListener('click', () => {
        // Get color from active button
        const activeColorBtn = document.querySelector('.color-btn.active');
        playerColor = activeColorBtn ? activeColorBtn.dataset.color : 'white';
        const level = document.getElementById('level').value;
        
        console.log('Starting game with color:', playerColor, 'level:', level);
        
        // Validate level input
        if (level < 0 || level > 20) {
            showNotification('Уровень должен быть от 0 до 20', 'error');
            return;
        }
        
        // Save user preferences
        saveUserPreferences();
        
        // Disable start button and show loading state
        const startBtn = document.getElementById('start');
        startBtn.disabled = true;
        const btnText = startBtn.querySelector('.btn-text');
        if (btnText) {
            btnText.textContent = 'Загрузка...';
        } else {
            startBtn.textContent = 'Загрузка...';
        }
        
        // Update status to show we're initializing
        const statusEl = document.getElementById('status');
        if (statusEl) {
            statusEl.innerText = '⏳ Инициализация игры...';
        }
        
        // Set a timeout to handle initialization errors
        const initTimeout = setTimeout(() => {
            if (statusEl) {
                statusEl.innerText = '⚠️ Превышено время ожидания инициализации. Попробуйте еще раз.';
            }
            startBtn.disabled = false;
            if (btnText) {
                btnText.textContent = 'Начать игру';
            } else {
                startBtn.textContent = 'Начать игру';
            }
            showNotification('Превышено время ожидания инициализации. Попробуйте еще раз.', 'error');
        }, 30000); // 30 seconds timeout
        
        // Store timeout ID to clear it later
        window.initTimeout = initTimeout;
        
        // Emit init_game event
        socket.emit('init_game', { color: playerColor, level: parseInt(level) });
        console.log('Sent init_game event');
    });
}

// Add reset button functionality
function addResetButton() {
    // Reset button is already in HTML, just add event listener
    const resetBtn = document.getElementById('reset');
    if (resetBtn && !resetBtn.hasAttribute('data-listener')) {
        resetBtn.setAttribute('data-listener', 'true');
        resetBtn.addEventListener('click', () => {
        if (board) {
            board.destroy();
            board = null;
        }
        
        // Reset game state
        chess = null;
        gameActive = false;
        gameHistory = [];
        currentHistoryIndex = -1;
        moveList = [];
        savedGameState = null;
        playerTimer = 0;
        aiTimer = 0;
        stopTimer();
        
        // Show setup and hide game section
        document.querySelector('.setup-screen').style.display = 'flex';
        document.getElementById('game-section').style.display = 'none';
        
        const statusEl = document.getElementById('status');
        if (statusEl) {
            statusEl.innerText = 'Готовы начать игру!';
        }
        updateMoveListDisplay();
        showNotification('Игра сброшена', 'info');
    });
    }
    
    // Takeback button
    const takebackBtn = document.getElementById('takeback');
    if (takebackBtn && !takebackBtn.hasAttribute('data-listener')) {
        takebackBtn.setAttribute('data-listener', 'true');
        takebackBtn.addEventListener('click', takebackMove);
    }
    
    // Analyze button
    const analyzeBtn = document.getElementById('analyze');
    if (analyzeBtn && !analyzeBtn.hasAttribute('data-listener')) {
        analyzeBtn.setAttribute('data-listener', 'true');
        analyzeBtn.addEventListener('click', analyzePosition);
    }
    
    // Clear history button
    const clearHistoryBtn = document.getElementById('clear-history');
    if (clearHistoryBtn && !clearHistoryBtn.hasAttribute('data-listener')) {
        clearHistoryBtn.setAttribute('data-listener', 'true');
        clearHistoryBtn.addEventListener('click', () => {
            moveList = [];
            updateMoveListDisplay();
            showNotification('История ходов очищена', 'info');
        });
    }
}

function takebackMove() {
    // Request takeback from server
    document.getElementById('status').innerText = 'Отмена последнего хода...';
    socket.emit('takeback_move');
}

function addPreferencesButton() {
    // Remove existing preferences button if it exists
    const existingBtn = document.getElementById('preferences-btn');
    if (existingBtn) {
        existingBtn.remove();
    }
    
    // Create preferences button
    const preferencesBtn = document.createElement('button');
    preferencesBtn.id = 'preferences-btn';
    preferencesBtn.textContent = '⚙️ Настройки';
    preferencesBtn.style.marginTop = '10px';
    preferencesBtn.addEventListener('click', showPreferencesDialog);
    
    // Insert after save/load container
    const saveLoadContainer = document.getElementById('save-load-container');
    if (saveLoadContainer) {
        saveLoadContainer.parentNode.insertBefore(preferencesBtn, saveLoadContainer.nextSibling);
    } else {
        const buttonContainer = document.getElementById('button-container');
        if (buttonContainer) {
            buttonContainer.parentNode.insertBefore(preferencesBtn, buttonContainer.nextSibling);
        } else {
            document.querySelector('.container').insertBefore(preferencesBtn, document.getElementById('status'));
        }
    }
}

function showPreferencesDialog() {
    // Remove existing dialog if it exists
    const existingDialog = document.getElementById('preferences-dialog');
    if (existingDialog) {
        existingDialog.remove();
    }
    
    // Create preferences dialog
    const dialog = document.createElement('div');
    dialog.id = 'preferences-dialog';
    dialog.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(0, 0, 0, 0.9);
        color: white;
        padding: 20px;
        border-radius: 10px;
        z-index: 1001;
        min-width: 300px;
        max-width: 90%;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
    `;
    
    // Add overlay
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 1000;
    `;
    overlay.addEventListener('click', () => {
        dialog.remove();
        overlay.remove();
    });
    
    // Add title
    const title = document.createElement('h2');
    title.textContent = '⚙️ Настройки';
    title.style.marginTop = '0';
    title.style.color = '#4FC3F7';
    dialog.appendChild(title);
    
    // Add sound option
    const soundContainer = document.createElement('div');
    soundContainer.style.marginBottom = '15px';
    soundContainer.innerHTML = `
        <label>
            <input type="checkbox" id="sound-enabled" ${userPreferences.soundEnabled ? 'checked' : ''}>
            Включить звуки
        </label>
    `;
    dialog.appendChild(soundContainer);
    
    // Add auto flip option
    const flipContainer = document.createElement('div');
    flipContainer.style.marginBottom = '15px';
    flipContainer.innerHTML = `
        <label>
            <input type="checkbox" id="auto-flip" ${userPreferences.autoFlipBoard ? 'checked' : ''}>
            Автоматически поворачивать доску
        </label>
    `;
    dialog.appendChild(flipContainer);
    
    // Add possible moves option
    const movesContainer = document.createElement('div');
    movesContainer.style.marginBottom = '15px';
    movesContainer.innerHTML = `
        <label>
            <input type="checkbox" id="show-moves" ${userPreferences.showPossibleMoves ? 'checked' : ''}>
            Показывать возможные ходы
        </label>
    `;
    dialog.appendChild(movesContainer);
    
    // Add animation speed option
    const speedContainer = document.createElement('div');
    speedContainer.style.marginBottom = '15px';
    speedContainer.innerHTML = `
        <label>
            Скорость анимации:
            <select id="animation-speed">
                <option value="100" ${userPreferences.animationSpeed === 100 ? 'selected' : ''}>Быстрая</option>
                <option value="300" ${userPreferences.animationSpeed === 300 ? 'selected' : ''}>Средняя</option>
                <option value="500" ${userPreferences.animationSpeed === 500 ? 'selected' : ''}>Медленная</option>
            </select>
        </label>
    `;
    dialog.appendChild(speedContainer);
    
    // Add buttons
    const buttonsContainer = document.createElement('div');
    buttonsContainer.style.display = 'flex';
    buttonsContainer.style.justifyContent = 'space-between';
    buttonsContainer.style.marginTop = '20px';
    
    const saveBtn = document.createElement('button');
    saveBtn.textContent = 'Сохранить';
    saveBtn.addEventListener('click', () => {
        // Save preferences
        userPreferences.soundEnabled = document.getElementById('sound-enabled').checked;
        userPreferences.autoFlipBoard = document.getElementById('auto-flip').checked;
        userPreferences.showPossibleMoves = document.getElementById('show-moves').checked;
        userPreferences.animationSpeed = parseInt(document.getElementById('animation-speed').value);
        
        // Apply preferences
        applyUserPreferences();
        
        // Save to server
        socket.emit('save_preferences', {
            preferences: userPreferences
        });
        
        // Close dialog
        dialog.remove();
        overlay.remove();
        
        showNotification('Настройки сохранены!', 'success');
    });
    
    const closeBtn = document.createElement('button');
    closeBtn.textContent = 'Закрыть';
    closeBtn.style.background = 'linear-gradient(to bottom, #616161, #424242)';
    closeBtn.addEventListener('click', () => {
        dialog.remove();
        overlay.remove();
    });
    
    buttonsContainer.appendChild(saveBtn);
    buttonsContainer.appendChild(closeBtn);
    dialog.appendChild(buttonsContainer);
    
    // Add to document
    document.body.appendChild(overlay);
    document.body.appendChild(dialog);
}

function addSaveLoadButtons() {
    // Remove existing save/load container if it exists
    const existingContainer = document.getElementById('save-load-container');
    if (existingContainer) {
        existingContainer.remove();
    }
    
    // Create save/load container
    const saveLoadContainer = document.createElement('div');
    saveLoadContainer.id = 'save-load-container';
    saveLoadContainer.style.margin = '10px 0';
    saveLoadContainer.style.display = 'flex';
    saveLoadContainer.style.justifyContent = 'center';
    saveLoadContainer.style.gap = '10px';
    saveLoadContainer.style.flexWrap = 'wrap';
    
    // Create save button
    const saveBtn = document.createElement('button');
    saveBtn.id = 'save-game';
    saveBtn.textContent = 'Сохранить';
    saveBtn.addEventListener('click', saveGame);
    
    // Create load button
    const loadBtn = document.createElement('button');
    loadBtn.id = 'load-game';
    loadBtn.textContent = 'Загрузить';
    loadBtn.addEventListener('click', loadGame);
    
    // Add buttons to container
    saveLoadContainer.appendChild(saveBtn);
    saveLoadContainer.appendChild(loadBtn);
    
    // Insert after button container
    const buttonContainer = document.getElementById('button-container');
    if (buttonContainer) {
        buttonContainer.parentNode.insertBefore(saveLoadContainer, buttonContainer.nextSibling);
    } else {
        document.querySelector('.container').insertBefore(saveLoadContainer, document.getElementById('status'));
    }
}

function saveGame() {
    document.getElementById('status').innerText = 'Сохранение игры...';
    socket.emit('save_game', {});
}

function loadGame() {
    if (savedGameState) {
        document.getElementById('status').innerText = 'Загрузка игры...';
        socket.emit('load_game', { game_state: savedGameState });
    } else {
        document.getElementById('status').innerText = 'Нет сохраненной игры для загрузки';
    }
}

function analyzePosition() {
    if (gameHistory.length > 0 && currentHistoryIndex >= 0) {
        const fen = gameHistory[currentHistoryIndex];
        document.getElementById('status').innerText = 'Анализ позиции...';
        
        // Emit analysis request
        socket.emit('analyze_position', { fen: fen });
    }
}

function displayAnalysis(data) {
    const analysisPanel = document.getElementById('analysis-panel');
    const analysisContent = document.getElementById('analysis-content');
    
    if (!analysisPanel || !analysisContent) {
        console.error('Analysis panel not found in HTML');
        return;
    }
    
    // Clear existing content
    analysisContent.innerHTML = '';
    
    // Add evaluation
    if (data.evaluation) {
        const evalItem = document.createElement('div');
        evalItem.className = 'analysis-item';
        
        const evalLabel = document.createElement('span');
        evalLabel.className = 'analysis-label';
        evalLabel.textContent = 'Оценка позиции:';
        
        const evalValue = document.createElement('span');
        evalValue.className = 'analysis-value';
        
        let evalText = '';
        if (data.evaluation.type === 'mate') {
            evalText = `Мат в ${Math.abs(data.evaluation.value)} ходов`;
            evalText += data.evaluation.value > 0 ? ' (белые)' : ' (черные)';
        } else if (data.evaluation.type === 'cp') {
            const cp = data.evaluation.value / 100;
            evalText = `${cp > 0 ? '+' : ''}${cp.toFixed(2)}`;
        } else {
            evalText = 'Неопределено';
        }
        evalValue.textContent = evalText;
        
        evalItem.appendChild(evalLabel);
        evalItem.appendChild(evalValue);
        analysisContent.appendChild(evalItem);
    }
    
    // Add best move
    if (data.best_move) {
        const bestMoveItem = document.createElement('div');
        bestMoveItem.className = 'analysis-item';
        
        const bestMoveLabel = document.createElement('span');
        bestMoveLabel.className = 'analysis-label';
        bestMoveLabel.textContent = 'Лучший ход:';
        
        const bestMoveValue = document.createElement('span');
        bestMoveValue.className = 'analysis-value';
        bestMoveValue.textContent = data.best_move;
        
        bestMoveItem.appendChild(bestMoveLabel);
        bestMoveItem.appendChild(bestMoveValue);
        analysisContent.appendChild(bestMoveItem);
    }
    
    // Add top moves
    if (data.top_moves && data.top_moves.length > 0) {
        const topMovesTitle = document.createElement('div');
        topMovesTitle.className = 'analysis-item';
        topMovesTitle.style.borderBottom = '1px solid rgba(255, 255, 255, 0.1)';
        topMovesTitle.style.paddingBottom = '0.5rem';
        topMovesTitle.style.marginBottom = '0.5rem';
        
        const titleLabel = document.createElement('span');
        titleLabel.className = 'analysis-label';
        titleLabel.textContent = 'Лучшие ходы:';
        titleLabel.style.fontWeight = 'bold';
        
        topMovesTitle.appendChild(titleLabel);
        analysisContent.appendChild(topMovesTitle);
        
        data.top_moves.slice(0, 5).forEach((move, index) => {
            const moveItem = document.createElement('div');
            moveItem.className = 'analysis-item';
            
            const moveLabel = document.createElement('span');
            moveLabel.className = 'analysis-label';
            moveLabel.textContent = `${index + 1}. ${move.Move}`;
            
            const moveValue = document.createElement('span');
            moveValue.className = 'analysis-value';
            
            let valueText = '';
            if (move.Centipawn !== undefined) {
                const cp = move.Centipawn / 100;
                valueText = `${cp > 0 ? '+' : ''}${cp.toFixed(2)}`;
            } else if (move.Mate !== undefined) {
                valueText = `Мат в ${Math.abs(move.Mate)}`;
            }
            moveValue.textContent = valueText;
            
            moveItem.appendChild(moveLabel);
            moveItem.appendChild(moveValue);
            analysisContent.appendChild(moveItem);
        });
    }
    
    // Show the panel
    analysisPanel.style.display = 'block';
}

function addNavigationControls() {
    // Remove existing navigation if it exists
    const existingNav = document.getElementById('navigation-container');
    if (existingNav) {
        existingNav.remove();
    }
    
    // Create navigation container
    const navContainer = document.createElement('div');
    navContainer.id = 'navigation-container';
    navContainer.style.margin = '10px 0';
    navContainer.style.display = 'flex';
    navContainer.style.justifyContent = 'center';
    navContainer.style.gap = '10px';
    navContainer.style.flexWrap = 'wrap';
    
    // First move button
    const firstBtn = document.createElement('button');
    firstBtn.id = 'first-move';
    firstBtn.textContent = '⏮';
    firstBtn.title = 'Первый ход';
    firstBtn.addEventListener('click', goToFirstMove);
    
    // Previous move button
    const prevBtn = document.createElement('button');
    prevBtn.id = 'prev-move';
    prevBtn.textContent = '⬅';
    prevBtn.title = 'Предыдущий ход';
    prevBtn.addEventListener('click', goToPreviousMove);
    
    // Next move button
    const nextBtn = document.createElement('button');
    nextBtn.id = 'next-move';
    nextBtn.textContent = '➡';
    nextBtn.title = 'Следующий ход';
    nextBtn.addEventListener('click', goToNextMove);
    
    // Last move button
    const lastBtn = document.createElement('button');
    lastBtn.id = 'last-move';
    lastBtn.textContent = '⏭';
    lastBtn.title = 'Последний ход';
    lastBtn.addEventListener('click', goToLastMove);
    
    // Add buttons to container
    navContainer.appendChild(firstBtn);
    navContainer.appendChild(prevBtn);
    navContainer.appendChild(nextBtn);
    navContainer.appendChild(lastBtn);
    
    // Add container to page after button container
    const buttonContainer = document.getElementById('button-container');
    if (buttonContainer) {
        buttonContainer.parentNode.insertBefore(navContainer, buttonContainer.nextSibling);
    } else {
        document.querySelector('.container').insertBefore(navContainer, document.getElementById('status'));
    }
}

function goToFirstMove() {
    if (gameHistory.length > 0) {
        currentHistoryIndex = 0;
        board.position(gameHistory[currentHistoryIndex]);
        updateNavigationButtons();
    }
}

function goToPreviousMove() {
    if (gameHistory.length > 0 && currentHistoryIndex > 0) {
        currentHistoryIndex--;
        board.position(gameHistory[currentHistoryIndex]);
        updateNavigationButtons();
    }
}

function goToNextMove() {
    if (gameHistory.length > 0 && currentHistoryIndex < gameHistory.length - 1) {
        currentHistoryIndex++;
        board.position(gameHistory[currentHistoryIndex]);
        updateNavigationButtons();
    }
}

function goToLastMove() {
    if (gameHistory.length > 0) {
        currentHistoryIndex = gameHistory.length - 1;
        board.position(gameHistory[currentHistoryIndex]);
        updateNavigationButtons();
    }
}

function updateNavigationButtons() {
    const firstBtn = document.getElementById('first-move');
    const prevBtn = document.getElementById('prev-move');
    const nextBtn = document.getElementById('next-move');
    const lastBtn = document.getElementById('last-move');
    
    if (firstBtn && prevBtn && nextBtn && lastBtn) {
        firstBtn.disabled = currentHistoryIndex <= 0;
        prevBtn.disabled = currentHistoryIndex <= 0;
        nextBtn.disabled = currentHistoryIndex >= gameHistory.length - 1;
        lastBtn.disabled = currentHistoryIndex >= gameHistory.length - 1;
    }
}

socket.on('game_initialized', (data) => {
    console.log('Game initialized:', data);
    document.querySelector('.setup-screen').style.display = 'none';
    document.getElementById('game-section').style.display = 'block';
    gameActive = true;
    
    // Clear initialization timeout
    if (window.initTimeout) {
        clearTimeout(window.initTimeout);
        window.initTimeout = null;
    }
    
    // Clear previous history and move list
    gameHistory = [];
    currentHistoryIndex = -1;
    moveList = [];
    
    // Initialize chess.js for validation
    chess = new Chess(data.fen || 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');
    currentTurn = chess.turn();
    
    // Reset timers
    playerTimer = 0;
    aiTimer = 0;
    startTimer();

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
        onSnapEnd: onSnapEnd,
        orientation: data.player_color || playerColor,
        pieceTheme: 'https://unpkg.com/chessboardjs@1.0.0/dist/img/chesspieces/wikipedia/{piece}.png'
    });
    
    // Add initial position to history
    gameHistory.push(data.fen);
    currentHistoryIndex = 0;
    
    // Re-enable start button
    const startBtn = document.getElementById('start');
    if (startBtn) {
        startBtn.disabled = false;
        startBtn.textContent = 'Начать игру';
    }
    
    // Add reset button
    addResetButton();
    
    // Add flip board button handler
    const flipBtn = document.getElementById('flip-board');
    if (flipBtn) {
        flipBtn.addEventListener('click', flipBoard);
    }
    
    // Initialize move list display
    updateMoveListDisplay();
    
    // Update status
    const statusText = playerColor === 'white' ? 
        'Ваш ход: белые' : 'Ход компьютера: черные';
    document.getElementById('status').innerText = statusText;
    
    // Show success notification
    showNotification('Игра начата успешно!', 'success');
});

socket.on('preferences_loaded', (data) => {
    console.log('Preferences loaded:', data);
    if (data.preferences) {
        userPreferences = {...userPreferences, ...data.preferences};
        
        // Apply preferences
        applyUserPreferences();
    }
});

function applyUserPreferences() {
    // Apply default values to form
    const colorSelect = document.getElementById('color');
    if (colorSelect) {
        colorSelect.value = userPreferences.defaultColor;
    }
    // Update color button
    const colorBtn = document.querySelector(`.color-btn[data-color="${userPreferences.defaultColor}"]`);
    if (colorBtn) {
        document.querySelectorAll('.color-btn').forEach(b => b.classList.remove('active'));
        colorBtn.classList.add('active');
    }
    const levelInput = document.getElementById('level');
    if (levelInput) {
        levelInput.value = userPreferences.defaultDifficulty;
    }
    
    // Apply board flip if needed
    if (board && userPreferences.autoFlipBoard && !isFlipped) {
        flipBoard();
    }
}

function saveUserPreferences() {
    const activeColorBtn = document.querySelector('.color-btn.active');
    userPreferences.defaultColor = activeColorBtn ? activeColorBtn.dataset.color : 'white';
    const levelInput = document.getElementById('level');
    userPreferences.defaultDifficulty = levelInput ? parseInt(levelInput.value) : 5;
    
    socket.emit('save_preferences', {
        preferences: userPreferences
    });
}

function onDragStart(source, piece, position, orientation) {
    if (!gameActive || !chess) return false;
    
    // Разрешаем ход только своей фигурой
    const isWhite = piece.startsWith('w');
    const isPlayerWhite = (playerColor === 'white');
    const isPlayerTurn = (chess.turn() === 'w') === isPlayerWhite;
    
    if (!isPlayerTurn || isPlayerWhite !== isWhite) {
        return false;
    }
    
    // Show possible moves for this piece
    if (userPreferences.showPossibleMoves && chess) {
        showPossibleMoves(source);
    }
    
    return true;
}

function onDrop(source, target) {
    if (!chess) return 'snapback';
    
    const move = {
        from: source,
        to: target,
        promotion: 'q' // Default to queen promotion
    };
    
    // Check if this is a valid move using chess.js
    const legalMove = chess.move(move);
    
    if (!legalMove) {
        // Invalid move - snap back
        console.log('Invalid move:', move);
        showNotification('Недопустимый ход!', 'error');
        return 'snapback';
    }
    
    // Valid move - convert to UCI format for server
    const uciMove = source + target;
    if (legalMove.promotion) {
        move.promotion = legalMove.promotion;
    }
    
    console.log('Making move:', uciMove, legalMove);
    
    // Play move sound
    if (moveSound) moveSound();
    
    // Show move processing status
    document.getElementById('status').innerText = '⏳ Обработка хода...';
    
    // Disable board interaction during move processing
    gameActive = false;
    
    // Update turn
    currentTurn = chess.turn();
    
    // Clear possible moves
    removeGreySquares();
    
    // Send move to server
    socket.emit('make_move', { move: uciMove });
    
    // Update board position from chess.js
    board.position(chess.fen());
    
    return null; // Allow the move
}

function onSnapEnd() {
    // This is called after a piece is dropped
    // We can use it to update the board position
    if (chess) {
        board.position(chess.fen());
    }
}

function onMouseoverSquare(square, piece) {
    if (piece && userPreferences.showPossibleMoves && chess && gameActive) {
        const isWhite = piece.startsWith('w');
        const isPlayerWhite = (playerColor === 'white');
        const isPlayerTurn = (chess.turn() === 'w') === isPlayerWhite;
        
        if (isPlayerTurn && isPlayerWhite === isWhite) {
            showPossibleMoves(square);
        }
    } else {
        removeGreySquares();
    }
}

function onMouseoutSquare(square, piece) {
    if (userPreferences.showPossibleMoves) {
        removeGreySquares();
    }
}

let greySquares = [];

function showPossibleMoves(square) {
    if (!chess || !gameActive) return;
    
    // Get all legal moves from this square
    const moves = chess.moves({ square: square, verbose: true });
    
    // Highlight the source square
    const sourceSquare = document.querySelector(`#board .square-${square}`);
    if (sourceSquare) {
        sourceSquare.style.background = 'rgba(99, 102, 241, 0.4)';
        greySquares.push(square);
    }
    
    // Highlight all possible destination squares
    moves.forEach(move => {
        const targetSquare = document.querySelector(`#board .square-${move.to}`);
        if (targetSquare) {
            // Check if it's a capture
            const pieceOnSquare = board.position()[move.to];
            if (pieceOnSquare) {
                targetSquare.style.background = 'rgba(239, 68, 68, 0.6)'; // Red for captures
            } else {
                targetSquare.style.background = 'rgba(16, 185, 129, 0.5)'; // Green for regular moves
            }
            greySquares.push(move.to);
        }
    });
}

function removeGreySquares() {
    greySquares.forEach(square => {
        const squareEl = document.querySelector(`#board .square-${square}`);
        if (squareEl) {
            squareEl.style.background = '';
        }
    });
    greySquares = [];
}

// Обработка обновления позиции
socket.on('position_update', (data) => {
    console.log('Position update:', data);
    if (board && chess) {
        // Update chess.js position
        chess.load(data.fen);
        currentTurn = chess.turn();
        
        // Update board display
        board.position(data.fen);
        gameHistory.push(data.fen);
        currentHistoryIndex = gameHistory.length - 1;
        updateNavigationButtons();
        
        // Highlight the last move if provided
        if (data.last_move || data.ai_move) {
            const move = data.ai_move || data.last_move;
            highlightMove(move);
            if (!data.takeback) { // Only add to move list if not a takeback
                const moveNotation = chess.history({verbose: true}).slice(-1)[0];
                if (moveNotation) {
                    addMoveToList(moveNotation.san || move);
                } else {
                    addMoveToList(move);
                }
                // Update move counter
                const moveNumberEl = document.getElementById('move-number');
                if (moveNumberEl && chess) {
                    const history = chess.history();
                    moveNumberEl.textContent = Math.ceil(history.length / 2) + 1;
                }
            }
        }
        
        // Play capture sound if it was a capture
        if (data.ai_move && (data.ai_move.includes('x') || data.ai_move.length > 4)) {
            if (captureSound) captureSound();
        } else {
            if (moveSound) moveSound();
        }
        
        // Re-enable board interaction
        gameActive = true;
        
        // Update timers
        updateTimer(data.ai_move ? 'ai' : 'player');
        
        // Show AI move if provided
        if (data.ai_move) {
            document.getElementById('status').innerText = `Компьютер сходил: ${data.ai_move}`;
            showNotification(`Компьютер сходил: ${data.ai_move}`, 'info');
        } else if (data.takeback) {
            document.getElementById('status').innerText = 'Ход отменен';
            showNotification('Ход отменен', 'info');
            // Reload chess.js to previous position
            if (gameHistory.length > 0) {
                chess.load(gameHistory[currentHistoryIndex]);
            }
        } else {
            document.getElementById('status').innerText = playerColor === 'white' ? 
                'Ваш ход: белые' : 'Ваш ход: черные';
        }
        
        // Check for check in status
        if (chess.in_check()) {
            if (checkSound) checkSound();
            document.getElementById('status').innerText += ' ⚠️ Шах!';
            showNotification('Шах!', 'warning');
        }
        
        // Check for checkmate/stalemate
        if (chess.is_checkmate()) {
            const winner = chess.turn() === 'w' ? 'black' : 'white';
            socket.emit('game_over', { result: 'checkmate', winner: winner });
        } else if (chess.is_stalemate() || chess.is_draw()) {
            socket.emit('game_over', { result: 'draw' });
        }
    }
});

socket.on('game_over', (data) => {
    console.log('Game over:', data);
    gameActive = false;
    if (board) {
        board.position(data.fen);
        gameHistory.push(data.fen);
        currentHistoryIndex = gameHistory.length - 1;
        updateNavigationButtons();
        
        // Highlight the last move if provided
        if (data.last_move) {
            highlightMove(data.last_move);
            addMoveToList(data.last_move);
        }
    }
    
    // Play game over sound
    if (gameOverSound) gameOverSound();
    
    let msg = '';
    let notificationMsg = '';
    if (data.result === 'checkmate') {
        if (data.winner === playerColor) {
            msg = '🏆 Поздравляем! Вы выиграли!';
            notificationMsg = 'Поздравляем! Вы выиграли!';
        } else {
            msg = '❌ Шах и мат! Вы проиграли.';
            notificationMsg = 'Шах и мат! Вы проиграли.';
        }
    } else if (data.result === 'stalemate') {
        msg = '🤝 Ничья (пат)!';
        notificationMsg = 'Ничья (пат)!';
    }
    
    document.getElementById('status').innerText = msg;
    
    // Add visual effect for game over
    const statusElement = document.getElementById('status');
    statusElement.style.animation = 'pulse 1s infinite';
    
    // Show notification
    showNotification(notificationMsg, data.result === 'checkmate' ? 
        (data.winner === playerColor ? 'success' : 'error') : 'info');
});

socket.on('invalid_move', (data) => {
    console.log('Invalid move:', data);
    
    // Re-enable board interaction
    gameActive = true;
    
    const errorMsg = data.message || 'Недопустимый ход';
    document.getElementById('status').innerText = '❌ ' + errorMsg;
    
    // Show error notification
    showNotification(errorMsg, 'error');
});

// Handle AI thinking indicator
socket.on('ai_thinking', (data) => {
    if (data.status === 'calculating') {
        document.getElementById('status').innerText = '🤔 Компьютер думает...';
        // Add visual indicator
        const statusEl = document.getElementById('status');
        statusEl.style.fontWeight = 'bold';
        statusEl.style.color = '#4CAF50';
    } else if (data.status === 'complete') {
        const time = data.time ? ` (${data.time.toFixed(2)}с)` : '';
        document.getElementById('status').innerText = `✓ Ход рассчитан${time}`;
        setTimeout(() => {
            const statusEl = document.getElementById('status');
            statusEl.style.fontWeight = 'normal';
            statusEl.style.color = '';
        }, 1000);
    } else if (data.status === 'error') {
        document.getElementById('status').innerText = '⚠️ Ошибка расчета хода';
        const statusEl = document.getElementById('status');
        statusEl.style.fontWeight = 'normal';
        statusEl.style.color = '';
    }
});

socket.on('error', (data) => {
    console.log('Error:', data);
    
    // Clear initialization timeout
    if (window.initTimeout) {
        clearTimeout(window.initTimeout);
        window.initTimeout = null;
    }
    
    // Re-enable board interaction and start button
    gameActive = false;
    const startBtn = document.getElementById('start');
    if (startBtn) {
        startBtn.disabled = false;
        startBtn.textContent = 'Начать игру';
    }
    
    // Handle specific error types
    let errorMessage = data.message || 'Неизвестная ошибка';
    if (errorMessage.includes('engine')) {
        errorMessage = 'Ошибка движка Stockfish. Попробуйте перезапустить игру.';
    } else if (errorMessage.includes('session')) {
        errorMessage = 'Ошибка сессии. Попробуйте обновить страницу.';
    } else if (errorMessage.includes('overload') || errorMessage.includes('limit')) {
        errorMessage = 'Сервер перегружен. Попробуйте позже.';
    } else if (errorMessage.includes('initialization')) {
        errorMessage = 'Ошибка инициализации. Попробуйте перезапустить игру.';
    } else if (errorMessage.includes('move')) {
        errorMessage = 'Ошибка обработки хода. Попробуйте повторить ход.';
    } else if (errorMessage.includes('timeout')) {
        errorMessage = 'Превышено время ожидания. Попробуйте еще раз.';
    }
    
    document.getElementById('status').innerText = '⚠️ Ошибка: ' + errorMessage;
    
    // Show error notification
    showNotification(errorMessage, 'error');
});

socket.on('analysis_result', (data) => {
    console.log('Analysis result:', data);
    document.getElementById('status').innerText = 'Анализ завершен';
    displayAnalysis(data);
    
    // Show info notification
    showNotification('Анализ завершен', 'info');
});

socket.on('game_saved', (data) => {
    if (data.success) {
        savedGameState = data.game_state;
        document.getElementById('status').innerText = 'Игра сохранена успешно!';
        
        // Show success notification
        showNotification('Игра сохранена успешно!', 'success');
    } else {
        document.getElementById('status').innerText = 'Ошибка сохранения игры';
        showNotification('Ошибка сохранения игры', 'error');
    }
});

socket.on('game_loaded', (data) => {
    console.log('Game loaded:', data);
    
    // Reset current game state
    if (board) {
        board.destroy();
    }
    
    document.getElementById('setup').style.display = 'none';
    document.getElementById('board').style.display = 'block';
    
    // Initialize board with loaded position
    board = Chessboard('board', {
        position: data.fen,
        draggable: true,
        onDragStart: onDragStart,
        onDrop: onDrop,
        onMouseoutSquare: onMouseoutSquare,
        onMouseoverSquare: onMouseoverSquare,
        orientation: data.player_color,
        pieceTheme: 'https://unpkg.com/chessboardjs@1.0.0/dist/img/chesspieces/wikipedia/{piece}.png'
    });
    
    // Update game state
    playerColor = data.player_color;
    gameActive = true;
    gameHistory = data.game_history || [];
    currentHistoryIndex = gameHistory.length > 0 ? gameHistory.length - 1 : 0;
    
    // Add initial position to history if empty
    if (gameHistory.length === 0) {
        gameHistory.push(data.fen);
        currentHistoryIndex = 0;
    }
    
    // Update UI
    updateNavigationButtons();
    document.getElementById('status').innerText = 'Игра загружена успешно!';
    
    // Show success notification
    showNotification('Игра загружена успешно!', 'success');
});

function addMoveToList(move) {
    // Add move to the move list
    moveList.push(move);
    
    // Update the move list display
    updateMoveListDisplay();
}

function updateMoveListDisplay() {
    const moveListEl = document.getElementById('move-list');
    if (!moveListEl) return;
    
    // Clear existing content
    moveListEl.innerHTML = '';
    
    if (moveList.length === 0) {
        moveListEl.innerHTML = '<div class="move-list-empty">Ходов пока нет</div>';
        return;
    }
    
    // Group moves by pair (white + black)
    for (let i = 0; i < moveList.length; i += 2) {
        const movePair = document.createElement('div');
        movePair.className = 'move-item';
        
        const moveNumber = Math.floor(i / 2) + 1;
        const whiteMove = moveList[i];
        const blackMove = moveList[i + 1];
        
        movePair.innerHTML = `
            <span class="move-number">${moveNumber}.</span>
            <span class="move-white">${whiteMove}</span>
            ${blackMove ? `<span class="move-black">${blackMove}</span>` : ''}
        `;
        
        moveListEl.appendChild(movePair);
    }
    
    // Scroll to bottom
    moveListEl.scrollTop = moveListEl.scrollHeight;
}

// Timer functions
function startTimer() {
    if (timerInterval) clearInterval(timerInterval);
    
    timerInterval = setInterval(() => {
        if (gameActive) {
            // Determine whose turn it is
            const isPlayerTurn = (chess && chess.turn() === 'w') === (playerColor === 'white');
            
            if (isPlayerTurn) {
                playerTimer++;
            } else {
                aiTimer++;
            }
        }
        
        updateTimerDisplay();
    }, 1000);
}

function updateTimer(turn) {
    // This can be called when a move is made to switch timer
    updateTimerDisplay();
}

function updateTimerDisplay() {
    const playerTimerEl = document.getElementById('player-timer');
    const aiTimerEl = document.getElementById('ai-timer');
    
    if (playerTimerEl) {
        playerTimerEl.textContent = formatTime(playerTimer);
    }
    
    if (aiTimerEl) {
        aiTimerEl.textContent = formatTime(aiTimer);
    }
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

// Flip board function
function flipBoard() {
    if (!board) return;
    
    isFlipped = !isFlipped;
    board.orientation(isFlipped ? (playerColor === 'white' ? 'black' : 'white') : playerColor);
}

// Notification function (override if exists from HTML)
window.showNotification = function(message, type = 'info') {
    const container = document.getElementById('notification-container');
    if (!container) {
        // Fallback if container doesn't exist
        console.log(`[${type}] ${message}`);
        return;
    }
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    container.appendChild(notification);
    
    // Trigger animation
    setTimeout(() => {
        notification.classList.add('notification-show');
    }, 10);
    
    // Remove after delay
    setTimeout(() => {
        notification.classList.remove('notification-show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 3000);
};

// Add move highlighting functionality
function highlightMove(move) {
    if (!board) return;
    
    // Remove previous highlights
    removeMoveHighlights();
    
    // Highlight source and target squares
    if (move && move.length >= 4) {
        const sourceSquare = move.substring(0, 2);
        const targetSquare = move.substring(2, 4);
        
        // Add highlight class to squares
        const sourceEl = document.querySelector(`#board .square-${sourceSquare}`);
        const targetEl = document.querySelector(`#board .square-${targetSquare}`);
        
        if (sourceEl) sourceEl.classList.add('highlight');
        if (targetEl) targetEl.classList.add('highlight');
    }
}

function removeMoveHighlights() {
    // Remove highlight class from all squares
    const highlightedSquares = document.querySelectorAll('#board .square-55d63.highlight');
    highlightedSquares.forEach(square => {
        square.classList.remove('highlight');
    });
}
