// Импортируем необходимые классы
// В браузерной среде они должны быть доступны через window

class PacmanGame {
    constructor() {
        // Инициализация холста
        this.canvas = document.getElementById('game-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.cellSize = 22;
        
        // Игровые параметры
        this.isRunning = false;
        this.animationFrameId = null;
        this.lastTimestamp = 0;
        this.updateInterval = 150; // Интервал обновления в миллисекундах (замедляет игру)
        this.lastUpdate = 0;
        
        // Инициализация игровых объектов
        this.pacman = new Pacman(10, 15);
        this.ghosts = [
            new Ghost(10, 8, 'red', 'Blinky'),
            new Ghost(9, 9, 'pink', 'Pinky'),
            new Ghost(11, 9, 'cyan', 'Inky'),
            new Ghost(10, 10, 'orange', 'Clyde')
        ];
        
        // Инициализация карты
        this.gameMap = new GameMap();
        
        // Игровое состояние
        this.score = 0;
        this.level = 1;
        this.lives = 3;
        this.selectedLevel = 1; // Default level
        
        // Система бонусов
        this.consecutiveEats = 0;  // Система последовательного поедания
        this.lastEatTime = 0;      // Время последнего поедания
        this.comboBonus = 0;       // Бонус за комбо
        this.comboDisplay = null;  // Отображение комбо
        
        // Инициализация менеджеров
        this.particleManager = new ParticleManager();
        this.soundManager = new SoundManager();
        this.fruitManager = new FruitManager();
        this.achievementManager = new AchievementManager();
        
        // Подсчет еды
        this.foodCount = 0;
        this.totalFood = 0;
        this.countFood();
        
        // Рекорды
        this.highScores = this.loadHighScores();  // Рекорды
        
        // Настройки
        this.settings = this.loadSettings();  // Настройки
        
        // Инициализация событий
        this.setupEventListeners();
        
        // Первичная отрисовка
        this.draw();
        
        console.log("Игра инициализирована");
    }
    
    // Метод для подсчета еды на карте
    countFood() {
        this.totalFood = this.gameMap.countFood(this.gameMap.getLevelMap(this.level));
        console.log("Всего еды:", this.totalFood);
        // Set the food count for achievement tracking
        this.achievementManager.setLevelFoodCount(this.totalFood);
    }
    
    // Метод для сброса игры
    reset() {
        console.log("Сброс игры");
        this.isRunning = false;
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
        }
        
        // Сброс игровых объектов
        this.pacman.resetPosition();
        this.ghosts.forEach(ghost => ghost.resetPosition());
        
        // Сброс карты
        this.resetMap();
        
        // Сброс состояния игры
        this.score = 0;
        this.level = 1;
        this.lives = 3;
        this.foodCount = 0;
        this.countFood();
        
        // Сброс системы бонусов
        this.consecutiveEats = 0;
        this.comboBonus = 0;
        this.comboDisplay = null;
        
        // Сброс менеджеров
        this.particleManager.clearParticles();
        this.fruitManager.reset();
        this.achievementManager.reset();
        
        // Сброс времени начала уровня для достижения "Скоростной демон"
        this.achievementManager.setLevelStartTime();
        
        this.updateScore();
        this.updateLives();
        this.updateLevel();
        
        // Перерисовка
        this.draw();
        
        console.log("Игра сброшена");
    }
    
    // Метод для сброса позиций
    resetPositions() {
        console.log("Сброс позиций");
        this.pacman.resetPosition();
        this.ghosts.forEach(ghost => ghost.resetPosition());
        this.particleManager.clearParticles();
    }
    
    // Метод для сброса карты
    resetMap() {
        console.log("Сброс карты");
        const currentMap = this.gameMap.getLevelMap(this.level);
        // Здесь должна быть логика сброса карты к исходному состоянию
        // Для простоты мы просто пересоздаем карту
        this.foodCount = 0;
        this.countFood();
        // Reset food eaten counter for achievement tracking
        this.achievementManager.setLevelFoodCount(this.totalFood);
    }
    
    // Метод для запуска игры
    start() {
        console.log("Запуск игры");
        if (!this.isRunning) {
            this.isRunning = true;
            // Set the level start time for achievement tracking
            this.achievementManager.setLevelStartTime();
            this.gameLoop();
        }
    }
    
