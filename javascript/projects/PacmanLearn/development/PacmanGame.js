// Импортируем необходимые классы
import { Pacman } from './Pacman.js';
import { Ghost } from './Ghost.js';
import { GameMap } from './GameMap.js';
import { SoundManager } from './SoundManager.js';
import { ParticleManager } from './ParticleManager.js';
import { FruitManager } from './FruitManager.js';
import { AchievementManager } from './AchievementManager.js';
import { PowerUpManager } from './PowerUpManager.js';
import { Utils } from './Utils.js';
import { GAME_SETTINGS, UI_CONSTANTS, CELL_TYPES } from './Constants.js';

class PacmanGame {
    constructor() {
        // Инициализация холста
        this.canvas = document.getElementById('game-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.cellSize = GAME_SETTINGS.DEFAULT_CELL_SIZE;
        
        // Игровые параметры
        this.isRunning = false;
        this.animationFrameId = null;
        this.lastTimestamp = 0;
        this.updateInterval = GAME_SETTINGS.DEFAULT_UPDATE_INTERVAL; // Интервал обновления в миллисекундах (замедляет игру)
        this.lastUpdate = 0;
        
        // Performance optimization settings
        this.targetFPS = 60;
        this.frameTime = 1000 / this.targetFPS;
        this.lastFrameTime = 0;
        this.fps = 0;
        this.frameCount = 0;
        this.lastFpsUpdate = 0;
        
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
        this.powerUpManager = new PowerUpManager(); // Новый менеджер power-up'ов
        
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
        
        // Pre-allocate objects for performance
        this.tempComboDisplay = {
            text: '',
            x: 0,
            y: 0,
            startTime: 0
        };
        
        // Performance monitoring
        this.performanceStats = {
            updateDuration: 0,
            drawDuration: 0,
            particleCount: 0
        };
        
        // Throttled functions for performance
        this.throttledDraw = Utils.throttle(() => this.draw(), 16); // ~60 FPS
        
        // First-time setup
        this.setupCanvas();
        
        // Первичная отрисовка
        this.draw();
        
        console.log("Игра инициализирована");
    }
    
    // Setup canvas for optimal performance
    setupCanvas() {
        // Enable image smoothing for better visuals
        this.ctx.imageSmoothingEnabled = true;
        this.ctx.imageSmoothingQuality = 'high';
        
        // Set canvas resolution to match display
        const dpr = window.devicePixelRatio || 1;
        this.canvas.width = this.canvas.clientWidth * dpr;
        this.canvas.height = this.canvas.clientHeight * dpr;
        this.ctx.scale(dpr, dpr);
    }
    
    // Метод для подсчета еды на карте
    countFood() {
        this.totalFood = this.gameMap.countFood(this.gameMap.getCurrentMap());
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
        this.powerUpManager.reset(); // Сброс power-up менеджера
        
        // Сброс системы уровней
        this.gameMap.reset();
        
        // Сброс времени начала уровня для достижения "Скоростной демон"
        this.achievementManager.setLevelStartTime();
        this.achievementManager.currentLevelStartLives = 3; // Reset lives tracking
        
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
        this.powerUpManager.reset(); // Сброс power-up менеджера
    }
    
    // Метод для сброса карты
    resetMap() {
        console.log("Сброс карты");
        const currentMap = this.gameMap.getCurrentMap();
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
            
            // Play background music
            this.soundManager.playBackgroundMusic();
            
            this.gameLoop();
        }
    }
    
    // Метод для перехода на следующий уровень
    nextLevel() {
        console.log("Переход на следующий уровень");
        
        // Проверяем, есть ли следующий уровень в системе уровней
        if (this.gameMap.nextLevel()) {
            this.level = this.gameMap.currentLevel + 1; // Обновляем уровень игры
            this.foodCount = 0;
            
            // Сброс позиций
            this.pacman.resetPosition();
            this.ghosts.forEach(ghost => ghost.resetPosition());
            
            // Сброс менеджеров
            this.particleManager.clearParticles();
            this.fruitManager.reset();
            this.powerUpManager.reset(); // Сброс power-up менеджера
            
            // Подсчет еды на новом уровне
            this.countFood();
            
            // Set the level start time for achievement tracking
            this.achievementManager.setLevelStartTime();
            this.achievementManager.currentLevelStartLives = this.lives; // Track lives for this level
            
            // Увеличение сложности
            this.increaseDifficulty();
            
            this.updateLevel();
            this.draw();
        } else {
            // Если уровней больше нет, показываем сообщение о завершении игры
            this.isRunning = false;
            if (this.animationFrameId) {
                cancelAnimationFrame(this.animationFrameId);
                this.animationFrameId = null;
            }
            
            // Создаем эффект окончания игры
            this.particleManager.createGameOverEffect(this.canvas.width, this.canvas.height);
            
            // Воспроизводим звук окончания игры
            this.soundManager.playSound('gameOver');
            
            // Проверяем и сохраняем рекорд
            this.saveHighScore(this.score);
            
            // Показываем сообщение окончания игры
            document.getElementById('message-title').textContent = 'Поздравляем!';
            document.getElementById('message-text').textContent = `Вы прошли все уровни! Ваш счет: ${this.score}`;
            document.getElementById('message').style.display = 'block';
        }
    }
    
