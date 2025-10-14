import { CELL_TYPES, GAME_SETTINGS } from './Constants.js';

class PowerUpManager {
    constructor() {
        // Define power-up types
        this.powerUpTypes = {
            SPEED_BOOST: {
                id: 'speed_boost',
                name: 'Ускорение',
                description: 'Увеличивает скорость Пакмана',
                duration: 5000, // 5 seconds
                color: '#00FF00',
                symbol: '⚡',
                points: 500
            },
            INVINCIBILITY: {
                id: 'invincibility',
                name: 'Неуязвимость',
                description: 'Пакман неуязвим для призраков',
                duration: 3000, // 3 seconds
                color: '#FF00FF',
                symbol: '🛡️',
                points: 1000
            },
            FREEZE_GHOSTS: {
                id: 'freeze_ghosts',
                name: 'Заморозка',
                description: 'Замораживает всех призраков',
                duration: 4000, // 4 seconds
                color: '#00FFFF',
                symbol: '❄️',
                points: 750
            },
            EXTRA_LIFE: {
                id: 'extra_life',
                name: 'Дополнительная жизнь',
                description: 'Добавляет одну жизнь',
                duration: 0, // Instant
                color: '#FF0000',
                symbol: '❤️',
                points: 0
            },
            POINTS_MULTIPLIER: {
                id: 'points_multiplier',
                name: 'Множитель очков',
                description: 'Удваивает все очки на 10 секунд',
                duration: 10000, // 10 seconds
                color: '#FFFF00',
                symbol: '🌟',
                points: 300
            }
        };
        
        // Active power-ups
        this.activePowerUps = [];
        
        // Power-up spawn settings
        this.spawnChance = 0.002; // 0.2% chance per frame
        this.currentPowerUp = null;
        this.powerUpVisible = false;
    }
    
    // Spawn a random power-up
    spawnPowerUp(map) {
        if (this.powerUpVisible || Math.random() > this.spawnChance) {
            return;
        }
        
        // Find a valid position for the power-up
        let attempts = 0;
        while (attempts < 50) {
            const x = Math.floor(Math.random() * (map[0].length - 2)) + 1;
            const y = Math.floor(Math.random() * (map.length - 2)) + 1;
            
            if (map[y][x] === CELL_TYPES.PATH) {
                // Get a random power-up type
                const powerUpTypes = Object.values(this.powerUpTypes);
                const randomPowerUp = powerUpTypes[Math.floor(Math.random() * powerUpTypes.length)];
                
                this.currentPowerUp = {
                    x: x,
                    y: y,
                    ...randomPowerUp,
                    spawnTime: Date.now()
                };
                this.powerUpVisible = true;
                break;
            }
            attempts++;
        }
    }
    
    // Check if Pacman collects a power-up
    checkPowerUpCollection(pacmanX, pacmanY, pacman, game) {
        if (!this.powerUpVisible || !this.currentPowerUp) {
            return false;
        }
        
        if (pacmanX === this.currentPowerUp.x && pacmanY === this.currentPowerUp.y) {
            // Apply the power-up effect
            this.applyPowerUp(this.currentPowerUp, pacman, game);
            
            // Add points
            if (this.currentPowerUp.points > 0) {
                game.score += this.currentPowerUp.points;
                game.updateScore();
            }
            
            // Hide the power-up
            this.powerUpVisible = false;
            this.currentPowerUp = null;
            
            return true;
        }
        
        // Remove power-up after 15 seconds if not collected
        if (Date.now() - this.currentPowerUp.spawnTime > 15000) {
            this.powerUpVisible = false;
            this.currentPowerUp = null;
        }
        
        return false;
    }
    
