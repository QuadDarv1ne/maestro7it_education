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
        // Add personality traits for unique ghost behaviors
        this.personality = this.getPersonality();
        // Performance optimization: limit AI calculations
        this.lastAiUpdate = 0;
        this.aiUpdateInterval = 100; // Update AI every 100ms
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

    // Get personality traits for unique ghost behaviors
    getPersonality() {
        switch(this.name) {
            case 'Blinky': // Red ghost - aggressive
                return { aggression: 1.0, predictiveness: 0.8, randomness: 0.1 };
            case 'Pinky': // Pink ghost - ambush
                return { aggression: 0.7, predictiveness: 1.0, randomness: 0.2 };
            case 'Inky': // Cyan ghost - unpredictable
                return { aggression: 0.5, predictiveness: 0.6, randomness: 0.5 };
            case 'Clyde': // Orange ghost - coward
                return { aggression: 0.3, predictiveness: 0.4, randomness: 0.4 };
            default:
                return { aggression: 0.5, predictiveness: 0.5, randomness: 0.5 };
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
        
        // Limit AI calculations for performance
        const now = Date.now();
        if (now - this.lastAiUpdate < this.aiUpdateInterval) {
            // Just move in current direction
            this.moveInCurrentDirection(map, cellSize);
            return;
        }
        this.lastAiUpdate = now;
        
        // Enhanced AI for ghost movement
        // Calculate distance to Pacman
        const dx = pacmanX - this.x;
        const dy = pacmanY - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // Different behaviors based on ghost type, distance, and state
        let targetX, targetY;
        
        switch(this.state) {
            case GHOST_STATES.FRIGHTENED:
                // Run away randomly with some intelligence
                const fleeDirection = Math.random();
                if (fleeDirection < this.personality.randomness) {
                    // Completely random movement
                    targetX = this.x + (Math.random() > 0.5 ? 5 : -5);
                    targetY = this.y + (Math.random() > 0.5 ? 5 : -5);
                } else {
                    // Run away from Pacman with some randomness
                    const randomFactor = 1 + (Math.random() * this.personality.randomness);
                    targetX = this.x - dx * randomFactor;
                    targetY = this.y - dy * randomFactor;
                }
                break;
                
            case GHOST_STATES.SCATTER:
                // Go to corner
                targetX = this.scatterTarget.x;
                targetY = this.scatterTarget.y;
                break;
                
            case GHOST_STATES.CHASE:
            default:
                // Special behaviors for different ghosts based on personality
                switch(this.name) {
                    case 'Blinky': // Red ghost - aggressive, targets Pacman directly with predictive behavior
                        // When close, be more aggressive
                        if (distance < 5) {
                            targetX = pacmanX;
                            targetY = pacmanY;
                        } else {
                            // Predict Pacman's movement based on his current direction
                            let predictX = pacmanX, predictY = pacmanY;
                            // Add predictive movement based on personality
                            switch(this.direction) {
                                case DIRECTIONS.UP: predictY -= 2 * this.personality.predictiveness; break;
                                case DIRECTIONS.DOWN: predictY += 2 * this.personality.predictiveness; break;
                                case DIRECTIONS.LEFT: predictX -= 2 * this.personality.predictiveness; break;
                                case DIRECTIONS.RIGHT: predictX += 2 * this.personality.predictiveness; break;
                            }
                            targetX = predictX;
                            targetY = predictY;
                        }
                        break;
                        
                    case 'Pinky': // Pink ghost - ambush, targets 4 tiles ahead of Pacman
                        // Predict where Pacman will be in 4 moves
                        let predictX = pacmanX, predictY = pacmanY;
                        switch(this.direction) {
                            case DIRECTIONS.UP: predictY -= 4; break;
                            case DIRECTIONS.DOWN: predictY += 4; break;
                            case DIRECTIONS.LEFT: predictX -= 4; break;
                            case DIRECTIONS.RIGHT: predictX += 4; break;
                        }
                        
                        // Add some predictive behavior based on personality
                        if (distance < 6) {
                            // When close, be more aggressive
                            targetX = pacmanX;
                            targetY = pacmanY;
                        } else {
                            // When far, use predictive ambush strategy
                            targetX = predictX;
                            targetY = predictY;
                        }
                        break;
                        
                    case 'Inky': // Cyan ghost - complex behavior based on Blinky's position and Pacman's direction
                        // Calculate a more complex target based on Pacman's direction and distance
                        let vectorX = dx;
                        let vectorY = dy;
                        
                        // Add personality-based unpredictability
                        if (Math.random() < this.personality.randomness) {
                            // Occasionally make a random move
                            targetX = this.x + (Math.random() > 0.5 ? 3 : -3);
                            targetY = this.y + (Math.random() > 0.5 ? 3 : -3);
                        } else {
                            // Normal Inky behavior with personality modifier
                            targetX = pacmanX + vectorX * this.personality.predictiveness;
                            targetY = pacmanY + vectorY * this.personality.predictiveness;
                        }
                        
                        // When far, be more unpredictable
                        if (distance > 10) {
                            if (Math.random() > 0.7) {
                                // Occasionally make a random move
                                targetX = this.x + (Math.random() > 0.5 ? 3 : -3);
                                targetY = this.y + (Math.random() > 0.5 ? 3 : -3);
                            }
                        }
                        break;
                        
                    case 'Clyde': // Orange ghost - coward, runs away when close but chases when far
                        if (distance < 5) {
                            // Run away from Pacman with personality modifier
                            const cowardFactor = 2 - this.personality.aggression;
                            targetX = this.x - dx * cowardFactor;
                            targetY = this.y - dy * cowardFactor;
                        } else if (distance > 8) {
                            // When far, chase Pacman normally
                            targetX = pacmanX;
                            targetY = pacmanY;
                        } else {
                            // In middle distance, move unpredictably
                            if (Math.random() < this.personality.randomness) {
                                targetX = this.x + (Math.random() > 0.5 ? 2 : -2);
                                targetY = this.y + (Math.random() > 0.5 ? 2 : -2);
                            } else {
                                targetX = pacmanX;
                                targetY = pacmanY;
                            }
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
                const randomness = (this.state === GHOST_STATES.FRIGHTENED) ? 0 : Math.random() * this.personality.randomness * 3;
                
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
    
    // Simple movement in current direction for performance
    moveInCurrentDirection(map, cellSize) {
        const nextPos = this.getNextPosition(this.x, this.y, this.direction, map, cellSize, this.tempPosition);
        if (this.isValidMove(nextPos.x, nextPos.y, map)) {
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
        } else {
            // If can't move in current direction, find a new direction
            this.findNewDirection(map, cellSize);
        }
    }
    
    // Find a new direction when current direction is blocked
    findNewDirection(map, cellSize) {
        // Try to find a valid move
        const directions = [DIRECTIONS.UP, DIRECTIONS.DOWN, DIRECTIONS.LEFT, DIRECTIONS.RIGHT];
        const validDirections = [];
        
        for (let i = 0; i < directions.length; i++) {
            const dir = directions[i];
            const nextPos = this.getNextPosition(this.x, this.y, dir, map, cellSize, this.tempPosition);
            if (this.isValidMove(nextPos.x, nextPos.y, map)) {
                validDirections.push(dir);
            }
        }
        
        // Choose a random valid direction
        if (validDirections.length > 0) {
            this.direction = validDirections[Math.floor(Math.random() * validDirections.length)];
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
        // Reset AI update timer
        this.lastAiUpdate = 0;
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
    
    // Get visual effect for current state (for drawing)
    getStateEffect() {
        switch(this.state) {
            case GHOST_STATES.FRIGHTENED:
                // Pulsing blue effect when frightened
                const pulse = Math.sin(Date.now() / 200) * 0.5 + 0.5;
                return {
                    color: '#0000FF',
                    glow: pulse * 10,
                    scale: 1 + pulse * 0.1
                };
            case GHOST_STATES.SCATTER:
                // Subtle effect when scattering
                return {
                    color: this.color,
                    glow: 2,
                    scale: 1
                };
            default:
                // Normal state
                return {
                    color: this.color,
                    glow: 0,
                    scale: 1
                };
        }
    }

    // Get personality-based visual effect
    getPersonalityEffect() {
        // Different visual effects based on personality
        let effectColor = this.color;
        let effectIntensity = 0;
        
        if (this.personality.aggression > 0.8) {
            // Aggressive ghosts (Blinky) have a red glow
            effectColor = '#FF0000';
            effectIntensity = this.personality.aggression * 5;
        } else if (this.personality.randomness > 0.4) {
            // Unpredictable ghosts (Inky) have a rainbow effect
            const hue = (Date.now() / 50) % 360;
            effectColor = `hsl(${hue}, 100%, 50%)`;
            effectIntensity = this.personality.randomness * 3;
        }
        
        return {
            color: effectColor,
            glow: effectIntensity
        };
    }
}

// Экспортируем класс для использования в других файлах
export { Ghost };