    // Метод для проверки завершения уровня
    checkLevelComplete() {
        if (this.foodCount >= this.totalFood) {
            console.log("Уровень завершен");
            this.soundManager.playSound('levelComplete');
            
            // Бонус за завершение уровня
            const levelBonus = 1000 * this.level;
            this.score += levelBonus;
            
            // Бонус за быстрое прохождение
            const timeBonus = this.achievementManager.calculateTimeBonus();
            this.score += timeBonus;
            
            // Проверка достижения за быстрое прохождение
            if (timeBonus > 0) {
                this.achievementManager.unlockAchievement('speed_demon');
            }
            
            this.updateScore();
            
            // Создаем визуальный эффект при завершении уровня
            this.particleManager.createLevelCompleteEffect(this.canvas.width/2, this.canvas.height/2);
            
            // Небольшая задержка перед переходом на следующий уровень
            setTimeout(() => {
                this.nextLevel();
            }, 1500);
        }
    }
    
    // Метод для увеличения сложности
    increaseDifficulty() {
        // Увеличиваем скорость призраков с каждым уровнем
        this.ghosts.forEach(ghost => {
            ghost.increaseSpeed(0.05);
        });
        
        // Уменьшаем интервал обновления для более быстрой игры (до минимума)
        this.updateInterval = Math.max(GAME_SETTINGS.MIN_UPDATE_INTERVAL, this.updateInterval - 5);
    }
    
    // Основной игровой цикл
    gameLoop(timestamp) {
        if (!this.isRunning) return;
        
        // Calculate delta time for smooth animation
        const deltaTime = timestamp - this.lastTimestamp;
        this.lastTimestamp = timestamp;
        
        // Calculate FPS
        this.frameCount++;
        if (timestamp - this.lastFpsUpdate >= 1000) {
            this.fps = this.frameCount;
            this.frameCount = 0;
            this.lastFpsUpdate = timestamp;
        }
        
        // Update game state at fixed intervals
        const currentTime = performance.now();
        const updateDelta = currentTime - this.lastUpdate;
        
        // Update game logic at consistent rate
        if (updateDelta >= this.updateInterval) {
            const updateStart = performance.now();
            this.update(updateDelta);
            this.performanceStats.updateDuration = performance.now() - updateStart;
            this.lastUpdate = currentTime;
        }
        
        // Draw at variable rate but throttled
        const drawStart = performance.now();
        this.throttledDraw();
        this.performanceStats.drawDuration = performance.now() - drawStart;
        
        // Continue the game loop
        this.animationFrameId = requestAnimationFrame((timestamp) => this.gameLoop(timestamp));
    }
    
    // Метод для обновления состояния игры
    update(deltaTime) {
        // Получаем текущую карту уровня
        const currentMap = this.gameMap.getCurrentMap();
        
        // Store previous tunnel state
        const wasInTunnel = this.pacman.isInTunnelTransition();
        
        // Обновляем Пакмана
        this.pacman.move(currentMap, this.cellSize);
        this.pacman.animateMouth();
        this.pacman.updatePowerMode(deltaTime);
        
        // Check if Pacman just completed a tunnel transition
        if (wasInTunnel && !this.pacman.isInTunnelTransition()) {
            this.achievementManager.incrementTunnelTransitions();
        }
        
        // Обновляем призраков
        this.ghosts.forEach(ghost => {
            ghost.move(this.pacman.x, this.pacman.y, currentMap, this.pacman.powerMode, this.cellSize);
        });
        
        // Обновляем power-up менеджер
        this.powerUpManager.update();
        
        // Спавним power-up
        this.powerUpManager.spawnPowerUp(currentMap);
        
        // Проверяем сбор еды
        this.checkFoodCollection(currentMap);
        
        // Проверяем сбор фруктов
        this.fruitManager.update(this.pacman.x, this.pacman.y, currentMap, this.cellSize);
        this.checkFruitCollection();
        
        // Проверяем сбор power-up'ов
        this.checkPowerUpCollection();
        
        // Проверяем столкновения с призраками
        this.checkGhostCollisions();
        
        // Проверяем завершение уровня
        this.checkLevelComplete();
        
        // Обновляем менеджеры
        this.particleManager.update();
        this.achievementManager.update(this.score, this.level, this.lives);
    }

