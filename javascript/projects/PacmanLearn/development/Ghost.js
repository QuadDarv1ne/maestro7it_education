import { GHOST_STATES, DIRECTIONS, COLLISION_SETTINGS } from './Constants.js';

class Ghost {
    constructor(x, y, color, name, speed = 0.8) {
        this.x = x;
        this.y = y;
        this.startX = x;
        this.startY = y;
        this.direction = DIRECTIONS.LEFT;
        this.color = color;
        this.name = name;
        this.speed = speed;
        this.defaultSpeed = speed;
        // Reuse array instead of creating new ones to reduce garbage collection
        this.possibleMoves = [];
        // Add state tracking for more intelligent behavior
        this.state = GHOST_STATES.CHASE; // 'chase', 'scatter', 'frightened'
        this.stateTimer = 0;
        this.scatterTarget = this.getScatterTarget();
        // Add sub-pixel positioning for smoother movement
        this.pixelX = x * 22 + 11; // Assuming cellSize = 22, center of cell
        this.pixelY = y * 22 + 11;
        this.speedPixels = speed * 2; // Convert to pixels per frame
        this.cellSize = 22;
        // Add collision radius for more precise collision detection
        this.collisionRadius = COLLISION_SETTINGS.GHOST_RADIUS;
        // Add pathfinding variables
        this.path = [];
        this.currentTarget = null;
        // Pre-allocate objects for position calculations
        this.tempPosition = { x: 0, y: 0 };
    }

    // Get scatter target based on ghost name (corner of the map)
    getScatterTarget() {
        switch(this.name) {
            case 'Blinky': return { x: 19, y: 0 }; // Top-right corner
            case 'Pinky': return { x: 0, y: 0 };   // Top-left corner
            case 'Inky': return { x: 19, y: 15 };  // Bottom-right corner
            case 'Clyde': return { x: 0, y: 15 };  // Bottom-left corner
            default: return { x: 10, y: 10 };
        }
    }

