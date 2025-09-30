class FruitManager {
    constructor() {
        // Фрукты, которые появляются на определенных уровнях
        this.fruitTypes = [
            { type: 'cherry', points: 100, color: '#FF0000', symbol: '🍒' },
            { type: 'strawberry', points: 300, color: '#FF00FF', symbol: '🍓' },
            { type: 'orange', points: 500, color: '#FFA500', symbol: '🍊' },
            { type: 'apple', points: 700, color: '#FF0000', symbol: '🍎' },
            { type: 'melon', points: 1000, color: '#00FF00', symbol: '🍉' },
            { type: 'galaxian', points: 2000, color: '#FFFF00', symbol: '⭐' },
            { type: 'bell', points: 3000, color: '#FFFF00', symbol: '🔔' },
            { type: 'key', points: 5000, color: '#FFFF00', symbol: '🔑' }
        ];
        this.fruitTimer = 0;
        this.fruitVisible = false;
        this.currentFruit = null;
    }

    // Показать фрукт на карте
    spawnFruit(map, foodCount, totalFood, level) {
        if (!this.fruitVisible && Math.random() < 0.005 && foodCount > totalFood * 0.3) {
            // Найти свободное место для фрукта
            let attempts = 0;
            while (attempts < 50) {
                const x = Math.floor(Math.random() * (map[0].length - 2)) + 1;
                const y = Math.floor(Math.random() * (map.length - 2)) + 1;
                
                if (map[y][x] === 1) { // Пустое место
                    this.currentFruit = {
                        x: x,
                        y: y,
                        ...this.fruitTypes[Math.min(level - 1, this.fruitTypes.length - 1)],
                        spawnTime: Date.now()
                    };
                    this.fruitVisible = true;
                    break;
                }
                attempts++;
            }
        }
        
        // Удалить фрукт через 10 секунд
        if (this.fruitVisible && Date.now() - this.currentFruit.spawnTime > 10000) {
            this.fruitVisible = false;
            this.currentFruit = null;
        }
    }

    // Проверить сбор фрукта
    checkFruitCollection(pacmanX, pacmanY, scoreCallback, particleCallback) {
        if (this.fruitVisible && pacmanX === this.currentFruit.x && pacmanY === this.currentFruit.y) {
            const points = this.currentFruit.points;
            particleCallback(this.currentFruit.x, this.currentFruit.y, this.currentFruit.color);
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
            
            // Анимация пульсации
            const pulse = Math.sin(Date.now() / 200) * 0.2 + 1;
            ctx.save();
            ctx.translate(pixelX, pixelY);
            ctx.scale(pulse, pulse);
            
            ctx.font = '20px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(this.currentFruit.symbol, 0, 0);
            
            ctx.restore();
        }
    }

    // Метод для сброса фруктов
    reset() {
        this.fruitVisible = false;
        this.currentFruit = null;
    }
}

// Экспортируем класс для использования в других файлах
// В браузерной среде добавляем в глобальную область видимости
if (typeof window !== 'undefined') {
    window.FruitManager = FruitManager;
}

// Для Node.js или модульных систем
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FruitManager;
}