    // Метод для проверки сбора еды
    checkFoodCollection(currentMap) {
        const cell = currentMap[this.pacman.y][this.pacman.x];
        
        if (cell === CELL_TYPES.FOOD) {
            // Собираем обычную еду
            currentMap[this.pacman.y][this.pacman.x] = CELL_TYPES.PATH;
            this.foodCount++;
            this.score += 10 * this.powerUpManager.getPointsMultiplier(); // Применяем множитель очков
            
            // Создаем частицы при сборе еды
            this.particleManager.createFoodParticles(
                this.pacman.x * this.cellSize + this.cellSize/2,
                this.pacman.y * this.cellSize + this.cellSize/2,
                false
            );
            
            // Воспроизводим звук
            this.soundManager.playSound('eat');
            
            // Проверяем комбо
            this.checkCombo();
            
            // Обновляем счет и проверяем достижения
            this.updateScore();
            this.achievementManager.checkFoodAchievements(this.foodCount, this.totalFood);
        } 
        else if (cell === CELL_TYPES.SUPER_FOOD) {
            // Собираем супер-еду
            currentMap[this.pacman.y][this.pacman.x] = CELL_TYPES.PATH;
            this.foodCount++;
            this.score += 50 * this.powerUpManager.getPointsMultiplier(); // Применяем множитель очков
            
            // Активируем режим силы
            this.pacman.activatePowerMode();
            
            // Создаем частицы при сборе супер-еды
            this.particleManager.createFoodParticles(
                this.pacman.x * this.cellSize + this.cellSize/2,
                this.pacman.y * this.cellSize + this.cellSize/2,
                true
            );
            
            // Создаем дополнительный эффект для супер-еды
            this.particleManager.createSuperFoodEffect(
                this.pacman.x * this.cellSize + this.cellSize/2,
                this.pacman.y * this.cellSize + this.cellSize/2
            );
            
            // Воспроизводим звук
            this.soundManager.playSound('power');
            
            // Проверяем комбо
            this.checkCombo();
            
            // Обновляем счет и проверяем достижения
            this.updateScore();
            this.achievementManager.checkFoodAchievements(this.foodCount, this.totalFood);
        }
    }
    
    // Метод для проверки комбо
    checkCombo() {
        const now = Date.now();
        if (now - this.lastEatTime < GAME_SETTINGS.COMBO_TIME_WINDOW) {
            this.consecutiveEats++;
            if (this.consecutiveEats >= GAME_SETTINGS.COMBO_MIN_COUNT) {
                this.comboBonus = this.consecutiveEats * 10 * this.powerUpManager.getPointsMultiplier(); // Применяем множитель очков
                this.score += this.comboBonus;
                
                // Создаем эффект комбо
                this.comboDisplay = {
                    text: `КОМБО x${this.consecutiveEats}! +${this.comboBonus}`,
                    x: this.pacman.x * this.cellSize + this.cellSize/2,
                    y: this.pacman.y * this.cellSize,
                    startTime: now
                };
                
                // Создаем частицы комбо
                this.particleManager.createComboEffect(
                    this.pacman.x * this.cellSize + this.cellSize/2,
                    this.pacman.y * this.cellSize + this.cellSize/2,
                    this.consecutiveEats
                );
                
                // Воспроизводим звук комбо
                this.soundManager.playSound('combo');
            }
        } else {
            this.consecutiveEats = 1;
        }
        this.lastEatTime = now;
    }
    
    // Метод для проверки сбора фруктов
    checkFruitCollection() {
        if (this.fruitManager.currentFruit && 
            this.pacman.x === this.fruitManager.currentFruit.x && 
            this.pacman.y === this.fruitManager.currentFruit.y) {
            
            const points = this.fruitManager.currentFruit.points * this.powerUpManager.getPointsMultiplier(); // Применяем множитель очков
            this.score += points;
            this.fruitManager.collectFruit();
            
            // Создаем эффект сбора фрукта
            this.particleManager.createFruitCollectedEffect(
                this.fruitManager.currentFruit.x * this.cellSize + this.cellSize/2,
                this.fruitManager.currentFruit.y * this.cellSize + this.cellSize/2,
                points
            );
            
            // Воспроизводим звук
            this.soundManager.playSound('fruit');
            
            // Обновляем счет и проверяем достижения
            this.updateScore();
            this.achievementManager.checkFruitAchievements();
        }
    }
    