    // Метод для перехода на следующий уровень
    nextLevel() {
        console.log("Переход на следующий уровень");
        this.level++;
        this.foodCount = 0;
        
        // Сброс позиций
        this.pacman.resetPosition();
        this.ghosts.forEach(ghost => ghost.resetPosition());
        
        // Сброс менеджеров
        this.particleManager.clearParticles();
        this.fruitManager.reset();
        
        // Подсчет еды на новом уровне
        this.countFood();
        
        // Set the level start time for achievement tracking
        this.achievementManager.setLevelStartTime();
        
        // Увеличение сложности
        this.increaseDifficulty();
        
        this.updateLevel();
        this.draw();
    }
    
    // Метод для проверки завершения уровня
    checkLevelComplete() {
        if (this.foodCount >= this.totalFood) {
            console.log("Уровень завершен");
            // Добавляем очки за завершение уровня
            this.score += 1000 * this.level;
            
            // Проверяем достижение "Перфекционист"
            this.achievementManager.checkAchievements(this.score, this.level, this.consecutiveEats);
            
            // Переход на следующий уровень
            this.nextLevel();
        }
    }
    
    // Метод для обработки столкновений
    checkCollisions() {
        // Проверяем сбор еды
        const cell = this.map[this.pacman.y][this.pacman.x];
        if (cell === 2) { // Обычная еда
            this.map[this.pacman.y][this.pacman.x] = 1;
            this.foodCount++;
            this.score += 10;
            this.playSound('eat');
            this.createCombo();
            // Создаем визуальный эффект при сборе обычной еды
            this.createFoodParticles(this.pacman.x, this.pacman.y, false);
            this.updateScore();
            this.checkLevelComplete();
            // Increment food eaten for achievement tracking
            this.achievementManager.incrementFoodEaten();
        } else if (cell === 3) { // Супер-еда
            this.map[this.pacman.y][this.pacman.x] = 1;
            this.foodCount++;
            this.score += 50;
            this.pacman.powerMode = true;
            this.pacman.powerModeTimer = 10000; // 10 секунд
            this.canvas.classList.add('power-mode');
            this.playSound('power');
            this.createCombo();
            // Создаем визуальный эффект при сборе супер-еды
            this.createFoodParticles(this.pacman.x, this.pacman.y, true);
            // Добавляем дополнительный эффект для супер-еды
            this.createSuperFoodEffect(this.pacman.x, this.pacman.y);
            this.updateScore();
            this.checkLevelComplete();
            // Increment food eaten for achievement tracking
            this.achievementManager.incrementFoodEaten();
        }
        
        // Проверяем сбор фрукта
        this.checkFruitCollection();
        
        // Проверяем столкновения с привидениями
        this.ghosts.forEach(ghost => {
            if (this.pacman.x === ghost.x && this.pacman.y === ghost.y) {
                if (this.pacman.powerMode) {
                    // Пакман съедает привидение
                    this.score += 200;
                    this.achievementManager.incrementGhostsEaten(); // Track for achievements
                    this.playSound('ghost');
                    this.createParticles(ghost.x, ghost.y, ghost.color);
                    // Создаем специальный эффект при поедании привидения
                    this.createGhostEatenEffect(ghost.x, ghost.y, ghost.color);
                    // Возвращаем привидение на начальную позицию
                    ghost.x = 10;
                    ghost.y = ghost.color === 'red' ? 8 : ghost.color === 'pink' ? 9 : 
                              ghost.color === 'cyan' ? 9 : 10;
                    this.updateScore();
                    // Check achievements after eating a ghost
                    this.achievementManager.checkAchievements(this.score, this.level, this.consecutiveEats);
                } else {
                    // Привидение съедает Пакмана
                    this.lives--;
                    this.updateLives();
                    this.playSound('death');
                    this.createParticles(this.pacman.x, this.pacman.y, 'yellow');
                    // Создаем специальный эффект при потере жизни
                    this.createLifeLostEffect(this.pacman.x, this.pacman.y);
                    
                    if (this.lives <= 0) {
                        this.gameOver();
                    } else {
                        // Возвращаем Пакмана и привидений на начальные позиции
                        this.resetPositions();
                    }
                }
            }
        });
    }
    