    // Метод для перемещения призрака
    move(pacmanX, pacmanY, map, powerMode, cellSize) {
        this.cellSize = cellSize;
        
        // Adjust speed based on power mode
        const effectiveSpeed = powerMode ? this.speed * 0.5 : this.speed;
        this.speedPixels = effectiveSpeed * 2;
        
        // Move ghosts more consistently rather than randomly
        // Only skip movement based on speed factor
        if (Math.random() > effectiveSpeed) return;
        
        // Update state timer
        this.stateTimer++;
        
        // Switch between chase and scatter modes periodically
        if (this.stateTimer > 300 && !powerMode) { // About 5 seconds at 60 FPS
            this.state = this.state === GHOST_STATES.CHASE ? GHOST_STATES.SCATTER : GHOST_STATES.CHASE;
            this.stateTimer = 0;
        }
        
        // In power mode, always frightened
        if (powerMode) {
            this.state = GHOST_STATES.FRIGHTENED;
        } else if (this.state === GHOST_STATES.FRIGHTENED) {
            // Return to normal state after power mode ends
            this.state = GHOST_STATES.CHASE;
        }
        
        // Enhanced AI for ghost movement
        // Calculate distance to Pacman
        const dx = pacmanX - this.x;
        const dy = pacmanY - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // Different behaviors based on ghost type, distance, and state
        let targetX, targetY;
        
        switch(this.state) {
            case GHOST_STATES.FRIGHTENED:
                // Run away randomly
                targetX = this.x + (Math.random() > 0.5 ? 5 : -5);
                targetY = this.y + (Math.random() > 0.5 ? 5 : -5);
                break;
                
            case GHOST_STATES.SCATTER:
                // Go to corner
                targetX = this.scatterTarget.x;
                targetY = this.scatterTarget.y;
                break;
                
            case GHOST_STATES.CHASE:
            default:
                // Special behaviors for different ghosts
                switch(this.name) {
                    case 'Blinky': // Red ghost - aggressive, targets Pacman directly
                        targetX = pacmanX;
                        targetY = pacmanY;
                        break;
                        
                    case 'Pinky': // Pink ghost - ambush, targets 4 tiles ahead of Pacman
                        switch(this.direction) {
                            case DIRECTIONS.UP: targetY = pacmanY - 4; break;
                            case DIRECTIONS.DOWN: targetY = pacmanY + 4; break;
                            case DIRECTIONS.LEFT: targetX = pacmanX - 4; break;
                            case DIRECTIONS.RIGHT: targetX = pacmanX + 4; break;
                            default: 
                                targetX = pacmanX;
                                targetY = pacmanY;
                        }
                        // Add some predictive behavior
                        if (distance < 6) {
                            // When close, be more aggressive
                            targetX = pacmanX;
                            targetY = pacmanY;
                        }
                        break;
                        
                    case 'Inky': // Cyan ghost - complex behavior based on Blinky's position
                        // Calculate a more complex target based on Pacman's direction and Blinky's position
                        const blinky = { x: 10, y: 8 }; // Approximate Blinky's position
                        const vectorX = pacmanX - blinky.x;
                        const vectorY = pacmanY - blinky.y;
                        targetX = pacmanX + vectorX * 2;
                        targetY = pacmanY + vectorY * 2;
                        
                        // When far, be more unpredictable
                        if (distance > 10) {
                            if (Math.random() > 0.7) {
                                // Occasionally make a random move
                                targetX = this.x + (Math.random() > 0.5 ? 3 : -3);
                                targetY = this.y + (Math.random() > 0.5 ? 3 : -3);
                            }
                        }
                        break;
                        
                    case 'Clyde': // Orange ghost - coward, runs away when close
                        if (distance < 5) {
                            // Run away from Pacman
                            targetX = this.x - dx * 2;
                            targetY = this.y - dy * 2;
                        } else {
                            // When far, chase Pacman normally
                            targetX = pacmanX;
                            targetY = pacmanY;
                        }
                        break;
                        
                    default:
                        targetX = pacmanX;
                        targetY = pacmanY;
                }
        }
        
        // Reuse array instead of creating new one to reduce garbage collection
        this.possibleMoves.length = 0; // Clear array without creating new one
        
        // Use pre-allocated object for position calculations
        const directions = [DIRECTIONS.UP, DIRECTIONS.DOWN, DIRECTIONS.LEFT, DIRECTIONS.RIGHT];
        
        for (let i = 0; i < directions.length; i++) {
            const dir = directions[i];
            const nextPos = this.getNextPosition(this.x, this.y, dir, map, cellSize, this.tempPosition);
            if (this.isValidMove(nextPos.x, nextPos.y, map)) {
                // Calculate distance to target for this move
                const moveDx = nextPos.x - targetX;
                const moveDy = nextPos.y - targetY;
                const moveDistance = Math.sqrt(moveDx * moveDx + moveDy * moveDy);
                
                // Add some randomness to make behavior less predictable (but not in frightened mode)
                const randomness = (this.state === GHOST_STATES.FRIGHTENED) ? 0 : Math.random() * 3;
                
                this.possibleMoves.push({
                    direction: dir,
                    x: nextPos.x,
                    y: nextPos.y,
                    distance: moveDistance + randomness
                });
            }
        }
        
        // Sort moves by distance to target (closest first)
        // If in frightened mode, sort in reverse (farthest first)
        if (this.state === GHOST_STATES.FRIGHTENED) {
            this.possibleMoves.sort((a, b) => b.distance - a.distance);
        } else {
            this.possibleMoves.sort((a, b) => a.distance - b.distance);
        }
        
        // Choose the best move
        if (this.possibleMoves.length > 0) {
            const bestMove = this.possibleMoves[0];
            
            // Update direction
            this.direction = bestMove.direction;
            
            // Update sub-pixel position
            switch(this.direction) {
                case DIRECTIONS.UP:
                    this.pixelY -= this.speedPixels;
                    break;
                case DIRECTIONS.DOWN:
                    this.pixelY += this.speedPixels;
                    break;
                case DIRECTIONS.LEFT:
                    this.pixelX -= this.speedPixels;
                    break;
                case DIRECTIONS.RIGHT:
                    this.pixelX += this.speedPixels;
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

    // Метод для сброса позиции призрака
    resetPosition() {
        this.x = this.startX;
        this.y = this.startY;
        this.direction = this.getInitialDirection();
        this.state = GHOST_STATES.CHASE;
        this.stateTimer = 0;
        // Reset sub-pixel positioning
        this.pixelX = this.x * this.cellSize + this.cellSize/2;
        this.pixelY = this.y * this.cellSize + this.cellSize/2;
    }

    getInitialDirection() {
        // Определяем начальное направление в зависимости от имени призрака
        switch(this.name) {
            case 'Blinky': return DIRECTIONS.LEFT;
            case 'Pinky': return DIRECTIONS.UP;
            case 'Inky': return DIRECTIONS.DOWN;
            case 'Clyde': return DIRECTIONS.RIGHT;
            default: return DIRECTIONS.LEFT;
        }
    }

    // Метод для увеличения скорости призрака
    increaseSpeed(amount) {
        this.speed = Math.min(this.speed + amount, 1.0);
        this.speedPixels = this.speed * 2;
    }

    // Метод для сброса скорости к значению по умолчанию
    resetSpeed() {
        this.speed = this.defaultSpeed;
        this.speedPixels = this.defaultSpeed * 2;
    }
    
    // Метод для проверки столкновения с другим объектом (более точная проверка)
    checkCollision(otherX, otherY, otherRadius = COLLISION_SETTINGS.GHOST_RADIUS) {
        // Use sub-pixel positions for more accurate collision detection
        const dx = this.pixelX - (otherX * this.cellSize + this.cellSize/2);
        const dy = this.pixelY - (otherY * this.cellSize + this.cellSize/2);
        const distance = Math.sqrt(dx * dx + dy * dy);
        return distance < (this.collisionRadius + otherRadius);
    }
}

// Экспортируем класс для использования в других файлах
export { Ghost };