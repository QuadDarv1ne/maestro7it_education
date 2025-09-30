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
    }

    // Метод для перемещения Пакмана
    move(map, cellSize) {
        // Применяем следующее направление, если возможно
        if (this.nextDirection) {
            const nextPos = this.getNextPosition(this.x, this.y, this.nextDirection, map, cellSize);
            if (this.isValidMove(nextPos.x, nextPos.y, map)) {
                this.direction = this.nextDirection;
                this.nextDirection = null;
            }
        }
        
        // Двигаемся в текущем направлении
        const nextPos = this.getNextPosition(this.x, this.y, this.direction, map, cellSize);
        if (this.isValidMove(nextPos.x, nextPos.y, map)) {
            this.x = nextPos.x;
            this.y = nextPos.y;
        }
    }

    getNextPosition(x, y, direction, map, cellSize) {
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
        
        return { x: newX, y: newY };
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
}

// Экспортируем класс для использования в других файлах
// В браузерной среде добавляем в глобальную область видимости
if (typeof window !== 'undefined') {
    window.Pacman = Pacman;
}

// Для Node.js или модульных систем
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Pacman;
}