    // Метод для проверки сбора power-up'ов
    checkPowerUpCollection() {
        if (this.powerUpManager.checkPowerUpCollection(
            this.pacman.x, 
            this.pacman.y, 
            this.pacman, 
            this
        )) {
            // Воспроизводим звук сбора power-up
            this.soundManager.playSound('powerUp');
            
            // Создаем визуальный эффект сбора power-up
            this.particleManager.createPowerUpEffect(
                this.pacman.x * this.cellSize + this.cellSize/2,
                this.pacman.y * this.cellSize + this.cellSize/2,
                this.powerUpManager.getLastCollectedPowerUpType()
            );
            
            // Track achievement criteria
            this.achievementManager.incrementPowerUpsCollected();
            
            // Track specific power-up types for achievements
            const powerUpType = this.powerUpManager.getLastCollectedPowerUpType();
            switch(powerUpType) {
                case 'invincibility':
                    this.achievementManager.incrementInvincibilityUsed();
                    break;
                case 'freeze_ghosts':
                    this.achievementManager.incrementFreezeUsed();
                    break;
                case 'extra_life':
                    this.achievementManager.incrementExtraLivesGained();
                    break;
                case 'points_multiplier':
                    this.achievementManager.incrementMultiplierUsed();
                    break;
            }
            
            // Обновляем счет
            this.updateScore();
        }
    }
    
    // Метод для проверки столкновений с призраками
    checkGhostCollisions() {
        for (let ghost of this.ghosts) {
            // Используем улучшенное обнаружение столкновений
            if (this.pacman.checkCollision(ghost.x, ghost.y, ghost.collisionRadius)) {
                if (this.pacman.powerMode) {
                    // Пакман съедает призрака
                    this.score += 200 * this.powerUpManager.getPointsMultiplier(); // Применяем множитель очков
                    this.ghostsEaten = (this.ghostsEaten || 0) + 1;
                    
                    // Создаем эффект поедания призрака
                    this.particleManager.createGhostEatenEffect(
                        ghost.x * this.cellSize + this.cellSize/2,
                        ghost.y * this.cellSize + this.cellSize/2,
                        ghost.color
                    );
                    
                    // Воспроизводим звук
                    this.soundManager.playSound('ghost');
                    
                    // Возвращаем призрака на начальную позицию
                    ghost.resetPosition();
                    
                    // Обновляем счет и проверяем достижения
                    this.updateScore();
                    this.achievementManager.checkGhostAchievements(this.ghostsEaten);
                } else {
                    // Призрак съедает Пакмана
                    this.lives--;
                    this.updateLives();
                    
                    // Создаем эффект смерти Пакмана
                    this.particleManager.createPacmanDeathEffect(
                        this.pacman.x * this.cellSize + this.cellSize/2,
                        this.pacman.y * this.cellSize + this.cellSize/2
                    );
                    
                    // Воспроизводим звук
                    this.soundManager.playSound('death');
                    
                    if (this.lives <= 0) {
                        this.gameOver();
                    } else {
                        // Возвращаем Пакмана и призраков на начальные позиции
                        this.resetPositions();
                    }
                    break; // Прерываем проверку после столкновения
                }
            }
        }
    }
    
    // Метод для окончания игры
    gameOver() {
        console.log("Игра окончена");
        this.isRunning = false;
        
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }
        
        // Создаем эффект окончания игры
        this.particleManager.createGameOverEffect(this.canvas.width, this.canvas.height);
        
        // Воспроизводим звук окончания игры
        this.soundManager.playSound('gameOver');
        
        // Проверяем и сохраняем рекорд
        this.saveHighScore(this.score);
        
