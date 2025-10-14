import { DIRECTIONS, COLLISION_SETTINGS, GAME_SETTINGS } from './Constants.js';

class Pacman {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.startX = x;
        this.startY = y;
        this.direction = DIRECTIONS.RIGHT;
        this.nextDirection = null;
        this.mouthAngle = 0;
        this.mouthOpening = 0.1;
        this.powerMode = false;
        this.powerModeTimer = 0;
        // Add sub-pixel positioning for smoother movement
        this.pixelX = x * GAME_SETTINGS.DEFAULT_CELL_SIZE + GAME_SETTINGS.DEFAULT_CELL_SIZE/2; // Center of cell
        this.pixelY = y * GAME_SETTINGS.DEFAULT_CELL_SIZE + GAME_SETTINGS.DEFAULT_CELL_SIZE/2;
        this.speed = GAME_SETTINGS.DEFAULT_PACMAN_SPEED; // Pixels per frame
        this.cellSize = GAME_SETTINGS.DEFAULT_CELL_SIZE;
        // Add collision radius for more precise collision detection
        this.collisionRadius = COLLISION_SETTINGS.PACMAN_RADIUS;
        // Pre-allocate object for position calculations
        this.tempPosition = { x: 0, y: 0 };
        // Add tunnel transition tracking
        this.isInTunnel = false;
        this.tunnelTransitionProgress = 0;
    }

    // Метод для перемещения Пакмана
    move(map, cellSize) {
        this.cellSize = cellSize;
        
        // Применяем следующее направление, если возможно
        if (this.nextDirection) {
            const nextPos = this.getNextPosition(this.x, this.y, this.nextDirection, map, cellSize, this.tempPosition);
            if (this.isValidMove(nextPos.x, nextPos.y, map)) {
                this.direction = this.nextDirection;
                this.nextDirection = null;
            }
        }
        
        // Двигаемся в текущем направлении
        const nextPos = this.getNextPosition(this.x, this.y, this.direction, map, cellSize, this.tempPosition);
        if (this.isValidMove(nextPos.x, nextPos.y, map)) {
            // Update sub-pixel position
            switch(this.direction) {
                case DIRECTIONS.UP: 
                    this.pixelY -= this.speed;
                    break;
                case DIRECTIONS.DOWN: 
                    this.pixelY += this.speed;
                    break;
                case DIRECTIONS.LEFT: 
                    this.pixelX -= this.speed;
                    break;
                case DIRECTIONS.RIGHT: 
                    this.pixelX += this.speed;
                    break;
            }
            
            // Handle tunnel transitions more smoothly
            this.handleTunnelTransition(map, cellSize);
            
            // Update grid position when we've moved enough
            const newGridX = Math.floor(this.pixelX / cellSize);
            const newGridY = Math.floor(this.pixelY / cellSize);
            
            // Only update grid position if it's actually changed
            if (newGridX !== this.x || newGridY !== this.y) {
                this.x = newGridX;
                this.y = newGridY;
            }
        }
    }

    // Handle tunnel transitions more smoothly
    handleTunnelTransition(map, cellSize) {
        // Left tunnel exit
        if (this.x === 0 && this.direction === DIRECTIONS.LEFT) {
            this.isInTunnel = true;
            this.tunnelTransitionProgress = (this.pixelX / cellSize) + 1;
            if (this.tunnelTransitionProgress >= 1) {
                this.pixelX = map[0].length * cellSize - (cellSize - this.pixelX % cellSize);
                this.isInTunnel = false;
                this.tunnelTransitionProgress = 0;
                // Notify that a tunnel transition was completed
                return true;
            }
        }
        // Right tunnel exit
        else if (this.x === map[0].length - 1 && this.direction === DIRECTIONS.RIGHT) {
            this.isInTunnel = true;
            this.tunnelTransitionProgress = (this.pixelX / cellSize) - (map[0].length - 1);
            if (this.tunnelTransitionProgress >= 1) {
                this.pixelX = -(cellSize - this.pixelX % cellSize);
                this.isInTunnel = false;
                this.tunnelTransitionProgress = 0;
                // Notify that a tunnel transition was completed
                return true;
            }
        }
        // Reset tunnel state when not in tunnel
        else if (this.isInTunnel) {
            this.isInTunnel = false;
            this.tunnelTransitionProgress = 0;
        }
        
        return false;
    }

    getNextPosition(x, y, direction, map, cellSize, result = {}) {
        let newX = x;
        let newY = y;
        
        switch(direction) {
            case DIRECTIONS.UP: newY--; break;
            case DIRECTIONS.DOWN: newY++; break;
            case DIRECTIONS.LEFT: newX--; break;
            case DIRECTIONS.RIGHT: newX++; break;
        }
        
        // Туннельные переходы
        if (newX < 0) newX = map[0].length - 1;
        if (newX >= map[0].length) newX = 0;
        if (newY < 0) newY = map.length - 1;
        if (newY >= map.length) newY = 0;
        
        result.x = newX;
        result.y = newY;
        return result;
    }

    isValidMove(x, y, map) {
        // Проверяем границы карты по вертикали
        if (y < 0 || y >= map.length) return false;
        
        // Проверяем стены
        if (map[y][x] === 0) return false;
        
        return true;
    }

    // Метод для сброса позиции Пакмана
    resetPosition() {
        this.x = this.startX;
        this.y = this.startY;
        this.direction = DIRECTIONS.RIGHT;
        this.nextDirection = null;
        this.powerMode = false;
        this.powerModeTimer = 0;
        // Reset sub-pixel positioning
        this.pixelX = this.x * this.cellSize + this.cellSize/2;
        this.pixelY = this.y * this.cellSize + this.cellSize/2;
        // Reset tunnel state
        this.isInTunnel = false;
        this.tunnelTransitionProgress = 0;
    }

    // Анимация рта Пакмана
    animateMouth() {
        this.mouthAngle += this.mouthOpening;
        if (this.mouthAngle <= 0 || this.mouthAngle >= 0.5) {
            this.mouthOpening *= -1;
        }
    }

    // Метод для активации режима силы
    activatePowerMode(duration = GAME_SETTINGS.POWER_MODE_DURATION) {
        this.powerMode = true;
        this.powerModeTimer = duration;
    }

    // Метод для обновления таймера режима силы
    updatePowerMode(deltaTime) {
        if (this.powerMode) {
            this.powerModeTimer -= deltaTime;
            if (this.powerModeTimer <= 0) {
                this.powerMode = false;
                this.powerModeTimer = 0;
            }
        }
    }

    // Метод для установки следующего направления
    setNextDirection(direction) {
        this.nextDirection = direction;
    }
    
    // Метод для проверки столкновения с другим объектом (более точная проверка)
    checkCollision(otherX, otherY, otherRadius = COLLISION_SETTINGS.PACMAN_RADIUS) {
        // Use sub-pixel positions for more accurate collision detection
        const dx = this.pixelX - (otherX * this.cellSize + this.cellSize/2);
        const dy = this.pixelY - (otherY * this.cellSize + this.cellSize/2);
        const distance = Math.sqrt(dx * dx + dy * dy);
        return distance < (this.collisionRadius + otherRadius);
    }
    
    // Метод для получения текущих координат для столкновений
    getCollisionPosition() {
        return {
            x: this.pixelX / this.cellSize,
            y: this.pixelY / this.cellSize,
            pixelX: this.pixelX,
            pixelY: this.pixelY
        };
    }

    // Get power mode effect intensity (for visual effects)
    getPowerModeEffect() {
        if (!this.powerMode) return 0;
        
        // Pulsing effect that gets stronger as power mode nears expiration
        const timeLeft = this.powerModeTimer / GAME_SETTINGS.POWER_MODE_DURATION;
        const pulse = Math.sin(Date.now() / 100) * 0.5 + 0.5;
        return timeLeft < 0.3 ? pulse * (1 - timeLeft) : 0; // Only show effect when time is running out
    }

    // Check if Pacman is in a tunnel transition
    isInTunnelTransition() {
        return this.isInTunnel;
    }

    // Get tunnel transition progress (0-1)
    getTunnelTransitionProgress() {
        return this.tunnelTransitionProgress;
    }
}

// Экспортируем класс для использования в других файлах
export { Pacman };