    // Apply power-up effect
    applyPowerUp(powerUp, pacman, game) {
        switch (powerUp.id) {
            case 'speed_boost':
                // Increase Pacman's speed temporarily
                const originalSpeed = pacman.speed;
                pacman.speed *= 1.5;
                this.activePowerUps.push({
                    id: powerUp.id,
                    endTime: Date.now() + powerUp.duration,
                    cleanup: () => { pacman.speed = originalSpeed; }
                });
                break;
                
            case 'invincibility':
                // Make Pacman invincible temporarily
                const originalPowerMode = pacman.powerMode;
                pacman.powerMode = true;
                this.activePowerUps.push({
                    id: powerUp.id,
                    endTime: Date.now() + powerUp.duration,
                    cleanup: () => { pacman.powerMode = originalPowerMode; }
                });
                break;
                
            case 'freeze_ghosts':
                // Freeze all ghosts temporarily
                game.ghosts.forEach(ghost => {
                    const originalSpeed = ghost.speed;
                    ghost.speed = 0;
                    this.activePowerUps.push({
                        id: powerUp.id,
                        endTime: Date.now() + powerUp.duration,
                        cleanup: () => { ghost.speed = originalSpeed; }
                    });
                });
                break;
                
            case 'extra_life':
                // Add an extra life
                game.lives++;
                game.updateLives();
                break;
                
            case 'points_multiplier':
                // Double points temporarily
                // This would need to be handled in the game logic where points are added
                this.activePowerUps.push({
                    id: powerUp.id,
                    endTime: Date.now() + powerUp.duration,
                    multiplier: 2
                });
                break;
        }
    }
    
    // Update active power-ups
    update() {
        const now = Date.now();
        for (let i = this.activePowerUps.length - 1; i >= 0; i--) {
            const powerUp = this.activePowerUps[i];
            if (now > powerUp.endTime) {
                // Clean up the power-up
                if (powerUp.cleanup) {
                    powerUp.cleanup();
                }
                this.activePowerUps.splice(i, 1);
            }
        }
    }
    
    // Check if points multiplier is active
    isPointsMultiplierActive() {
        return this.activePowerUps.some(powerUp => powerUp.id === 'points_multiplier');
    }
    
    // Get points multiplier
    getPointsMultiplier() {
        const multiplierPowerUp = this.activePowerUps.find(powerUp => powerUp.id === 'points_multiplier');
        return multiplierPowerUp ? multiplierPowerUp.multiplier : 1;
    }
    
    // Draw power-up on the map
    draw(ctx, cellSize) {
        if (this.powerUpVisible && this.currentPowerUp) {
            const pixelX = this.currentPowerUp.x * cellSize + cellSize/2;
            const pixelY = this.currentPowerUp.y * cellSize + cellSize/2;
            
            // Animate pulsing effect
            const pulse = Math.sin(Date.now() / 200) * 0.2 + 1;
            
            // Add rotation effect
            const rotation = Date.now() / 1000;
            
            // Add glow effect
            ctx.shadowColor = this.currentPowerUp.color;
            ctx.shadowBlur = 15;
            
            ctx.save();
            ctx.translate(pixelX, pixelY);
            ctx.scale(pulse, pulse);
            ctx.rotate(rotation);
            
            ctx.font = '24px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = this.currentPowerUp.color;
            ctx.fillText(this.currentPowerUp.symbol, 0, 0);
            
            // Add a secondary visual element
            ctx.font = '16px Arial';
            ctx.fillStyle = '#FFFFFF';
            ctx.fillText('?', 0, -15);
            
            ctx.restore();
            
            // Reset shadow
            ctx.shadowBlur = 0;
            
            // Draw a circular background
            ctx.save();
            ctx.translate(pixelX, pixelY);
            ctx.rotate(-rotation); // Rotate back for background
            
            ctx.beginPath();
            ctx.arc(0, 0, cellSize/2 - 2, 0, Math.PI * 2);
            ctx.strokeStyle = this.currentPowerUp.color;
            ctx.lineWidth = 2;
            ctx.stroke();
            
            ctx.restore();
        }
    }
    
    // Reset power-ups
    reset() {
        this.activePowerUps = [];
        this.powerUpVisible = false;
        this.currentPowerUp = null;
    }

    // Get the type of the last collected power-up
    getLastCollectedPowerUpType() {
        if (this.currentPowerUp) {
            return this.currentPowerUp.id;
        }
        return null;
    }
}

// Export the class
export { PowerUpManager };