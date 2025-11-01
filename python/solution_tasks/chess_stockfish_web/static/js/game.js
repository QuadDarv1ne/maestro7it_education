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

document.getElementById('start').addEventListener('click', () => {
    playerColor = document.getElementById('color').value;
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
    startBtn.textContent = 'Загрузка...';
    
    // Update status to show we're initializing
    document.getElementById('status').innerText = '⏳ Инициализация игры...';
    
    // Set a timeout to handle initialization errors
    const initTimeout = setTimeout(() => {
        document.getElementById('status').innerText = '⚠️ Превышено время ожидания инициализации. Попробуйте еще раз.';
        startBtn.disabled = false;
        startBtn.textContent = 'Начать игру';
        showNotification('Превышено время ожидания инициализации. Попробуйте еще раз.', 'error');
    }, 30000); // 30 seconds timeout
    
    // Store timeout ID to clear it later
    window.initTimeout = initTimeout;
    
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
    
    // Create button container
    const buttonContainer = document.createElement('div');
    buttonContainer.id = 'button-container';
    buttonContainer.style.margin = '10px 0';
    buttonContainer.style.display = 'flex';
    buttonContainer.style.justifyContent = 'center';
    buttonContainer.style.gap = '10px';
    buttonContainer.style.flexWrap = 'wrap';
    
    // Create reset button
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
        currentHistoryIndex = -1;
        moveList = [];
        savedGameState = null;
        
        // Remove navigation buttons
        const navContainer = document.getElementById('navigation-container');
        if (navContainer) {
            navContainer.remove();
        }
        
        // Remove analysis panel
        const analysisPanel = document.getElementById('analysis-panel');
        if (analysisPanel) {
            analysisPanel.remove();
        }
        
        // Remove save/load buttons
        const saveLoadContainer = document.getElementById('save-load-container');
        if (saveLoadContainer) {
            saveLoadContainer.remove();
        }
        
        // Remove preferences button
        const preferencesBtn = document.getElementById('preferences-btn');
        if (preferencesBtn) {
            preferencesBtn.remove();
        }
        
        // Remove move list
        const moveListPanel = document.getElementById('move-list');
        if (moveListPanel) {
            moveListPanel.remove();
        }
        
        // Remove button container
        const buttonContainer = document.getElementById('button-container');
        if (buttonContainer) {
            buttonContainer.remove();
        }
        
        document.getElementById('status').innerText = 'Готовы начать игру!';
    });
    
    // Create takeback button
    const takebackBtn = document.createElement('button');
    takebackBtn.id = 'takeback';
    takebackBtn.textContent = '↩️ Отменить ход';
    takebackBtn.addEventListener('click', takebackMove);
    
    // Create analyze button
    const analyzeBtn = document.createElement('button');
    analyzeBtn.id = 'analyze';
    analyzeBtn.textContent = 'Анализ';
    analyzeBtn.addEventListener('click', analyzePosition);
    
    // Add buttons to container
    buttonContainer.appendChild(resetBtn);
    buttonContainer.appendChild(takebackBtn);
    buttonContainer.appendChild(analyzeBtn);
    
    // Add container to page
    document.querySelector('.container').insertBefore(buttonContainer, document.getElementById('status'));
    
    // Add save/load buttons
    addSaveLoadButtons();
    
    // Add preferences button
    addPreferencesButton();
    
    // Add navigation controls
    addNavigationControls();
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
    // Remove existing analysis panel if it exists
    const existingPanel = document.getElementById('analysis-panel');
    if (existingPanel) {
        existingPanel.remove();
    }
    
    // Create analysis panel
    const analysisPanel = document.createElement('div');
    analysisPanel.id = 'analysis-panel';
    analysisPanel.style.margin = '15px 0';
    analysisPanel.style.padding = '15px';
    analysisPanel.style.background = 'rgba(255, 255, 255, 0.1)';
    analysisPanel.style.borderRadius = '10px';
    analysisPanel.style.textAlign = 'left';
    
    // Add title
    const title = document.createElement('h3');
    title.textContent = 'Анализ позиции';
    title.style.color = '#4FC3F7';
    title.style.marginTop = '0';
    analysisPanel.appendChild(title);
    
    // Add evaluation
    if (data.evaluation) {
        const evalDiv = document.createElement('div');
        evalDiv.style.marginBottom = '10px';
        
        let evalText = 'Оценка: ';
        if (data.evaluation.type === 'mate') {
            evalText += `Мат в ${Math.abs(data.evaluation.value)} ходов`;
            evalText += data.evaluation.value > 0 ? ' (белые)' : ' (черные)';
        } else if (data.evaluation.type === 'cp') {
            const cp = data.evaluation.value / 100;
            evalText += `${cp > 0 ? '+' : ''}${cp.toFixed(2)}`;
        } else {
            evalText += 'Неопределено';
        }
        
        evalDiv.textContent = evalText;
        analysisPanel.appendChild(evalDiv);
    }
    
    // Add best move
    if (data.best_move) {
        const bestMoveDiv = document.createElement('div');
        bestMoveDiv.style.marginBottom = '10px';
        bestMoveDiv.textContent = `Лучший ход: ${data.best_move}`;
        analysisPanel.appendChild(bestMoveDiv);
    }
    
    // Add top moves
    if (data.top_moves && data.top_moves.length > 0) {
        const topMovesDiv = document.createElement('div');
        topMovesDiv.style.marginBottom = '10px';
        
        const topMovesTitle = document.createElement('div');
        topMovesTitle.textContent = 'Лучшие ходы:';
        topMovesTitle.style.fontWeight = 'bold';
        topMovesDiv.appendChild(topMovesTitle);
        
        const movesList = document.createElement('ul');
        movesList.style.paddingLeft = '20px';
        movesList.style.margin = '5px 0';
        
        data.top_moves.forEach(move => {
            const moveItem = document.createElement('li');
            let moveText = move.Move;
            if (move.Centipawn !== undefined) {
                const cp = move.Centipawn / 100;
                moveText += ` (${cp > 0 ? '+' : ''}${cp.toFixed(2)})`;
            } else if (move.Mate !== undefined) {
                moveText += ` (Мат в ${Math.abs(move.Mate)} ходов)`;
            }
            moveItem.textContent = moveText;
            movesList.appendChild(moveItem);
        });
        
        topMovesDiv.appendChild(movesList);
        analysisPanel.appendChild(topMovesDiv);
    }
    
    // Add close button
    const closeBtn = document.createElement('button');
    closeBtn.textContent = 'Закрыть';
    closeBtn.style.cssText = 'padding: 5px 10px; font-size: 14px; margin-top: 10px;';
    closeBtn.addEventListener('click', () => {
        analysisPanel.remove();
    });
    analysisPanel.appendChild(closeBtn);
    
    // Insert after navigation container
    const navContainer = document.getElementById('navigation-container');
    if (navContainer) {
        navContainer.parentNode.insertBefore(analysisPanel, navContainer.nextSibling);
    } else {
        document.querySelector('.container').insertBefore(analysisPanel, document.getElementById('status'));
    }
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
    document.getElementById('setup').style.display = 'none';
    document.getElementById('board').style.display = 'block';
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
    
    // Add initial position to history
    gameHistory.push(data.fen);
    currentHistoryIndex = 0;
    
    // Re-enable start button
    const startBtn = document.getElementById('start');
    startBtn.disabled = false;
    startBtn.textContent = 'Начать игру';
    
    // Add reset button
    addResetButton();
    
    // Update status
    document.getElementById('status').innerText = playerColor === 'white' ? 
        'Ваш ход: белые' : 'Ход компьютера: черные';
    
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
    document.getElementById('color').value = userPreferences.defaultColor;
    document.getElementById('level').value = userPreferences.defaultDifficulty;
    
    // Apply board flip if needed
    if (board && userPreferences.autoFlipBoard && !isFlipped) {
        flipBoard();
    }
}

