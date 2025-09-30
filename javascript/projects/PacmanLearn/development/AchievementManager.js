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
            { id: 'survivor', name: 'Выживший', description: 'Пройти уровень без потери жизни', unlocked: false, points: 700 },
            { id: 'speed_demon', name: 'Скоростной демон', description: 'Завершить уровень за 30 секунд', unlocked: false, points: 800 },
            { id: 'perfectionist', name: 'Перфекционист', description: 'Собрать всю еду на уровне', unlocked: false, points: 1000 },
            // New achievements
            { id: 'ghost_buster', name: 'Призракобой', description: 'Съесть 50 привидений', unlocked: false, points: 1200 },
            { id: 'fruit_expert', name: 'Эксперт по фруктам', description: 'Собрать 25 фруктов', unlocked: false, points: 1000 },
            { id: 'combo_king', name: 'Король комбо', description: 'Собрать 20 комбо', unlocked: false, points: 1500 },
            { id: 'level_master', name: 'Мастер уровней', description: 'Достичь 10 уровня', unlocked: false, points: 2000 },
            { id: 'pacman_legend', name: 'Легенда Pacman', description: 'Набрать 10000 очков', unlocked: false, points: 3000 },
            { id: 'ghost_haunter', name: 'Преследователь призраков', description: 'Съесть 5 привидений за одну жизнь', unlocked: false, points: 1000 },
            { id: 'speedrunner', name: 'Спидраннер', description: 'Завершить уровень за 15 секунд', unlocked: false, points: 1500 },
            { id: 'collector', name: 'Коллекционер', description: 'Собрать все типы фруктов', unlocked: false, points: 800 }
        ];

        this.ghostsEaten = 0;
        this.fruitsCollected = 0;
        this.levelsCompletedWithoutDeath = 0;
        this.currentLevelStartLives = 3;
        this.levelStartTime = 0; // Track level start time
        this.foodEaten = 0; // Track food eaten in current level
        this.totalFoodInLevel = 0; // Track total food in current level
        
        // New tracking variables
        this.ghostsEatenInCurrentLife = 0;
        this.collectedFruitTypes = new Set(); // Track unique fruit types collected
        this.lastLevelCompletedTime = 0;
        this.achievementsUnlockedThisSession = 0;
        
        // Pre-allocate objects for performance
        this.tempStats = {
            ghostsEaten: 0,
            fruitsCollected: 0,
            levelsCompletedWithoutDeath: 0,
            achievementsUnlocked: 0,
            achievementsUnlockedThisSession: 0,
            uniqueFruitTypesCollected: 0
        };
        
        this.tempProgress = {
            unlocked: 0,
            total: 0,
            percentage: 0
        };
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
        
        // New high score achievement
        if (!this.achievements.find(a => a.id === 'pacman_legend').unlocked && score >= 10000) {
            this.unlockAchievement('pacman_legend');
        }
        
        // Level achievement
        if (!this.achievements[3].unlocked && level >= 5) {
            this.unlockAchievement('level_5');
        }
        
        // New level achievement
        const levelMaster = this.achievements.find(a => a.id === 'level_master');
        if (levelMaster && !levelMaster.unlocked && level >= 10) {
            this.unlockAchievement('level_master');
        }
        
        // Combo achievement
        if (!this.achievements[4].unlocked && consecutiveEats >= 10) {
            this.unlockAchievement('combo_10');
        }
        
        // New combo achievement
        const comboKing = this.achievements.find(a => a.id === 'combo_king');
        if (comboKing && !comboKing.unlocked && consecutiveEats >= 20) {
            this.unlockAchievement('combo_king');
        }
        
        // Ghost hunter achievement
        if (!this.achievements[5].unlocked && this.ghostsEaten >= 20) {
            this.unlockAchievement('ghost_hunter');
        }
        
        // New ghost achievements
        const ghostBuster = this.achievements.find(a => a.id === 'ghost_buster');
        if (ghostBuster && !ghostBuster.unlocked && this.ghostsEaten >= 50) {
            this.unlockAchievement('ghost_buster');
        }
        
        const ghostHaunter = this.achievements.find(a => a.id === 'ghost_haunter');
        if (ghostHaunter && !ghostHaunter.unlocked && this.ghostsEatenInCurrentLife >= 5) {
            this.unlockAchievement('ghost_haunter');
        }
        
        // Fruit lover achievement
        if (!this.achievements[6].unlocked && this.fruitsCollected >= 10) {
            this.unlockAchievement('fruit_lover');
        }
        
        // New fruit achievements
        const fruitExpert = this.achievements.find(a => a.id === 'fruit_expert');
        if (fruitExpert && !fruitExpert.unlocked && this.fruitsCollected >= 25) {
            this.unlockAchievement('fruit_expert');
        }
        
        const collector = this.achievements.find(a => a.id === 'collector');
        if (collector && !collector.unlocked && this.collectedFruitTypes.size >= 10) {
            this.unlockAchievement('collector');
        }
        
        // Survivor achievement - check if level was completed without losing lives
        const survivor = this.achievements.find(a => a.id === 'survivor');
        if (survivor && !survivor.unlocked && 
            this.currentLevelStartLives === 3 && this.levelsCompletedWithoutDeath > 0) {
            this.unlockAchievement('survivor');
        }
        
        // Speed demon achievement - check if level was completed quickly
        if (this.levelStartTime > 0) {
            const timeToComplete = (Date.now() - this.levelStartTime) / 1000; // in seconds
            const speedDemon = this.achievements.find(a => a.id === 'speed_demon');
            if (speedDemon && !speedDemon.unlocked && timeToComplete <= 30) {
                this.unlockAchievement('speed_demon');
            }
            
            // New speedrunner achievement
            const speedrunner = this.achievements.find(a => a.id === 'speedrunner');
            if (speedrunner && !speedrunner.unlocked && timeToComplete <= 15) {
                this.unlockAchievement('speedrunner');
            }
        }
        
        // Perfectionist achievement - check if all food was eaten
        const perfectionist = this.achievements.find(a => a.id === 'perfectionist');
        if (perfectionist && !perfectionist.unlocked && 
            this.totalFoodInLevel > 0 && this.foodEaten >= this.totalFoodInLevel) {
            this.unlockAchievement('perfectionist');
        }
    }

    // Unlock an achievement
    unlockAchievement(id) {
        const achievement = this.achievements.find(a => a.id === id);
        if (achievement && !achievement.unlocked) {
            achievement.unlocked = true;
            this.achievementsUnlockedThisSession++;
            this.showAchievementNotification(achievement);
            this.playAchievementSound();
            console.log(`Достижение разблокировано: ${achievement.name}`);
            return achievement.points;
        }
        return 0;
    }

    // Play sound when achievement is unlocked
    playAchievementSound() {
        // This would integrate with the SoundManager
        console.log('Achievement unlocked sound played');
    }

    // Show achievement notification
    showAchievementNotification(achievement) {
        // Create element only if DOM is available
        if (typeof document === 'undefined') return;
        
        // Создать элемент уведомления
        const notification = document.createElement('div');
        notification.className = 'achievement-notification';
        
        // Add special styling for rare achievements
        let specialClass = '';
        if (achievement.points >= 2000) {
            specialClass = ' rare-achievement';
        } else if (achievement.points >= 1000) {
            specialClass = ' epic-achievement';
        }
        
        notification.innerHTML = `
            <div class="achievement-content${specialClass}">
                <h3>Новое достижение!</h3>
                <h4>${achievement.name}</h4>
                <p>${achievement.description}</p>
                <span>+${achievement.points} очков</span>
                <div class="achievement-badge" data-points="${achievement.points}"></div>
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
                    backdrop-filter: blur(5px);
                }
                
                .achievement-notification.rare {
                    background: linear-gradient(135deg, #FF8C00, #FF4500);
                    border: 2px solid #FFD700;
                    box-shadow: 0 0 20px #FF4500;
                }
                
                .achievement-notification.epic {
                    background: linear-gradient(135deg, #00BFFF, #1E90FF);
                    border: 2px solid #00FFFF;
                    box-shadow: 0 0 20px #00BFFF;
                }
                
                .achievement-content h3 {
                    margin: 0 0 5px 0;
                    color: #FFD700;
                    font-size: 1.2em;
                    text-align: center;
                }
                
                .achievement-content.rare-achievement h3 {
                    color: #FFA500;
                    text-shadow: 0 0 5px #FF4500;
                }
                
                .achievement-content.epic-achievement h3 {
                    color: #00FFFF;
                    text-shadow: 0 0 5px #00BFFF;
                }
                
                .achievement-content h4 {
                    margin: 0 0 5px 0;
                    font-size: 1.1em;
                    text-align: center;
                }
                
                .achievement-content p {
                    margin: 0 0 10px 0;
                    font-size: 0.9em;
                    text-align: center;
                }
                
                .achievement-content span {
                    font-weight: bold;
                    color: #00FF00;
                    display: block;
                    text-align: center;
                }
                
                .achievement-badge {
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    background: radial-gradient(circle, #FFD700, #D4AF37);
                    margin: 10px auto 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    font-size: 12px;
                    color: #000;
                }
                
                .achievement-badge[data-points="100"] { background: radial-gradient(circle, #C0C0C0, #A9A9A9); }
                .achievement-badge[data-points="200"] { background: radial-gradient(circle, #C0C0C0, #A9A9A9); }
                .achievement-badge[data-points="300"] { background: radial-gradient(circle, #C0C0C0, #A9A9A9); }
                .achievement-badge[data-points="350"] { background: radial-gradient(circle, #C0C0C0, #A9A9A9); }
                .achievement-badge[data-points="400"] { background: radial-gradient(circle, #CD7F32, #A0522D); } /* Bronze */
                .achievement-badge[data-points="500"] { background: radial-gradient(circle, #CD7F32, #A0522D); } /* Bronze */
                .achievement-badge[data-points="600"] { background: radial-gradient(circle, #C0C0C0, #A9A9A9); } /* Silver */
                .achievement-badge[data-points="700"] { background: radial-gradient(circle, #C0C0C0, #A9A9A9); } /* Silver */
                .achievement-badge[data-points="800"] { background: radial-gradient(circle, #FFD700, #D4AF37); } /* Gold */
                .achievement-badge[data-points="1000"] { background: radial-gradient(circle, #FFD700, #D4AF37); } /* Gold */
                .achievement-badge[data-points="1200"] { background: radial-gradient(circle, #00BFFF, #1E90FF); } /* Epic Blue */
                .achievement-badge[data-points="1500"] { background: radial-gradient(circle, #00BFFF, #1E90FF); } /* Epic Blue */
                .achievement-badge[data-points="2000"] { background: radial-gradient(circle, #FF8C00, #FF4500); } /* Rare Orange/Red */
                .achievement-badge[data-points="3000"] { background: radial-gradient(circle, #FF8C00, #FF4500); } /* Rare Orange/Red */
                
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                
                @keyframes fadeOut {
                    from { opacity: 1; }
                    to { opacity: 0; }
                }
                
                @keyframes pulse {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                    100% { transform: scale(1); }
                }
                
                .achievement-content.rare-achievement,
                .achievement-content.epic-achievement {
                    animation: pulse 1s infinite;
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
        this.ghostsEatenInCurrentLife++;
    }

    incrementFruitsCollected(fruitType = null) {
        this.fruitsCollected++;
        if (fruitType) {
            this.collectedFruitTypes.add(fruitType);
        }
    }

    incrementLevelsCompletedWithoutDeath() {
        this.levelsCompletedWithoutDeath++;
    }

    // Reset ghosts eaten in current life (called when player dies)
    resetGhostsEatenInCurrentLife() {
        this.ghostsEatenInCurrentLife = 0;
    }

    // New methods for tracking level progress
    setLevelStartTime() {
        this.levelStartTime = Date.now();
    }

    setLevelFoodCount(totalFood) {
        this.totalFoodInLevel = totalFood;
        this.foodEaten = 0;
    }

    incrementFoodEaten() {
        this.foodEaten++;
    }

    // Called when level is completed
    onLevelCompleted() {
        this.lastLevelCompletedTime = Date.now();
        // Check if player completed level without losing lives
        if (this.currentLevelStartLives === 3) {
            this.levelsCompletedWithoutDeath++;
        }
    }

    // Called when player loses a life
    onLifeLost() {
        this.currentLevelStartLives--;
        this.resetGhostsEatenInCurrentLife();
    }

    // Метод для получения счетчиков
    getStats() {
        // Reuse pre-allocated object to reduce garbage collection
        this.tempStats.ghostsEaten = this.ghostsEaten;
        this.tempStats.fruitsCollected = this.fruitsCollected;
        this.tempStats.levelsCompletedWithoutDeath = this.levelsCompletedWithoutDeath;
        this.tempStats.achievementsUnlocked = this.achievements.filter(a => a.unlocked).length;
        this.tempStats.achievementsUnlockedThisSession = this.achievementsUnlockedThisSession;
        this.tempStats.uniqueFruitTypesCollected = this.collectedFruitTypes.size;
        return this.tempStats;
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
        this.levelStartTime = 0;
        this.foodEaten = 0;
        this.totalFoodInLevel = 0;
        this.ghostsEatenInCurrentLife = 0;
        this.collectedFruitTypes.clear();
        this.lastLevelCompletedTime = 0;
        this.achievementsUnlockedThisSession = 0;
    }
    
    // Get unlocked achievements
    getUnlockedAchievements() {
        return this.achievements.filter(a => a.unlocked);
    }
    
    // Get locked achievements
    getLockedAchievements() {
        return this.achievements.filter(a => !a.unlocked);
    }
    
    // Get achievement progress
    getAchievementProgress() {
        const unlocked = this.achievements.filter(a => a.unlocked).length;
        const total = this.achievements.length;
        // Reuse pre-allocated object to reduce garbage collection
        this.tempProgress.unlocked = unlocked;
        this.tempProgress.total = total;
        this.tempProgress.percentage = Math.round((unlocked / total) * 100);
        return this.tempProgress;
    }
}

// Экспортируем класс для использования в других файлах
export { AchievementManager };