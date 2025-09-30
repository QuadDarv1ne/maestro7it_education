class Pacman {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.startX = x;
        this.startY = y;
        this.direction = 'right';
        this.nextDirection = null;
        this.mouthAngle = 0;
        this.mouthOpening = 0.1;
        this.powerMode = false;
        this.powerModeTimer = 0;
        // Add sub-pixel positioning for smoother movement
        this.pixelX = x * 22 + 11; // Assuming cellSize = 22, center of cell
        this.pixelY = y * 22 + 11;
        this.speed = 2.5; // Pixels per frame
        this.cellSize = 22;
        // Add collision radius for more precise collision detection
        this.collisionRadius = 8;
        // Pre-allocate object for position calculations
        this.tempPosition = { x: 0, y: 0 };
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
                case 'up':
                    this.pixelY -= this.speed;
                    break;
                case 'down':
                    this.pixelY += this.speed;
                    break;
                case 'left':
                    this.pixelX -= this.speed;
                    break;
                case 'right':
                    this.pixelX += this.speed;
                    break;
            }
            
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

    getNextPosition(x, y, direction, map, cellSize, result = {}) {
        let newX = x;
        let newY = y;
        
        switch(direction) {
            case 'up': newY--; break;
            case 'down': newY++; break;
            case 'left': newX--; break;
            case 'right': newX++; break;
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
        this.direction = 'right';
        this.nextDirection = null;
        this.powerMode = false;
        this.powerModeTimer = 0;
        // Reset sub-pixel positioning
        this.pixelX = this.x * this.cellSize + this.cellSize/2;
        this.pixelY = this.y * this.cellSize + this.cellSize/2;
    }

    // Анимация рта Пакмана
    animateMouth() {
        this.mouthAngle += this.mouthOpening;
        if (this.mouthAngle <= 0 || this.mouthAngle >= 0.5) {
            this.mouthOpening *= -1;
        }
    }

    // Метод для активации режима силы
    activatePowerMode(duration = 10000) {
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
    checkCollision(otherX, otherY, otherRadius = 8) {
        // Use sub-pixel positions for more accurate collision detection
        const dx = this.pixelX - (otherX * this.cellSize + this.cellSize/2);
        const dy = this.pixelY - (otherY * this.cellSize + this.cellSize/2);
        const distance = Math.sqrt(dx * dx + dy * dy);
        return distance < (this.collisionRadius + otherRadius);
    }
}

// Экспортируем класс для использования в других файлах
export { Pacman };