function saveUserPreferences() {
    userPreferences.defaultColor = document.getElementById('color').value;
    userPreferences.defaultDifficulty = parseInt(document.getElementById('level').value);
    
    socket.emit('save_preferences', {
        preferences: userPreferences
    });
}

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
    
    // Play move sound
    if (moveSound) moveSound();
    
    // Show move processing status
    document.getElementById('status').innerText = '⏳ Обработка хода...';
    
    // Disable board interaction during move processing
    gameActive = false;
    
    socket.emit('make_move', { move: move });
    removeGreySquares();
}

function onMouseoverSquare(square, piece) {
    if (piece && userPreferences.showPossibleMoves) greySquare(square);
}

function onMouseoutSquare(square, piece) {
    if (userPreferences.showPossibleMoves) removeGreySquares();
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
        currentHistoryIndex = gameHistory.length - 1;
        updateNavigationButtons();
        
        // Highlight the last move if provided
        if (data.last_move || data.ai_move) {
            const move = data.ai_move || data.last_move;
            highlightMove(move);
            if (!data.takeback) { // Only add to move list if not a takeback
                addMoveToList(move);
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
        
        // Show AI move if provided
        if (data.ai_move) {
            document.getElementById('status').innerText = `Компьютер сходил: ${data.ai_move}`;
            showNotification(`Компьютер сходил: ${data.ai_move}`, 'info');
        } else if (data.takeback) {
            document.getElementById('status').innerText = 'Ход отменен';
            showNotification('Ход отменен', 'info');
        } else {
            document.getElementById('status').innerText = playerColor === 'white' ? 
                'Ваш ход: белые' : 'Ваш ход: черные';
        }
        
        // Check for check in status
        if (data.fen && data.fen.includes('+')) {
            if (checkSound) checkSound();
            document.getElementById('status').innerText += ' ⚠️ Шах!';
            showNotification('Шах!', 'warning');
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
    // Remove existing move list if it exists
    const existingMoveList = document.getElementById('move-list');
    if (existingMoveList) {
        existingMoveList.remove();
    }
    
    // Create move list panel
    const moveListPanel = document.createElement('div');
    moveListPanel.id = 'move-list';
    
    // Add title
    const title = document.createElement('h3');
    title.textContent = 'Ходы';
    moveListPanel.appendChild(title);
    
    // Add move list
    const moveListOl = document.createElement('ol');
    moveList.forEach((move, index) => {
        const moveItem = document.createElement('li');
        moveItem.textContent = move;
        moveListOl.appendChild(moveItem);
    });
    moveListPanel.appendChild(moveListOl);
    
    // Insert after navigation container
    const navContainer = document.getElementById('navigation-container');
    if (navContainer) {
        navContainer.parentNode.insertBefore(moveListPanel, navContainer.nextSibling);
    } else {
        document.querySelector('.container').insertBefore(moveListPanel, document.getElementById('status'));
    }
}

// New function to show notifications
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification';
    
    // Set styles based on type
    switch (type) {
        case 'success':
            notification.style.background = 'rgba(76, 175, 80, 0.9)';
            break;
        case 'error':
            notification.style.background = 'rgba(244, 67, 54, 0.9)';
            break;
        case 'warning':
            notification.style.background = 'rgba(255, 152, 0, 0.9)';
            break;
        case 'info':
        default:
            notification.style.background = 'rgba(33, 150, 243, 0.9)';
            break;
    }
    
    notification.textContent = message;
    
    // Add to document
    document.body.appendChild(notification);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

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
