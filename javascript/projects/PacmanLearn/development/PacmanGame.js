// Импортируем необходимые классы
import { Pacman } from './Pacman.js';
import { Ghost } from './Ghost.js';
import { GameMap } from './GameMap.js';
import { SoundManager } from './SoundManager.js';
import { ParticleManager } from './ParticleManager.js';
import { FruitManager } from './FruitManager.js';
import { AchievementManager } from './AchievementManager.js';
import { Utils } from './Utils.js';
import { GAME_SETTINGS, UI_CONSTANTS } from './Constants.js';

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
        
        // Pre-allocate objects for performance
        this.tempComboDisplay = {
            text: '',
            x: 0,
            y: 0,
            startTime: 0
        };
        
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
        this.achievementManager.currentLevelStartLives = this.lives; // Track lives for this level
        
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
            
            // Notify achievement manager that level is completed
            this.achievementManager.onLevelCompleted();
            
            // Проверяем достижение "Перфекционист"
            this.achievementManager.checkAchievements(this.score, this.level, this.consecutiveEats);
            
            // Переход на следующий уровень
            this.nextLevel();
        }
    }
    
    // Метод для обработки столкновений
    checkCollisions() {
        // Получаем текущую карту уровня
        const currentMap = this.gameMap.getLevelMap(this.level);
        
        // Проверяем сбор еды
        const cell = currentMap[this.pacman.y][this.pacman.x];
        if (cell === 2) { // Обычная еда
            currentMap[this.pacman.y][this.pacman.x] = 1;
            this.foodCount++;
            this.score += 10;
            this.soundManager.playSound('eat');
            this.createCombo();
            // Создаем визуальный эффект при сборе обычной еды
            this.particleManager.createEffect(
                this.pacman.x * this.cellSize + this.cellSize/2, 
                this.pacman.y * this.cellSize + this.cellSize/2, 
                this.particleManager.particleTypes.SPARKLE,
                '#FFF',
                5
            );
            this.updateScore();
            this.checkLevelComplete();
            // Increment food eaten for achievement tracking
            this.achievementManager.incrementFoodEaten();
        } else if (cell === 3) { // Супер-еда
            currentMap[this.pacman.y][this.pacman.x] = 1;
            this.foodCount++;
            this.score += 50;
            this.pacman.powerMode = true;
            this.pacman.powerModeTimer = GAME_SETTINGS.POWER_MODE_DURATION; // 10 секунд
            this.canvas.classList.add('power-mode');
            this.soundManager.playSound('power');
            this.createCombo();
            // Создаем визуальный эффект при сборе супер-еды
            this.particleManager.createEffect(
                this.pacman.x * this.cellSize + this.cellSize/2, 
                this.pacman.y * this.cellSize + this.cellSize/2, 
                this.particleManager.particleTypes.SPARKLE,
                '#FFF',
                15
            );
            // Добавляем дополнительный эффект для супер-еды
            this.createSuperFoodEffect(this.pacman.x, this.pacman.y);
            this.updateScore();
            this.checkLevelComplete();
            // Increment food eaten for achievement tracking
            this.achievementManager.incrementFoodEaten();
        }
        
        // Проверяем сбор фрукта с более точным столкновением
        this.checkFruitCollection();
        
        // Проверяем столкновения с привидениями с более точным столкновением
        this.ghosts.forEach(ghost => {
            // Use more precise collision detection
            if (this.pacman.checkCollision(ghost.x, ghost.y, ghost.collisionRadius)) {
                if (this.pacman.powerMode) {
                    // Пакман съедает привидение
                    this.score += 200;
                    this.achievementManager.incrementGhostsEaten(); // Track for achievements
                    this.soundManager.playSound('ghost');
                    this.particleManager.createEffect(
                        ghost.x * this.cellSize + this.cellSize/2, 
                        ghost.y * this.cellSize + this.cellSize/2, 
                        this.particleManager.particleTypes.EXPLOSION,
                        ghost.color,
                        20
                    );
                    // Создаем специальный эффект при поедании привидения
                    this.createGhostEatenEffect(ghost.x, ghost.y, ghost.color);
                    // Возвращаем привидение на начальную позицию
                    ghost.x = 10;
                    ghost.y = ghost.color === 'red' ? 8 : ghost.color === 'pink' ? 9 : 
                              ghost.color === 'cyan' ? 9 : 10;
                    ghost.resetPosition(); // Reset sub-pixel position too
                    this.updateScore();
                    // Check achievements after eating a ghost
                    this.achievementManager.checkAchievements(this.score, this.level, this.consecutiveEats);
                } else {
                    // Привидение съедает Пакмана
                    this.lives--;
                    this.achievementManager.onLifeLost(); // Track for achievements
                    this.updateLives();
                    this.soundManager.playSound('death');
                    this.particleManager.createEffect(
                        this.pacman.x * this.cellSize + this.cellSize/2, 
                        this.pacman.y * this.cellSize + this.cellSize/2, 
                        this.particleManager.particleTypes.EXPLOSION,
                        'yellow',
                        30
                    );
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
    
    // Проверяем сбор фрукта с более точным столкновением
    checkFruitCollection() {
        const fruitPoints = this.fruitManager.checkFruitCollection(
            this.pacman.x, 
            this.pacman.y,
            (points) => {
                this.score += points;
                this.updateScore();
            },
            (x, y, color) => {
                this.particleManager.createEffect(
                    x * this.cellSize + this.cellSize/2, 
                    y * this.cellSize + this.cellSize/2, 
                    this.particleManager.particleTypes.SPARKLE,
                    color,
                    25
                );
                // Track fruit collection with fruit type for achievements
                if (this.fruitManager.currentFruit) {
                    this.achievementManager.incrementFruitsCollected(this.fruitManager.currentFruit.type);
                } else {
                    this.achievementManager.incrementFruitsCollected();
                }
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
        this.soundManager.playSound('gameover');
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
    
    // Метод для отрисовки игры
    draw() {
        // Очистка холста
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Получаем текущую карту уровня
        this.map = this.gameMap.getLevelMap(this.level);
        
        // Отрисовка карты
        this.drawMap();
        
        // Отрисовка фруктов
        this.fruitManager.drawFruits(this.ctx, this.cellSize);
        
        // Отрисовка Пакмана
        this.drawPacman();
        
        // Отрисовка привидений
        this.drawGhosts();
        
        // Отрисовка частиц
        this.particleManager.drawParticles(this.ctx);
        
        // Отрисовка комбо
        this.drawCombo();
    }
    
    // Метод для отрисовки карты
    drawMap() {
        for (let y = 0; y < this.map.length; y++) {
            for (let x = 0; x < this.map[y].length; x++) {
                const cell = this.map[y][x];
                const pixelX = x * this.cellSize;
                const pixelY = y * this.cellSize;
                
                switch(cell) {
                    case 0: // Стена
                        this.ctx.fillStyle = '#2222FF';
                        this.ctx.fillRect(pixelX, pixelY, this.cellSize, this.cellSize);
                        // Добавляем детали стен
                        this.ctx.fillStyle = '#0000CC';
                        this.ctx.fillRect(pixelX + 2, pixelY + 2, this.cellSize - 4, this.cellSize - 4);
                        break;
                    case 1: // Путь
                        this.ctx.fillStyle = '#000';
                        this.ctx.fillRect(pixelX, pixelY, this.cellSize, this.cellSize);
                        break;
                    case 2: // Еда
                        this.ctx.fillStyle = '#FFF';
                        this.ctx.beginPath();
                        this.ctx.arc(pixelX + this.cellSize/2, pixelY + this.cellSize/2, 3, 0, Math.PI * 2);
                        this.ctx.fill();
                        break;
                    case 3: // Супер-еда
                        this.ctx.fillStyle = '#FFF';
                        this.ctx.beginPath();
                        this.ctx.arc(pixelX + this.cellSize/2, pixelY + this.cellSize/2, 6, 0, Math.PI * 2);
                        this.ctx.fill();
                        break;
                }
            }
        }
    }
    
    // Метод для отрисовки Пакмана
    drawPacman() {
        // Use sub-pixel positioning for smoother movement
        const pixelX = this.pacman.pixelX;
        const pixelY = this.pacman.pixelY;
        const radius = this.cellSize/2 - 2;
        
        this.ctx.fillStyle = '#FFD700'; // Золотой цвет
        this.ctx.beginPath();
        
        let startAngle, endAngle;
        switch(this.pacman.direction) {
            case 'right':
                startAngle = this.pacman.mouthAngle * Math.PI;
                endAngle = (2 - this.pacman.mouthAngle) * Math.PI;
                break;
            case 'down':
                startAngle = (0.5 + this.pacman.mouthAngle) * Math.PI;
                endAngle = (2.5 - this.pacman.mouthAngle) * Math.PI;
                break;
            case 'left':
                startAngle = (1 + this.pacman.mouthAngle) * Math.PI;
                endAngle = (3 - this.pacman.mouthAngle) * Math.PI;
                break;
            case 'up':
                startAngle = (1.5 + this.pacman.mouthAngle) * Math.PI;
                endAngle = (3.5 - this.pacman.mouthAngle) * Math.PI;
                break;
        }
        
        this.ctx.arc(pixelX, pixelY, radius, startAngle, endAngle);
        this.ctx.lineTo(pixelX, pixelY);
        this.ctx.fill();
    }
    
    // Метод для отрисовки привидений
    drawGhosts() {
        this.ghosts.forEach(ghost => {
            // Use sub-pixel positioning for smoother movement
            const pixelX = ghost.pixelX;
            const pixelY = ghost.pixelY;
            const radius = this.cellSize/2 - 2;
            
            // Тело привидения
            this.ctx.fillStyle = this.pacman.powerMode ? '#0000FF' : ghost.color;
            
            // Добавляем свечение во время power mode
            if (this.pacman.powerMode) {
                this.ctx.shadowColor = '#0000FF';
                this.ctx.shadowBlur = 10;
            }
            
            this.ctx.beginPath();
            this.ctx.arc(pixelX, pixelY - 2, radius, Math.PI, 0, false); // Верхняя часть
            this.ctx.lineTo(pixelX + radius, pixelY + radius - 2);
            
            // Нижняя часть с волнами
            for (let i = 0; i < 3; i++) {
                this.ctx.lineTo(pixelX + radius - (i * radius * 2/3), pixelY + radius - 6);
                this.ctx.lineTo(pixelX + radius - ((i + 0.5) * radius * 2/3), pixelY + radius - 2);
            }
            
            this.ctx.lineTo(pixelX - radius, pixelY + radius - 2);
            this.ctx.lineTo(pixelX - radius, pixelY - 2);
            this.ctx.fill();
            
            // Сбрасываем свечение
            this.ctx.shadowBlur = 0;
            
            // Глаза
            this.ctx.fillStyle = 'white';
            this.ctx.beginPath();
            this.ctx.arc(pixelX - 4, pixelY - 4, 3, 0, Math.PI * 2);
            this.ctx.arc(pixelX + 4, pixelY - 4, 3, 0, Math.PI * 2);
            this.ctx.fill();
            
            this.ctx.fillStyle = 'black';
            let eyeOffsetX = 0, eyeOffsetY = 0;
            switch(ghost.direction) {
                case 'left': eyeOffsetX = -1; break;
                case 'right': eyeOffsetX = 1; break;
                case 'up': eyeOffsetY = -1; break;
                case 'down': eyeOffsetY = 1; break;
            }
            
            this.ctx.beginPath();
            this.ctx.arc(pixelX - 4 + eyeOffsetX, pixelY - 4 + eyeOffsetY, 1.5, 0, Math.PI * 2);
            this.ctx.arc(pixelX + 4 + eyeOffsetX, pixelY - 4 + eyeOffsetY, 1.5, 0, Math.PI * 2);
            this.ctx.fill();
        });
    }
    
    // Метод для отрисовки комбо
    drawCombo() {
        // Получаем настройки из localStorage или используем значения по умолчанию
        let settings = { animationsEnabled: true };
        try {
            const savedSettings = localStorage.getItem('pacmanSettings');
            if (savedSettings) {
                settings = JSON.parse(savedSettings);
            }
        } catch (e) {
            console.warn('Ошибка загрузки настроек анимации:', e);
        }
        
        if (this.comboDisplay && settings.animationsEnabled) {
            const elapsed = Date.now() - this.comboDisplay.startTime;
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
        }
    }
    
    // Метод для отображения комбо
    showCombo(bonus) {
        // Reuse pre-allocated object to reduce garbage collection
        this.tempComboDisplay.text = `КОМБО +${bonus}`;
        this.tempComboDisplay.x = this.pacman.x * this.cellSize + this.cellSize/2;
        this.tempComboDisplay.y = this.pacman.y * this.cellSize;
        this.tempComboDisplay.startTime = Date.now();
        
        this.comboDisplay = {...this.tempComboDisplay};
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
        
        // Only add points if fruit was collected (points > 0)
        // Sound is already played in the callback, so we don't play it again here
        if (points > 0) {
            this.score += points;
            this.achievementManager.incrementFruitsCollected();
            this.updateScore();
        }
    }
    
    // Метод для создания эффекта при сборе супер-еды
    createSuperFoodEffect(x, y) {
        // Получаем настройки из localStorage или используем значения по умолчанию
        let settings = { animationsEnabled: true };
        try {
            const savedSettings = localStorage.getItem('pacmanSettings');
            if (savedSettings) {
                settings = JSON.parse(savedSettings);
            }
        } catch (e) {
            console.warn('Ошибка загрузки настроек анимации:', e);
        }
        
        if (!settings.animationsEnabled) return;
        
        // Создаем концентрические круги через частицы
        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                for (let j = 0; j < 20; j++) {
                    const angle = (j / 20) * Math.PI * 2;
                    const distance = 20 + i * 10;
                    const pixelX = x * this.cellSize + this.cellSize/2;
                    const pixelY = y * this.cellSize + this.cellSize/2;
                    
                    this.particleManager.createEffect(
                        pixelX + Math.cos(angle) * distance,
                        pixelY + Math.sin(angle) * distance,
                        this.particleManager.particleTypes.GLOW,
                        '#00FFFF',
                        1
                    );
                }
            }, i * 100);
        }
    }
    
    // Метод для создания эффекта при поедании привидения
    createGhostEatenEffect(x, y, color) {
        // Получаем настройки из localStorage или используем значения по умолчанию
        let settings = { animationsEnabled: true };
        try {
            const savedSettings = localStorage.getItem('pacmanSettings');
            if (savedSettings) {
                settings = JSON.parse(savedSettings);
            }
        } catch (e) {
            console.warn('Ошибка загрузки настроек анимации:', e);
        }
        
        if (!settings.animationsEnabled) return;
        
        // Создаем взрыв частиц
        const pixelX = x * this.cellSize + this.cellSize/2;
        const pixelY = y * this.cellSize + this.cellSize/2;
        
        this.particleManager.createEffect(
            pixelX,
            pixelY,
            this.particleManager.particleTypes.EXPLOSION,
            color,
            30
        );
    }
    
    // Метод для создания эффекта при потере жизни
    createLifeLostEffect(x, y) {
        // Получаем настройки из localStorage или используем значения по умолчанию
        let settings = { animationsEnabled: true };
        try {
            const savedSettings = localStorage.getItem('pacmanSettings');
            if (savedSettings) {
                settings = JSON.parse(savedSettings);
            }
        } catch (e) {
            console.warn('Ошибка загрузки настроек анимации:', e);
        }
        
        if (!settings.animationsEnabled) return;
        
        // Создаем красные частицы
        const pixelX = x * this.cellSize + this.cellSize/2;
        const pixelY = y * this.cellSize + this.cellSize/2;
        
        this.particleManager.createEffect(
            pixelX,
            pixelY,
            this.particleManager.particleTypes.EXPLOSION,
            '#FF0000',
            40
        );
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
                this.particleManager.createEffect(
                    this.pacman.x * this.cellSize + this.cellSize/2, 
                    this.pacman.y * this.cellSize + this.cellSize/2, 
                    this.particleManager.particleTypes.SPARKLE,
                    '#FF00FF',
                    20
                );
            }
        } else {
            this.consecutiveEats = 1;
        }
        this.lastEatTime = now;
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
        try {
            const scoreElement = document.getElementById('score');
            if (scoreElement) {
                scoreElement.textContent = this.score;
            } else {
                console.warn('Score element not found in DOM');
            }
        } catch (error) {
            console.error('Error updating score display:', error);
        }
    }
    
    // Метод для обновления уровня
    updateLevel() {
        try {
            const levelElement = document.getElementById('level');
            if (levelElement) {
                levelElement.textContent = this.level;
            } else {
                console.warn('Level element not found in DOM');
            }
        } catch (error) {
            console.error('Error updating level display:', error);
        }
    }
    
    // Метод для обновления жизней
    updateLives() {
        try {
            const livesElement = document.getElementById('lives');
            if (livesElement) {
                livesElement.innerHTML = '❤️'.repeat(this.lives);
            } else {
                console.warn('Lives element not found in DOM');
            }
        } catch (error) {
            console.error('Error updating lives display:', error);
        }
    }
    
    // Метод для отображения сообщений
    showMessage(text) {
        try {
            const titleElement = document.getElementById('message-title');
            const textElement = document.getElementById('message-text');
            const messageElement = document.getElementById('message');
            
            if (titleElement && textElement && messageElement) {
                titleElement.textContent = 'Игра окончена';
                textElement.innerHTML = text;
                messageElement.style.display = 'block';
            } else {
                console.warn('Message elements not found in DOM');
                // Fallback to alert
                alert(text);
            }
        } catch (error) {
            console.error('Error showing message:', error);
            // Fallback to alert
            alert(text);
        }
    }
    
    // Система рекордов
    loadHighScores() {
        try {
            const scores = localStorage.getItem('pacmanHighScores');
            if (scores) {
                const parsed = JSON.parse(scores);
                // Validate that it's an array
                if (Array.isArray(parsed)) {
                    return parsed;
                } else {
                    console.warn('Invalid high scores format in localStorage');
                    return [];
                }
            }
            return [];
        } catch (e) {
            console.error('Ошибка загрузки рекордов:', e);
            return [];
        }
    }
    
    saveHighScore() {
        try {
            // Validate score before saving
            if (typeof this.score !== 'number' || this.score < 0) {
                console.warn('Invalid score value:', this.score);
                return;
            }
            
            const name = prompt('Поздравляем! Вы набрали ' + this.score + ' очков. Введите ваше имя:', 'Игрок') || 'Аноним';
            // Validate name
            if (typeof name !== 'string' || name.trim().length === 0) {
                console.warn('Invalid player name');
                return;
            }
            
            const newScore = { 
                name: name.trim(), 
                score: this.score, 
                date: new Date().toLocaleDateString() 
            };
            
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
        try {
            const menuElement = document.getElementById('main-menu');
            const scoresScreenElement = document.getElementById('highscores-screen');
            const scoresListElement = document.getElementById('scores-list');
            
            if (!menuElement || !scoresScreenElement || !scoresListElement) {
                console.warn('High scores elements not found in DOM');
                return;
            }
            
            menuElement.classList.add('hidden');
            scoresScreenElement.classList.remove('hidden');
            
            scoresListElement.innerHTML = '';
            
            if (this.highScores.length === 0) {
                scoresListElement.innerHTML = '<div class="score-entry"><span>Нет рекордов</span></div>';
                return;
            }
            
            this.highScores.forEach((score, index) => {
                const entry = document.createElement('div');
                entry.className = 'score-entry';
                entry.innerHTML = `
                    <span class="score-rank">#${index + 1}</span>
                    <span class="score-name">${this.escapeHtml(score.name)}</span>
                    <span class="score-value">${score.score}</span>
                `;
                scoresListElement.appendChild(entry);
            });
        } catch (error) {
            console.error('Error showing high scores:', error);
        }
    }
    
    // Utility method to escape HTML to prevent XSS
    escapeHtml(text) {
        if (typeof text !== 'string') return '';
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }
    
    hideHighScores() {
        try {
            const scoresScreenElement = document.getElementById('highscores-screen');
            const menuElement = document.getElementById('main-menu');
            
            if (!scoresScreenElement || !menuElement) {
                console.warn('High scores elements not found in DOM');
                return;
            }
            
            scoresScreenElement.classList.add('hidden');
            menuElement.classList.remove('hidden');
        } catch (error) {
            console.error('Error hiding high scores:', error);
        }
    }
    
    // Система настроек
    loadSettings() {
        try {
            const settings = localStorage.getItem('pacmanSettings');
            if (settings) {
                const parsed = JSON.parse(settings);
                // Validate settings object
                if (typeof parsed === 'object' && parsed !== null) {
                    return {
                        difficulty: parsed.difficulty || 'normal',
                        gameSpeed: parsed.gameSpeed || 150,
                        soundEnabled: parsed.soundEnabled !== undefined ? parsed.soundEnabled : true,
                        musicEnabled: parsed.musicEnabled !== undefined ? parsed.musicEnabled : true,
                        animationsEnabled: parsed.animationsEnabled !== undefined ? parsed.animationsEnabled : true
                    };
                } else {
                    console.warn('Invalid settings format in localStorage');
                }
            }
        } catch (e) {
            console.error('Ошибка загрузки настроек:', e);
        }
        
        // Return default settings if anything fails
        return {
            difficulty: 'normal',
            gameSpeed: 150,
            soundEnabled: true,
            musicEnabled: true,
            animationsEnabled: true
        };
    }
    
    applySettings() {
        try {
            const difficultyElement = document.getElementById('difficulty');
            const gameSpeedElement = document.getElementById('game-speed');
            const soundEnabledElement = document.getElementById('sound-enabled');
            const musicEnabledElement = document.getElementById('music-enabled');
            const animationsEnabledElement = document.getElementById('animations-enabled');
            
            if (!difficultyElement || !gameSpeedElement || !soundEnabledElement || 
                !musicEnabledElement || !animationsEnabledElement) {
                console.warn('Settings elements not found in DOM');
                return;
            }
            
            const settings = {
                difficulty: difficultyElement.value,
                gameSpeed: parseInt(gameSpeedElement.value),
                soundEnabled: soundEnabledElement.checked,
                musicEnabled: musicEnabledElement.checked,
                animationsEnabled: animationsEnabledElement.checked
            };
            
            // Validate settings values
            if (isNaN(settings.gameSpeed) || settings.gameSpeed < 50 || settings.gameSpeed > 300) {
                console.warn('Invalid game speed value:', settings.gameSpeed);
                settings.gameSpeed = 150; // Default value
            }
            
            this.settings = settings;
            
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