        // Показываем сообщение окончания игры
        document.getElementById('message-title').textContent = 'Игра окончена';
        document.getElementById('message-text').textContent = `Ваш счет: ${this.score}`;
        document.getElementById('message').style.display = 'block';
    }
    
    // Метод для отрисовки игры
    draw() {
        // Only draw if animations are enabled
        if (this.settings.animationsEnabled === false) {
            return;
        }
        
        // Очистка холста с оптимизацией
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Получаем текущую карту уровня
        const currentMap = this.gameMap.getCurrentMap();
        
        // Отрисовка карты
        this.drawMap(currentMap);
        
        // Отрисовка фруктов
        this.fruitManager.draw(this.ctx, this.cellSize);
        
        // Отрисовка power-up'ов
        this.powerUpManager.draw(this.ctx, this.cellSize);
        
        // Отрисовка Пакмана
        this.drawPacman();
        
        // Отрисовка призраков
        this.drawGhosts();
        
        // Отрисовка частиц только если есть активные частицы
        this.performanceStats.particleCount = this.particleManager.getActiveParticleCount();
        if (this.performanceStats.particleCount > 0) {
            this.particleManager.draw(this.ctx);
        }
        
        // Отрисовка комбо
        this.drawCombo();
        
        // Draw tunnel transition effects
        this.drawTunnelEffects();
        
        // Draw performance stats if enabled (for debugging)
        if (this.settings.showPerformanceStats) {
            this.drawPerformanceStats();
        }
    }
    
    // Метод для отрисовки эффектов туннеля
    drawTunnelEffects() {
        // Left tunnel entrance
        const leftTunnelX = 0;
        const rightTunnelX = this.gameMap.getCurrentMap()[0].length - 1;
        
        for (let y = 0; y < this.gameMap.getCurrentMap().length; y++) {
            // Check if this is a valid tunnel position (path)
            if (this.gameMap.getCurrentMap()[y][leftTunnelX] === CELL_TYPES.PATH) {
                // Draw subtle glow effect at tunnel entrances
                this.ctx.save();
                this.ctx.globalAlpha = 0.3;
                this.ctx.shadowColor = '#8080FF';
                this.ctx.shadowBlur = 10;
                
                // Left tunnel entrance
                this.ctx.fillStyle = '#8080FF';
                this.ctx.beginPath();
                this.ctx.arc(
                    leftTunnelX * this.cellSize + this.cellSize/2,
                    y * this.cellSize + this.cellSize/2,
                    this.cellSize/4,
                    0,
                    Math.PI * 2
                );
                this.ctx.fill();
                
                // Right tunnel entrance
                this.ctx.beginPath();
                this.ctx.arc(
                    rightTunnelX * this.cellSize + this.cellSize/2,
                    y * this.cellSize + this.cellSize/2,
                    this.cellSize/4,
                    0,
                    Math.PI * 2
                );
                this.ctx.fill();
                
                this.ctx.restore();
            }
        }
    }
    
    // Метод для отрисовки карты с оптимизацией
    drawMap(map) {
        // Use a more efficient drawing method
        for (let y = 0; y < map.length; y++) {
            for (let x = 0; x < map[y].length; x++) {
                const cell = map[y][x];
                const pixelX = x * this.cellSize;
                const pixelY = y * this.cellSize;
                
                switch(cell) {
                    case CELL_TYPES.WALL: // Стена
                        this.ctx.fillStyle = '#2222FF';
                        this.ctx.fillRect(pixelX, pixelY, this.cellSize, this.cellSize);
                        // Добавляем детали стен с оптимизацией
                        this.ctx.fillStyle = '#0000CC';
                        this.ctx.fillRect(pixelX + 2, pixelY + 2, this.cellSize - 4, this.cellSize - 4);
                        break;
                    case CELL_TYPES.PATH: // Путь
                        this.ctx.fillStyle = '#000';
                        this.ctx.fillRect(pixelX, pixelY, this.cellSize, this.cellSize);
                        break;
                    case CELL_TYPES.FOOD: // Еда
                        this.ctx.fillStyle = '#FFF';
                        this.ctx.beginPath();
                        this.ctx.arc(pixelX + this.cellSize/2, pixelY + this.cellSize/2, 3, 0, Math.PI * 2);
                        this.ctx.fill();
                        break;
                    case CELL_TYPES.SUPER_FOOD: // Супер-еда
                        this.ctx.fillStyle = '#FFF';
                        this.ctx.beginPath();
                        this.ctx.arc(pixelX + this.cellSize/2, pixelY + this.cellSize/2, 6, 0, Math.PI * 2);
                        this.ctx.fill();
                        break;
                }
            }
        }
    }
    
    // Метод для отрисовки Пакмана с оптимизацией
    drawPacman() {
        const pixelX = this.pacman.pixelX;
        const pixelY = this.pacman.pixelY;
        const radius = this.cellSize/2 - 2;
        
        this.ctx.fillStyle = '#FFD700'; // Золотой цвет
        this.ctx.beginPath();
        
        let startAngle, endAngle;
        switch(this.pacman.direction) {
            case DIRECTIONS.RIGHT:
                startAngle = this.pacman.mouthAngle * Math.PI;
                endAngle = (2 - this.pacman.mouthAngle) * Math.PI;
                break;
            case DIRECTIONS.DOWN:
                startAngle = (0.5 + this.pacman.mouthAngle) * Math.PI;
                endAngle = (2.5 - this.pacman.mouthAngle) * Math.PI;
                break;
            case DIRECTIONS.LEFT:
                startAngle = (1 + this.pacman.mouthAngle) * Math.PI;
                endAngle = (3 - this.pacman.mouthAngle) * Math.PI;
                break;
            case DIRECTIONS.UP:
                startAngle = (1.5 + this.pacman.mouthAngle) * Math.PI;
                endAngle = (3.5 - this.pacman.mouthAngle) * Math.PI;
                break;
        }
        
        // Add glow effect when in power mode
        if (this.pacman.powerMode) {
            this.ctx.shadowColor = '#0000FF';
            this.ctx.shadowBlur = 15;
        }
        
        // Add pulsing effect when power mode is about to expire
        const powerModeEffect = this.pacman.getPowerModeEffect();
        if (powerModeEffect > 0) {
            this.ctx.shadowColor = '#FF0000';
            this.ctx.shadowBlur = 10 + powerModeEffect * 20;
        }
        
        this.ctx.arc(pixelX, pixelY, radius, startAngle, endAngle);
        this.ctx.lineTo(pixelX, pixelY);
        this.ctx.fill();
        
        // Reset shadow
        this.ctx.shadowBlur = 0;
        
        // Add tunnel transition effect
        if (this.pacman.isInTunnelTransition()) {
            const progress = this.pacman.getTunnelTransitionProgress();
            this.ctx.globalAlpha = 0.5 + Math.abs(Math.sin(progress * Math.PI)) * 0.5;
            this.ctx.strokeStyle = '#8080FF';
            this.ctx.lineWidth = 2;
            this.ctx.stroke();
            this.ctx.globalAlpha = 1.0;
        }
    }
    
    // Метод для отрисовки призраков с оптимизацией
    drawGhosts() {
        // Batch draw operations for better performance
        this.ctx.save();
        
        this.ghosts.forEach(ghost => {
            const pixelX = ghost.pixelX;
            const pixelY = ghost.pixelY;
            const radius = this.cellSize/2 - 2;
            
            // Get state effect
            const stateEffect = ghost.getStateEffect();
            const personalityEffect = ghost.getPersonalityEffect();
            
            // Determine color based on state
            let ghostColor = stateEffect.color;
            if (this.pacman.powerMode) {
                ghostColor = '#0000FF'; // Blue when Pacman is in power mode
            }
            
            // Apply personality effect
            if (personalityEffect.glow > 0) {
                ghostColor = personalityEffect.color;
            }
            
            // Тело призрака
            this.ctx.fillStyle = ghostColor;
            
            // Add glow effect
            let glowIntensity = stateEffect.glow;
            if (personalityEffect.glow > glowIntensity) {
                glowIntensity = personalityEffect.glow;
            }
            
            if (glowIntensity > 0) {
                this.ctx.shadowColor = ghostColor;
                this.ctx.shadowBlur = glowIntensity;
            }
            
            // Apply scaling effect
            this.ctx.save();
            this.ctx.translate(pixelX, pixelY);
            this.ctx.scale(stateEffect.scale, stateEffect.scale);
            
            this.ctx.beginPath();
            this.ctx.arc(0, -2, radius, Math.PI, 0, false); // Верхняя часть
            this.ctx.lineTo(radius, radius - 2);
            
            // Нижняя часть с волнами
            for (let i = 0; i < 3; i++) {
                this.ctx.lineTo(radius - (i * radius * 2/3), radius - 6);
                this.ctx.lineTo(radius - ((i + 0.5) * radius * 2/3), radius - 2);
            }
            
            this.ctx.lineTo(-radius, radius - 2);
            this.ctx.lineTo(-radius, -2);
            this.ctx.fill();
            
            this.ctx.restore();
            
            // Сбрасываем свечение
            this.ctx.shadowBlur = 0;
        });
        
        this.ctx.restore();
        
        // Draw eyes separately for better performance
        this.ctx.save();
        this.ctx.fillStyle = 'white';
        
        this.ghosts.forEach(ghost => {
            const pixelX = ghost.pixelX;
            const pixelY = ghost.pixelY;
            
            this.ctx.beginPath();
            this.ctx.arc(pixelX - 4, pixelY - 4, 3, 0, Math.PI * 2);
            this.ctx.arc(pixelX + 4, pixelY - 4, 3, 0, Math.PI * 2);
            this.ctx.fill();
            
            this.ctx.fillStyle = 'black';
            let eyeOffsetX = 0, eyeOffsetY = 0;
            switch(ghost.direction) {
                case DIRECTIONS.LEFT: eyeOffsetX = -1; break;
                case DIRECTIONS.RIGHT: eyeOffsetX = 1; break;
                case DIRECTIONS.UP: eyeOffsetY = -1; break;
                case DIRECTIONS.DOWN: eyeOffsetY = 1; break;
            }
            
            this.ctx.beginPath();
            this.ctx.arc(pixelX - 4 + eyeOffsetX, pixelY - 4 + eyeOffsetY, 1.5, 0, Math.PI * 2);
            this.ctx.arc(pixelX + 4 + eyeOffsetX, pixelY - 4 + eyeOffsetY, 1.5, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Reset fill style for next ghost
            this.ctx.fillStyle = 'white';
        });
        
        this.ctx.restore();
    }
    
    // Метод для отрисовки комбо
    drawCombo() {
        if (this.comboDisplay && this.settings.animationsEnabled !== false) {
            const elapsed = Date.now() - this.comboDisplay.startTime;
            if (elapsed < 2000) { // Показываем комбо 2 секунды
                const alpha = 1 - elapsed / 2000;
                const scale = 1 + Math.sin(elapsed / 200) * 0.2; // Пульсация
                
                this.ctx.globalAlpha = alpha;
                
                // Добавляем свечение
                this.ctx.shadowColor = '#FF00FF';
                this.ctx.shadowBlur = 10;
                
                this.ctx.fillStyle = '#FF00FF';
                this.ctx.font = `bold ${20 * scale}px Arial`;
                this.ctx.textAlign = 'center';
                this.ctx.fillText(this.comboDisplay.text, this.comboDisplay.x, this.comboDisplay.y);
                
                // Сбрасываем свечение
                this.ctx.shadowBlur = 0;
                this.ctx.globalAlpha = 1;
                this.ctx.textAlign = 'left';
            } else {
                this.comboDisplay = null;
            }
        }
    }
    
    // Метод для отрисовки статистики производительности
    drawPerformanceStats() {
        this.ctx.save();
        this.ctx.fillStyle = '#00FF00';
        this.ctx.font = '12px Arial';
        this.ctx.textAlign = 'left';
        this.ctx.fillText(`FPS: ${this.fps}`, 10, 20);
        this.ctx.fillText(`Particles: ${this.performanceStats.particleCount}`, 10, 40);
        this.ctx.fillText(`Update: ${this.performanceStats.updateDuration.toFixed(2)}ms`, 10, 60);
        this.ctx.fillText(`Draw: ${this.performanceStats.drawDuration.toFixed(2)}ms`, 10, 80);
        this.ctx.restore();
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
    
    saveHighScore(score) {
        try {
            const name = prompt('Поздравляем! Вы набрали ' + score + ' очков. Введите ваше имя:', 'Игрок') || 'Аноним';
            const newScore = { name, score, date: new Date().toLocaleDateString() };
            
            this.highScores.push(newScore);
            this.highScores.sort((a, b) => b.score - a.score);
            this.highScores = this.highScores.slice(0, UI_CONSTANTS.MAX_HIGH_SCORES); // Сохраняем только топ-10
            
            // Создаем визуальный эффект при новом рекорде
            if (this.highScores[0].score === score) {
                this.particleManager.createNewHighScoreEffect(this.canvas.width/2, this.canvas.height/2);
            }
            
            localStorage.setItem('pacmanHighScores', JSON.stringify(this.highScores));
            console.log('Рекорд сохранен:', newScore);
        } catch (e) {
            console.error('Ошибка сохранения рекорда:', e);
        }
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
                animationsEnabled: true,
                volume: 1.0
            };
        } catch (e) {
            console.error('Ошибка загрузки настроек:', e);
            return {
                difficulty: 'normal',
                gameSpeed: 150,
                soundEnabled: true,
                musicEnabled: true,
                animationsEnabled: true,
                volume: 1.0
            };
        }
    }
    
    // Инициализация событий
    setupEventListeners() {
        // Управление клавишами
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowUp':
                case 'w':
                case 'W':
                    this.pacman.setNextDirection(DIRECTIONS.UP);
                    e.preventDefault();
                    break;
                case 'ArrowDown':
                case 's':
                case 'S':
                    this.pacman.setNextDirection(DIRECTIONS.DOWN);
                    e.preventDefault();
                    break;
                case 'ArrowLeft':
                case 'a':
                case 'A':
                    this.pacman.setNextDirection(DIRECTIONS.LEFT);
                    e.preventDefault();
                    break;
                case 'ArrowRight':
                case 'd':
                case 'D':
                    this.pacman.setNextDirection(DIRECTIONS.RIGHT);
                    e.preventDefault();
                    break;
            }
        });
        
        // Add touch controls for mobile devices
        this.setupTouchControls();
        
        // Кнопки управления игрой
        document.getElementById('start-btn').addEventListener('click', () => {
            this.start();
        });
        
        document.getElementById('pause-btn').addEventListener('click', () => {
            this.isRunning = !this.isRunning;
            document.getElementById('start-btn').textContent = this.isRunning ? "Продолжить" : "Начать игру";
        });
        
        document.getElementById('reset-btn').addEventListener('click', () => {
            this.reset();
        });
        
        document.getElementById('menu-btn').addEventListener('click', () => {
            this.isRunning = false;
            if (this.animationFrameId) {
                cancelAnimationFrame(this.animationFrameId);
                this.animationFrameId = null;
            }
            document.getElementById('game-screen').classList.add('hidden');
            document.getElementById('main-menu').classList.remove('hidden');
        });
        
        // Обработчик кнопки сообщения
        document.getElementById('message-btn').addEventListener('click', () => {
            document.getElementById('message').style.display = 'none';
        });
        
        console.log("Обработчики событий установлены");
    }
    
    // Setup touch controls for mobile devices
    setupTouchControls() {
        // Check if we're on a touch device
        if (!('ontouchstart' in window)) return;
        
        // Create touch control elements
        this.createTouchControls();
        
        // Add touch event listeners
        this.addTouchEventListeners();
    }
    
    // Create touch control elements
    createTouchControls() {
        // Create a container for touch controls
        const touchContainer = document.createElement('div');
        touchContainer.id = 'touch-controls';
        touchContainer.className = 'touch-controls';
        
        // Create directional buttons
        const upButton = document.createElement('button');
        upButton.id = 'up-btn';
        upButton.className = 'touch-btn up-btn';
        upButton.innerHTML = '↑';
        
        const downButton = document.createElement('button');
        downButton.id = 'down-btn';
        downButton.className = 'touch-btn down-btn';
        downButton.innerHTML = '↓';
        
        const leftButton = document.createElement('button');
        leftButton.id = 'left-btn';
        leftButton.className = 'touch-btn left-btn';
        leftButton.innerHTML = '←';
        
        const rightButton = document.createElement('button');
        rightButton.id = 'right-btn';
        rightButton.className = 'touch-btn right-btn';
        rightButton.innerHTML = '→';
        
        // Create action buttons
        const actionButton = document.createElement('button');
        actionButton.id = 'action-btn';
        actionButton.className = 'touch-btn action-btn';
        actionButton.innerHTML = '●';
        
        // Add buttons to container
        touchContainer.appendChild(upButton);
        touchContainer.appendChild(downButton);
        touchContainer.appendChild(leftButton);
        touchContainer.appendChild(rightButton);
        touchContainer.appendChild(actionButton);
        
        // Add container to document
        document.body.appendChild(touchContainer);
        
        // Add CSS for touch controls
        this.addTouchControlStyles();
    }
    
    // Add CSS for touch controls
    addTouchControlStyles() {
        if (document.getElementById('touch-control-styles')) return;
        
        const style = document.createElement('style');
        style.id = 'touch-control-styles';
        style.textContent = `
            .touch-controls {
                position: fixed;
                bottom: 20px;
                left: 0;
                right: 0;
                display: none;
                justify-content: center;
                align-items: center;
                z-index: 1000;
                pointer-events: none;
            }
            
            .touch-btn {
                width: 60px;
                height: 60px;
                margin: 10px;
                border-radius: 50%;
                border: 2px solid #fff;
                background: rgba(0, 0, 0, 0.7);
                color: white;
                font-size: 24px;
                display: flex;
                justify-content: center;
                align-items: center;
                pointer-events: auto;
                touch-action: manipulation;
                user-select: none;
                -webkit-tap-highlight-color: transparent;
            }
            
            .touch-btn:active {
                background: rgba(255, 255, 255, 0.3);
            }
            
            .up-btn, .down-btn {
                position: absolute;
                left: 50%;
                transform: translateX(-50%);
            }
            
            .up-btn {
                top: -80px;
            }
            
            .down-btn {
                bottom: -80px;
            }
            
            .left-btn, .right-btn {
                position: absolute;
                top: 50%;
                transform: translateY(-50%);
            }
            
            .left-btn {
                left: -80px;
            }
            
            .right-btn {
                right: -80px;
            }
            
            .action-btn {
                position: absolute;
                right: 20px;
                bottom: 20px;
                width: 80px;
                height: 80px;
                font-size: 32px;
            }
            
            @media (max-width: 768px) {
                .touch-controls {
                    display: flex;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Add touch event listeners
    addTouchEventListeners() {
        // Directional buttons
        document.getElementById('up-btn')?.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.pacman.setNextDirection(DIRECTIONS.UP);
        });
        
        document.getElementById('down-btn')?.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.pacman.setNextDirection(DIRECTIONS.DOWN);
        });
        
        document.getElementById('left-btn')?.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.pacman.setNextDirection(DIRECTIONS.LEFT);
        });
        
        document.getElementById('right-btn')?.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.pacman.setNextDirection(DIRECTIONS.RIGHT);
        });
        
        // Action button (for future use)
        document.getElementById('action-btn')?.addEventListener('touchstart', (e) => {
            e.preventDefault();
            // Could be used for power-up activation or other actions
        });
        
        // Prevent default touch behavior to avoid scrolling
        document.getElementById('touch-controls')?.addEventListener('touchmove', (e) => {
            e.preventDefault();
        });
    }
}

// Экспортируем класс для использования в других файлах
export { PacmanGame };