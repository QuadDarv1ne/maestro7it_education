class Ghost {
    constructor(x, y, color, name, speed = 0.8) {
        this.x = x;
        this.y = y;
        this.startX = x;
        this.startY = y;
        this.direction = 'left';
        this.color = color;
        this.name = name;
        this.speed = speed;
        this.defaultSpeed = speed;
    }

    // Метод для перемещения призрака
    move(pacmanX, pacmanY, map, powerMode, cellSize) {
        // Adjust speed based on power mode
        const effectiveSpeed = powerMode ? this.speed * 0.5 : this.speed;
        
        // Move ghosts more consistently rather than randomly
        // Only skip movement based on speed factor
        if (Math.random() > effectiveSpeed) return;
        
        // Enhanced AI for ghost movement
        // Calculate distance to Pacman
        const dx = pacmanX - this.x;
        const dy = pacmanY - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // Different behaviors based on ghost type and distance
        let targetX = pacmanX;
        let targetY = pacmanY;
        
        // Special behaviors for different ghosts
        switch(this.name) {
            case 'Blinky': // Red ghost - aggressive, targets Pacman directly
                // Always targets Pacman
                break;
            case 'Pinky': // Pink ghost - ambush, targets 4 tiles ahead of Pacman
                switch(this.direction) {
                    case 'up': targetY -= 4; break;
                    case 'down': targetY += 4; break;
                    case 'left': targetX -= 4; break;
                    case 'right': targetX += 4; break;
                }
                break;
            case 'Inky': // Cyan ghost - erratic, targets based on Blinky's position
                // More random movement when far, more targeted when close
                if (distance > 8) {
                    // Random movement when far away
                    targetX = this.x + (Math.random() > 0.5 ? 2 : -2);
                    targetY = this.y + (Math.random() > 0.5 ? 2 : -2);
                }
                break;
            case 'Clyde': // Orange ghost - coward, runs away when close
                if (distance < 5) {
                    // Run away from Pacman
                    targetX = this.x - dx;
                    targetY = this.y - dy;
                }
                break;
        }
        
        // Calculate possible moves
        const possibleMoves = [];
        const directions = ['up', 'down', 'left', 'right'];
        
        directions.forEach(dir => {
            const nextPos = this.getNextPosition(this.x, this.y, dir, map, cellSize);
            if (this.isValidMove(nextPos.x, nextPos.y, map)) {
                // Calculate distance to target for this move
                const moveDx = nextPos.x - targetX;
                const moveDy = nextPos.y - targetY;
                const moveDistance = Math.sqrt(moveDx * moveDx + moveDy * moveDy);
                
                possibleMoves.push({
                    direction: dir,
                    x: nextPos.x,
                    y: nextPos.y,
                    distance: moveDistance
                });
            }
        });
        
        // Sort moves by distance to target (closest first)
        // If in power mode, sort in reverse (farthest first)
        if (powerMode) {
            possibleMoves.sort((a, b) => b.distance - a.distance);
        } else {
            possibleMoves.sort((a, b) => a.distance - b.distance);
        }
        
        // Choose the best move
        if (possibleMoves.length > 0) {
            const bestMove = possibleMoves[0];
            this.x = bestMove.x;
            this.y = bestMove.y;
            this.direction = bestMove.direction;
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
        if (newY < 0) newY = map.length - 1;
        if (newY >= map.length) newY = 0;
        
        return { x: newX, y: newY };
    }

    isValidMove(x, y, map) {
        // Проверяем границы карты по вертикали
        if (y < 0 || y >= map.length) return false;
        
        // Проверяем стены
        if (map[y][x] === 0) return false;
        
        return true;
    }

    // Метод для сброса позиции призрака
    resetPosition() {
        this.x = this.startX;
        this.y = this.startY;
        this.direction = this.getInitialDirection();
    }

    getInitialDirection() {
        // Определяем начальное направление в зависимости от имени призрака
        switch(this.name) {
            case 'Blinky': return 'left';
            case 'Pinky': return 'up';
            case 'Inky': return 'down';
            case 'Clyde': return 'right';
            default: return 'left';
        }
    }

    // Метод для увеличения скорости призрака
    increaseSpeed(amount) {
        this.speed = Math.min(this.speed + amount, 1.0);
    }

    // Метод для сброса скорости к значению по умолчанию
    resetSpeed() {
        this.speed = this.defaultSpeed;
    }
}

// Экспортируем класс для использования в других файлах
// В браузерной среде добавляем в глобальную область видимости
if (typeof window !== 'undefined') {
    window.Ghost = Ghost;
}

// Для Node.js или модульных систем
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Ghost;
}