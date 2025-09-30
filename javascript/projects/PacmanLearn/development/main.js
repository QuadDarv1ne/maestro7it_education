// Main module that imports all game components
import { Pacman } from './Pacman.js';
import { Ghost } from './Ghost.js';
import { GameMap } from './GameMap.js';
import { SoundManager } from './SoundManager.js';
import { ParticleManager } from './ParticleManager.js';
import { FruitManager } from './FruitManager.js';
import { AchievementManager } from './AchievementManager.js';
import { PacmanGame } from './PacmanGame.js';

// Export all classes for potential use by other modules
export {
    Pacman,
    Ghost,
    GameMap,
    SoundManager,
    ParticleManager,
    FruitManager,
    AchievementManager,
    PacmanGame
};

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const game = new PacmanGame();
    console.log("Игра загружена");
    
    // Make game globally available for button handlers in HTML
    window.game = game;
});