    // Проверяем сбор фрукта
    checkFruitCollection() {
        const fruitPoints = this.fruitManager.checkFruitCollection(
            this.pacman.x, 
            this.pacman.y,
            (points) => {
                this.score += points;
                this.updateScore();
            },
            (x, y, color) => {
                this.createParticles(x, y, color);
                this.achievementManager.incrementFruitsCollected(); // Track for achievements
                this.achievementManager.checkAchievements(this.score, this.level, this.consecutiveEats);
            }
        );
        
        if (fruitPoints > 0) {
            this.score += fruitPoints;
            this.updateScore();
        }
    }
    
    // Метод для завершения игры
    gameOver() {
        console.log("Игра окончена");
        this.isRunning = false;
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
        }
        
        // Сохраняем рекорд
        this.saveHighScore();
        
        // Проверяем достижения
        this.achievementManager.checkAchievements(this.score, this.level, this.consecutiveEats);
        
        // Показываем сообщение
        this.showMessage(`Игра окончена!<br>Ваш счет: ${this.score}<br>Достигнутый уровень: ${this.level}`);
        
        // Воспроизводим звук окончания игры
        this.playSound('gameover');
    }
    
    // Метод для установки обработчиков событий
    setupEventListeners() {
        // Обработчики для кнопок меню
        document.getElementById('play-btn').addEventListener('click', () => {
            this.soundManager.playSound('start');
            this.hideMenu();
            this.start();
        });
        
        document.getElementById('level-select-btn').addEventListener('click', () => {
            this.soundManager.playSound('start');
            this.showLevelSelect();
        });
        
        document.getElementById('settings-btn').addEventListener('click', () => {
            this.soundManager.playSound('start');
            this.showSettings();
        });
        
        document.getElementById('highscores-btn').addEventListener('click', () => {
            this.soundManager.playSound('start');
            this.showHighScores();
        });
        
        document.getElementById('about-btn').addEventListener('click', () => {
            this.soundManager.playSound('start');
            alert('Pacman - классическая аркадная игра 1980 года.\n\nУправление:\n- Стрелки или WASD для движения\n\nЦель:\n- Соберите всю еду\n- Избегайте привидений\n- Используйте супер-еду для временного преимущества\n\nОсобенности:\n- Система комбо\n- Увеличивающаяся сложность\n- Рекорды\n- Настройки игры');
        });
        
        // Добавляем обработчики для кнопок возврата
        document.getElementById('back-from-scores-btn').addEventListener('click', () => {
            this.soundManager.playSound('start');
            this.hideHighScores();
        });
        
        document.getElementById('back-from-settings-btn').addEventListener('click', () => {
            this.soundManager.playSound('start');
            this.hideSettings();
        });
        
        // Добавляем обработчик для кнопки возврата из выбора уровней
        document.getElementById('back-from-levels-btn').addEventListener('click', () => {
            this.soundManager.playSound('start');
            this.hideLevelSelect();
        });
        
        document.getElementById('save-settings-btn').addEventListener('click', () => {
            this.soundManager.playSound('start');
            this.applySettings();
        });
        
        // Обработчики для кнопок игрового экрана
        document.getElementById('start-btn').addEventListener('click', () => {
            this.soundManager.playSound('start');
            this.start();
        });
        
        document.getElementById('pause-btn').addEventListener('click', () => {
            this.soundManager.playSound('start');
            this.pause();
        });
        
        document.getElementById('reset-btn').addEventListener('click', () => {
            this.soundManager.playSound('start');
            this.reset();
        });
        
        document.getElementById('menu-btn').addEventListener('click', () => {
            this.soundManager.playSound('start');
            this.showMenu();
        });
        
        document.getElementById('message-btn').addEventListener('click', () => {
            document.getElementById('message').style.display = 'none';
            this.showMenu();
        });
        
        // Управление клавишами
        document.addEventListener('keydown', (e) => {
            console.log("Нажата клавиша:", e.key);
            this.handleKey(e);
        });
        
        // Событие слайдера для настроек
        document.getElementById('game-speed').addEventListener('input', (e) => {
            document.getElementById('speed-value').textContent = e.target.value + ' мс';
        });
        
        console.log("Обработчики событий установлены");
    }
    
    // Метод для обработки нажатий клавиш
    handleKey(e) {
        // Всегда разрешаем управление, даже если игра на паузе
        switch(e.key) {
            case 'ArrowUp':
            case 'w':
            case 'W':
                this.pacman.setNextDirection('up');
                e.preventDefault();
                break;
            case 'ArrowDown':
            case 's':
            case 'S':
                this.pacman.setNextDirection('down');
                e.preventDefault();
                break;
            case 'ArrowLeft':
            case 'a':
            case 'A':
                this.pacman.setNextDirection('left');
                e.preventDefault();
                break;
            case 'ArrowRight':
            case 'd':
            case 'D':
                this.pacman.setNextDirection('right');
                e.preventDefault();
                break;
        }
    }
    
    // Метод для паузы игры
    pause() {
        console.log("Пауза игры");
        this.isRunning = false;
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }
        
        // Пауза фоновой музыки
        this.soundManager.pauseBackgroundMusic();
    }
    
    // Основной игровой цикл
    gameLoop(timestamp) {
        if (!this.isRunning) return;
        
        // Вычисляем deltaTime для плавного движения
        const deltaTime = timestamp - this.lastTimestamp;
        this.lastTimestamp = timestamp;
        
        // Обновляем игру с заданным интервалом
        if (timestamp - this.lastUpdate >= this.updateInterval) {
            this.update(deltaTime);
            this.lastUpdate = timestamp;
        }
        
        // Отрисовываем
        this.draw();
        
        // Обновляем частицы
        this.particleManager.updateParticles();
        
        // Продолжаем цикл
        this.animationFrameId = requestAnimationFrame((timestamp) => this.gameLoop(timestamp));
    }
    
    // Метод для обновления игрового состояния
    update(deltaTime) {
        // Обновляем движение Пакмана
        this.pacman.move(this.gameMap.getLevelMap(this.level), this.cellSize);
        
        // Обновляем движение привидений
        this.ghosts.forEach(ghost => {
            ghost.move(this.pacman.x, this.pacman.y, this.gameMap.getLevelMap(this.level), this.pacman.powerMode, this.cellSize);
        });
        
        // Проверяем столкновения
        this.checkCollisions();
        
        // Анимируем рот Пакмана
        this.pacman.animateMouth();
        
        // Update power mode timer
        this.pacman.updatePowerMode(deltaTime);
        if (!this.pacman.powerMode) {
            this.canvas.classList.remove('power-mode');
        } else {
            this.canvas.classList.add('power-mode');
        }
        
        // Update combo display timer
        if (this.comboDisplay && Date.now() - this.comboDisplay.startTime > 2000) {
            this.comboDisplay = null;
        }
        
        // Update fruit system
        this.fruitManager.spawnFruit(
            this.gameMap.getLevelMap(this.level),
            this.foodCount,
            this.totalFood,
            this.level
        );
        this.checkFruitCollection();
        
        // Check achievements
        this.achievementManager.checkAchievements(this.score, this.level, this.consecutiveEats);
    }
    
    // Метод для создания комбо
    createCombo() {
        const now = Date.now();
        if (now - this.lastEatTime < 2000) { // 2 секунды для комбо
            this.consecutiveEats++;
            if (this.consecutiveEats >= 3) {
                this.comboBonus = this.consecutiveEats * 10;
                this.score += this.comboBonus;
                this.soundManager.playSound('combo');
                this.showCombo(this.comboBonus);
                this.particleManager.createParticles(this.pacman.x, this.pacman.y, '#FF00FF');
            }
        } else {
            this.consecutiveEats = 1;
        }
        this.lastEatTime = now;
    }
    
    // Метод для отображения комбо
    showCombo(bonus) {
        this.comboDisplay = {
            text: `КОМБО +${bonus}`,
            x: this.pacman.x * this.cellSize + this.cellSize/2,
            y: this.pacman.y * this.cellSize,
            startTime: Date.now()
        };
    }
    
    // Метод для проверки сбора фруктов
    checkFruitCollection() {
        const points = this.fruitManager.checkFruitCollection(
            this.pacman.x, 
            this.pacman.y,
            (points) => {
                this.score += points;
                this.achievementManager.incrementFruitsCollected();
                this.soundManager.playSound('fruit');
                this.updateScore();
            },
            (x, y, color) => {
                this.particleManager.createParticles(x, y, color);
            }
        );
        
        if (points > 0) {
            this.score += points;
            this.achievementManager.incrementFruitsCollected();
            this.soundManager.playSound('fruit');
            this.updateScore();
        }
    }
    
    // Метод для увеличения сложности
    increaseDifficulty() {
        // Увеличиваем скорость привидений с каждым уровнем
        this.ghosts.forEach(ghost => {
            ghost.increaseSpeed(0.05);
        });
        
        // Уменьшаем интервал обновления для более быстрой игры
        this.updateInterval = Math.max(50, this.updateInterval - 5);
    }
    
    // Метод для обновления счета
    updateScore() {
        document.getElementById('score').textContent = this.score;
    }
    
    // Метод для обновления уровня
    updateLevel() {
        document.getElementById('level').textContent = this.level;
    }
    
    // Метод для обновления жизней
    updateLives() {
        document.getElementById('lives').innerHTML = '❤️'.repeat(this.lives);
    }
    
    // Метод для отображения сообщений
    showMessage(text) {
        document.getElementById('message-title').textContent = 'Игра окончена';
        document.getElementById('message-text').innerHTML = text;
        document.getElementById('message').style.display = 'block';
    }
    
    // Система рекордов
    loadHighScores() {
        try {
            const scores = localStorage.getItem('pacmanHighScores');
            return scores ? JSON.parse(scores) : [];
        } catch (e) {
            console.error('Ошибка загрузки рекордов:', e);
            return [];
        }
    }
    
    saveHighScore() {
        try {
            const name = prompt('Поздравляем! Вы набрали ' + this.score + ' очков. Введите ваше имя:', 'Игрок') || 'Аноним';
            const newScore = { name, score: this.score, date: new Date().toLocaleDateString() };
            
            this.highScores.push(newScore);
            this.highScores.sort((a, b) => b.score - a.score);
            this.highScores = this.highScores.slice(0, 10); // Сохраняем только топ-10
            
            localStorage.setItem('pacmanHighScores', JSON.stringify(this.highScores));
            console.log('Рекорд сохранен:', newScore);
        } catch (e) {
            console.error('Ошибка сохранения рекорда:', e);
        }
    }
    
    showHighScores() {
        document.getElementById('main-menu').classList.add('hidden');
        document.getElementById('highscores-screen').classList.remove('hidden');
        
        const scoresList = document.getElementById('scores-list');
        scoresList.innerHTML = '';
        
        if (this.highScores.length === 0) {
            scoresList.innerHTML = '<div class="score-entry"><span>Нет рекордов</span></div>';
            return;
        }
        
        this.highScores.forEach((score, index) => {
            const entry = document.createElement('div');
            entry.className = 'score-entry';
            entry.innerHTML = `
                <span class="score-rank">#${index + 1}</span>
                <span class="score-name">${score.name}</span>
                <span class="score-value">${score.score}</span>
            `;
            scoresList.appendChild(entry);
        });
    }
    
    hideHighScores() {
        document.getElementById('highscores-screen').classList.add('hidden');
        document.getElementById('main-menu').classList.remove('hidden');
    }
    
    // Система настроек
    loadSettings() {
        try {
            const settings = localStorage.getItem('pacmanSettings');
            return settings ? JSON.parse(settings) : {
                difficulty: 'normal',
                gameSpeed: 150,
                soundEnabled: true,
                musicEnabled: true,
                animationsEnabled: true
            };
        } catch (e) {
            console.error('Ошибка загрузки настроек:', e);
            return {
                difficulty: 'normal',
                gameSpeed: 150,
                soundEnabled: true,
                musicEnabled: true,
                animationsEnabled: true
            };
        }
    }
    
    applySettings() {
        const settings = {
            difficulty: document.getElementById('difficulty').value,
            gameSpeed: parseInt(document.getElementById('game-speed').value),
            soundEnabled: document.getElementById('sound-enabled').checked,
            musicEnabled: document.getElementById('music-enabled').checked,
            animationsEnabled: document.getElementById('animations-enabled').checked
        };
        
        this.settings = settings;
        
        try {
            localStorage.setItem('pacmanSettings', JSON.stringify(settings));
            console.log('Настройки сохранены:', settings);
            
            // Применяем настройки
            this.updateInterval = settings.gameSpeed;
            
            // Если игра запущена и музыка включена, запускаем её
            if (this.isRunning && settings.musicEnabled) {
                this.soundManager.playBackgroundMusic();
            } else if (!settings.musicEnabled) {
                this.soundManager.pauseBackgroundMusic();
            }
        } catch (e) {
            console.error('Ошибка сохранения настроек:', e);
        }
        
        this.hideSettings();
    }
    
    showSettings() {
        document.getElementById('main-menu').classList.add('hidden');
        document.getElementById('settings-screen').classList.remove('hidden');
        
        // Заполняем поля текущими значениями
        document.getElementById('difficulty').value = this.settings.difficulty;
        document.getElementById('game-speed').value = this.settings.gameSpeed;
        document.getElementById('speed-value').textContent = this.settings.gameSpeed + ' мс';
        document.getElementById('sound-enabled').checked = this.settings.soundEnabled;
        document.getElementById('music-enabled').checked = this.settings.musicEnabled;
        document.getElementById('animations-enabled').checked = this.settings.animationsEnabled;
    }
    
    hideSettings() {
        document.getElementById('settings-screen').classList.add('hidden');
        document.getElementById('main-menu').classList.remove('hidden');
    }
    
    hideMenu() {
        document.getElementById('main-menu').classList.add('hidden');
        document.getElementById('game-screen').classList.remove('hidden');
    }
    
    // Добавляем методы для работы с выбором уровней
    showLevelSelect() {
        document.getElementById('main-menu').classList.add('hidden');
        document.getElementById('level-select-screen').classList.remove('hidden');
        
        // Генерируем кнопки уровней
        this.generateLevelButtons();
    }
    
    hideLevelSelect() {
        document.getElementById('level-select-screen').classList.add('hidden');
        document.getElementById('main-menu').classList.remove('hidden');
    }
    
    generateLevelButtons() {
        const levelGrid = document.getElementById('level-grid');
        levelGrid.innerHTML = '';
        
        // Создаем кнопки для 10 уровней - все уровни открыты
        for (let i = 1; i <= 10; i++) {
            const button = document.createElement('button');
            button.className = 'level-btn';
            button.textContent = `Уровень ${i}`;
            
            // Все уровни доступны без ограничений
            button.addEventListener('click', () => {
                this.soundManager.playSound('start');
                this.selectLevel(i);
            });
            
            levelGrid.appendChild(button);
        }
    }
    
    selectLevel(level) {
        this.selectedLevel = level;
        this.level = level;
        
        // Сбрасываем игру
        this.reset();
        
        // Скрываем выбор уровней и показываем игру
        this.hideLevelSelect();
        this.hideMenu();
        this.start();
    }
    
    // Метод для разблокировки следующего уровня (устарел, все уровни открыты)
    /*
    unlockNextLevel() {
        try {
            let unlockedLevels = 1;
            const saved = localStorage.getItem('pacmanUnlockedLevels');
            if (saved) {
                unlockedLevels = Math.min(10, Math.max(1, parseInt(saved)));
            }
            
            if (this.level >= unlockedLevels && this.level < 10) {
                unlockedLevels = this.level + 1;
                localStorage.setItem('pacmanUnlockedLevels', unlockedLevels.toString());
            }
        } catch (e) {
            console.warn('Ошибка сохранения разблокированных уровней:', e);
        }
    }
    */
    
    // Метод для возврата в главное меню во время игры
    showMenu() {
        // Останавливаем игру
        this.isRunning = false;
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }
        
        // Пауза музыки
        this.soundManager.pauseBackgroundMusic();
        
        // Скрываем игровой экран и показываем меню
        document.getElementById('game-screen').classList.add('hidden');
        document.getElementById('main-menu').classList.remove('hidden');
    }
}

// Инициализировать игру при загрузке страницы
let game;
window.addEventListener('load', () => {
    game = new PacmanGame();
    console.log("Игра загружена");
});