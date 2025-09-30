class AchievementManager {
    constructor() {
        this.achievements = [
            { id: 'first_game', name: 'Первый шаг', description: 'Начать первую игру', unlocked: false, points: 100 },
            { id: 'score_1000', name: 'Тысячник', description: 'Набрать 1000 очков', unlocked: false, points: 200 },
            { id: 'score_5000', name: 'Пяти тысячник', description: 'Набрать 5000 очков', unlocked: false, points: 500 },
            { id: 'level_5', name: 'Продвинутый', description: 'Достичь 5 уровня', unlocked: false, points: 300 },
            { id: 'combo_10', name: 'Комбо-мастер', description: 'Собрать 10 комбо', unlocked: false, points: 400 },
            { id: 'ghost_hunter', name: 'Охотник за привидениями', description: 'Съесть 20 привидений', unlocked: false, points: 600 },
            { id: 'fruit_lover', name: 'Любитель фруктов', description: 'Собрать 10 фруктов', unlocked: false, points: 350 },
            { id: 'survivor', name: 'Выживший', description: 'Пройти уровень без потери жизни', unlocked: false, points: 700 }
        ];

        this.ghostsEaten = 0;
        this.fruitsCollected = 0;
        this.levelsCompletedWithoutDeath = 0;
        this.currentLevelStartLives = 3;
    }

    // Check and unlock achievements
    checkAchievements(score, level, consecutiveEats) {
        // First game
        if (!this.achievements[0].unlocked) {
            this.unlockAchievement('first_game');
        }
        
        // Score achievements
        if (!this.achievements[1].unlocked && score >= 1000) {
            this.unlockAchievement('score_1000');
        }
        
        if (!this.achievements[2].unlocked && score >= 5000) {
            this.unlockAchievement('score_5000');
        }
        
        // Level achievement
        if (!this.achievements[3].unlocked && level >= 5) {
            this.unlockAchievement('level_5');
        }
        
        // Combo achievement
        if (!this.achievements[4].unlocked && consecutiveEats >= 10) {
            this.unlockAchievement('combo_10');
        }
        
        // Ghost hunter achievement
        if (!this.achievements[5].unlocked && this.ghostsEaten >= 20) {
            this.unlockAchievement('ghost_hunter');
        }
        
        // Fruit lover achievement
        if (!this.achievements[6].unlocked && this.fruitsCollected >= 10) {
            this.unlockAchievement('fruit_lover');
        }
    }

    // Unlock an achievement
    unlockAchievement(id) {
        const achievement = this.achievements.find(a => a.id === id);
        if (achievement && !achievement.unlocked) {
            achievement.unlocked = true;
            this.showAchievementNotification(achievement);
            console.log(`Достижение разблокировано: ${achievement.name}`);
            return achievement.points;
        }
        return 0;
    }

    // Show achievement notification
    showAchievementNotification(achievement) {
        // Создать элемент уведомления
        const notification = document.createElement('div');
        notification.className = 'achievement-notification';
        notification.innerHTML = `
            <div class="achievement-content">
                <h3>Новое достижение!</h3>
                <h4>${achievement.name}</h4>
                <p>${achievement.description}</p>
                <span>+${achievement.points} очков</span>
            </div>
        `;
        
        // Добавить стили для уведомления
        if (!document.getElementById('achievement-styles')) {
            const style = document.createElement('style');
            style.id = 'achievement-styles';
            style.textContent = `
                .achievement-notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: linear-gradient(135deg, #8A2BE2, #4B0082);
                    color: white;
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                    z-index: 1000;
                    animation: slideIn 0.5s, fadeOut 0.5s 4.5s forwards;
                    border: 2px solid #FFD700;
                    max-width: 300px;
                }
                
                .achievement-content h3 {
                    margin: 0 0 5px 0;
                    color: #FFD700;
                    font-size: 1.2em;
                }
                
                .achievement-content h4 {
                    margin: 0 0 5px 0;
                    font-size: 1.1em;
                }
                
                .achievement-content p {
                    margin: 0 0 10px 0;
                    font-size: 0.9em;
                }
                
                .achievement-content span {
                    font-weight: bold;
                    color: #00FF00;
                }
                
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                
                @keyframes fadeOut {
                    from { opacity: 1; }
                    to { opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
        
        document.body.appendChild(notification);
        
        // Удалить уведомление через 5 секунд
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }

    // Методы для увеличения счетчиков
    incrementGhostsEaten() {
        this.ghostsEaten++;
    }

    incrementFruitsCollected() {
        this.fruitsCollected++;
    }

    incrementLevelsCompletedWithoutDeath() {
        this.levelsCompletedWithoutDeath++;
    }

    // Метод для сброса счетчиков при начале нового уровня
    resetLevelCounters(lives) {
        this.currentLevelStartLives = lives;
    }

    // Метод для получения счетчиков
    getStats() {
        return {
            ghostsEaten: this.ghostsEaten,
            fruitsCollected: this.fruitsCollected,
            levelsCompletedWithoutDeath: this.levelsCompletedWithoutDeath
        };
    }

    // Метод для сброса всех достижений
    reset() {
        this.achievements.forEach(achievement => {
            achievement.unlocked = false;
        });
        this.ghostsEaten = 0;
        this.fruitsCollected = 0;
        this.levelsCompletedWithoutDeath = 0;
        this.currentLevelStartLives = 3;
    }
}

// Экспортируем класс для использования в других файлах
// В браузерной среде добавляем в глобальную область видимости
if (typeof window !== 'undefined') {
    window.AchievementManager = AchievementManager;
}

// Для Node.js или модульных систем
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AchievementManager;
}