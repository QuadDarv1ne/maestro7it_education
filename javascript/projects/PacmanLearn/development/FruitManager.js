class FruitManager {
    constructor() {
        // Фрукты, которые появляются на определенных уровнях
        this.fruitTypes = [
            { type: 'cherry', points: 100, color: '#FF0000', symbol: '🍒', rarity: 'common' },
            { type: 'strawberry', points: 300, color: '#FF00FF', symbol: '🍓', rarity: 'common' },
            { type: 'orange', points: 500, color: '#FFA500', symbol: '🍊', rarity: 'uncommon' },
            { type: 'apple', points: 700, color: '#FF0000', symbol: '🍎', rarity: 'uncommon' },
            { type: 'melon', points: 1000, color: '#00FF00', symbol: '🍉', rarity: 'rare' },
            { type: 'galaxian', points: 2000, color: '#FFFF00', symbol: '⭐', rarity: 'rare' },
            { type: 'bell', points: 3000, color: '#FFFF00', symbol: '🔔', rarity: 'epic' },
            { type: 'key', points: 5000, color: '#FFFF00', symbol: '🔑', rarity: 'legendary' },
            { type: 'banana', points: 1500, color: '#FFD700', symbol: '🍌', rarity: 'uncommon' },
            { type: 'grapes', points: 2500, color: '#9370DB', symbol: '🍇', rarity: 'rare' },
            // New fruit types
            { type: 'pineapple', points: 1200, color: '#FFD700', symbol: '🍍', rarity: 'rare' },
            { type: 'peach', points: 800, color: '#FFB6C1', symbol: '🍑', rarity: 'uncommon' },
            { type: 'pear', points: 600, color: '#90EE90', symbol: '🍐', rarity: 'uncommon' },
            { type: 'coconut', points: 1800, color: '#D2B48C', symbol: '🥥', rarity: 'rare' },
            { type: 'kiwi', points: 900, color: '#ADFF2F', symbol: '🥝', rarity: 'uncommon' },
            { type: 'mango', points: 1600, color: '#FFA500', symbol: '🥭', rarity: 'rare' },
            { type: 'watermelon', points: 2200, color: '#00FF00', symbol: '🍉', rarity: 'epic' },
            { type: 'dragonfruit', points: 3500, color: '#FF69B4', symbol: '🐉', rarity: 'epic' },
            { type: 'starfruit', points: 2800, color: '#7FFF00', symbol: '⭐', rarity: 'epic' },
            { type: 'durian', points: 4000, color: '#DAA520', symbol: '💥', rarity: 'legendary' }
        ];
        this.fruitTimer = 0;
        this.fruitVisible = false;
        this.currentFruit = null;
        this.spawnChance = 0.005; // Base spawn chance
        // Add tracking for collected fruits
        this.collectedFruits = {};
        this.totalFruitsSpawned = 0;
        this.rarityBonuses = {
            'common': 1,
            'uncommon': 1.2,
            'rare': 1.5,
            'epic': 2.0,
            'legendary': 3.0
        };
        // Pre-allocate arrays for weighted selection to reduce garbage collection
        this.availableFruits = [];
        this.weightedFruits = [];
        // Pre-allocate object for current fruit to reduce allocations
        this.tempFruit = {
            x: 0,
            y: 0,
            type: '',
            points: 0,
            color: '#FFFFFF',
            symbol: '',
            rarity: 'common',
            spawnTime: 0,
            pulsePhase: 0
        };
    }

    // Показать фрукт на карте
    spawnFruit(map, foodCount, totalFood, level) {
        // Increase spawn chance based on level for more excitement
        const levelAdjustedSpawnChance = Math.min(this.spawnChance * (1 + level * 0.1), 0.02);
        
        // Add bonus spawn chance if player is doing well
        const foodRatio = foodCount / totalFood;
        const performanceBonus = foodRatio > 0.7 ? 0.005 : 0; // Bonus if player is collecting food well
        
        if (!this.fruitVisible && Math.random() < (levelAdjustedSpawnChance + performanceBonus) && foodCount > totalFood * 0.2) {
            // Найти свободное место для фрукта
            let attempts = 0;
            while (attempts < 50) {
                const x = Math.floor(Math.random() * (map[0].length - 2)) + 1;
                const y = Math.floor(Math.random() * (map.length - 2)) + 1;
                
                if (map[y][x] === 1) { // Пустое место
                    // Select fruit based on level with some randomness and rarity system
                    const fruit = this.selectFruitByLevelAndRarity(level);
                    
                    // Reuse pre-allocated object instead of creating new one
                    this.tempFruit.x = x;
                    this.tempFruit.y = y;
                    this.tempFruit.type = fruit.type;
                    this.tempFruit.points = fruit.points;
                    this.tempFruit.color = fruit.color;
                    this.tempFruit.symbol = fruit.symbol;
                    this.tempFruit.rarity = fruit.rarity;
                    this.tempFruit.spawnTime = Date.now();
                    this.tempFruit.pulsePhase = Math.random() * Math.PI * 2; // Random starting phase for animation
                    
                    this.currentFruit = {...this.tempFruit}; // Create a copy for current use
                    this.fruitVisible = true;
                    this.totalFruitsSpawned++;
                    break;
                }
                attempts++;
            }
        }
        
        // Удалить фрукт через 10 секунд или if player has been idle
        if (this.fruitVisible && (Date.now() - this.currentFruit.spawnTime > 10000 || 
            (foodCount === this.lastFoodCount && Date.now() - this.currentFruit.spawnTime > 7000))) {
            this.fruitVisible = false;
            this.currentFruit = null;
        }
        
        // Store last food count for idle detection
        this.lastFoodCount = foodCount;
    }
    
    // Select fruit based on level and rarity
    selectFruitByLevelAndRarity(level) {
        // Reuse arrays instead of creating new ones
        this.availableFruits.length = 0;
        this.weightedFruits.length = 0;
        
        this.fruitTypes.forEach((fruit, index) => {
            // Higher level fruits become available at higher levels
            const levelRequirement = Math.max(1, Math.floor(index / 2));
            
            if (level >= levelRequirement) {
                // Add multiple entries based on rarity (common fruits appear more often)
                const rarityWeights = {
                    'common': 5,
                    'uncommon': 3,
                    'rare': 2,
                    'epic': 1,
                    'legendary': 0.5
                };
                
                const weight = rarityWeights[fruit.rarity] || 1;
                const count = Math.max(1, Math.floor(weight));
                
                for (let i = 0; i < count; i++) {
                    this.weightedFruits.push(fruit);
                }
            }
        });
        
        // If no fruits are available for this level, use the first available fruit
        if (this.weightedFruits.length === 0) {
            return this.fruitTypes[0];
        }
        
        // Select random fruit from weighted list
        const randomIndex = Math.floor(Math.random() * this.weightedFruits.length);
        return this.weightedFruits[randomIndex];
    }

    // Проверить сбор фрукта
    checkFruitCollection(pacmanX, pacmanY, scoreCallback, particleCallback) {
        if (this.fruitVisible && pacmanX === this.currentFruit.x && pacmanY === this.currentFruit.y) {
            // Apply rarity bonus to points
            const rarityBonus = this.rarityBonuses[this.currentFruit.rarity] || 1;
            const points = Math.floor(this.currentFruit.points * rarityBonus);
            
            particleCallback(this.currentFruit.x, this.currentFruit.y, this.currentFruit.color);
            
            // Track collected fruit
            if (!this.collectedFruits[this.currentFruit.type]) {
                this.collectedFruits[this.currentFruit.type] = 0;
            }
            this.collectedFruits[this.currentFruit.type]++;
            
            // Special effect for rare fruits
            if (this.currentFruit.rarity === 'epic' || this.currentFruit.rarity === 'legendary') {
                // Could trigger special effects here
                console.log(`Rare fruit collected: ${this.currentFruit.type}`);
            }
            
            this.fruitVisible = false;
            this.currentFruit = null;
            return points;
        }
        return 0;
    }

    // Draw fruits on the map
    drawFruits(ctx, cellSize) {
        if (this.fruitVisible && this.currentFruit) {
            const pixelX = this.currentFruit.x * cellSize + cellSize/2;
            const pixelY = this.currentFruit.y * cellSize + cellSize/2;
            
            // Анимация пульсации с unique phase for each fruit
            const pulse = Math.sin((Date.now() / 200) + this.currentFruit.pulsePhase) * 0.2 + 1;
            
            // Add glow effect for rare fruits
            if (this.currentFruit.rarity === 'epic' || this.currentFruit.rarity === 'legendary') {
                ctx.shadowColor = this.currentFruit.color;
                ctx.shadowBlur = 15;
            }
            
            ctx.save();
            ctx.translate(pixelX, pixelY);
            ctx.scale(pulse, pulse);
            
            ctx.font = '24px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = this.currentFruit.color;
            
            // Add outline for better visibility
            ctx.lineWidth = 2;
            ctx.strokeStyle = '#000000';
            ctx.strokeText(this.currentFruit.symbol, 0, 0);
            ctx.fillText(this.currentFruit.symbol, 0, 0);
            
            ctx.restore();
            
            // Reset shadow
            ctx.shadowBlur = 0;
            
            // Draw rarity indicator for rare fruits
            if (this.currentFruit.rarity === 'rare' || this.currentFruit.rarity === 'epic' || this.currentFruit.rarity === 'legendary') {
                let indicatorColor;
                switch(this.currentFruit.rarity) {
                    case 'rare': indicatorColor = '#00BFFF'; break;
                    case 'epic': indicatorColor = '#FF00FF'; break;
                    case 'legendary': indicatorColor = '#FFD700'; break;
                    default: indicatorColor = '#FFFFFF';
                }
                
                ctx.fillStyle = indicatorColor;
                ctx.beginPath();
                ctx.arc(pixelX + 15, pixelY - 15, 4, 0, Math.PI * 2);
                ctx.fill();
            }
        }
    }

    // Метод для сброса фруктов
    reset() {
        this.fruitVisible = false;
        this.currentFruit = null;
        this.lastFoodCount = 0;
    }
    
    // Get statistics about fruit collection
    getStats() {
        return {
            totalSpawned: this.totalFruitsSpawned,
            collected: this.collectedFruits,
            totalCollected: Object.values(this.collectedFruits).reduce((a, b) => a + b, 0)
        };
    }
    
    // Get available fruits for current level
    getAvailableFruits(level) {
        this.availableFruits.length = 0; // Clear array
        this.fruitTypes.forEach((fruit, index) => {
            const levelRequirement = Math.max(1, Math.floor(index / 2));
            if (level >= levelRequirement) {
                this.availableFruits.push(fruit);
            }
        });
        return this.availableFruits;
    }
}

// Экспортируем класс для использования в других файлах
export { FruitManager };