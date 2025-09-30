// Game constants

// Cell types
export const CELL_TYPES = {
    WALL: 0,
    PATH: 1,
    FOOD: 2,
    SUPER_FOOD: 3
};

// Directions
export const DIRECTIONS = {
    UP: 'up',
    DOWN: 'down',
    LEFT: 'left',
    RIGHT: 'right'
};

// Ghost states
export const GHOST_STATES = {
    CHASE: 'chase',
    SCATTER: 'scatter',
    FRIGHTENED: 'frightened'
};

// Particle types
export const PARTICLE_TYPES = {
    DEFAULT: 'default',
    GLOW: 'glow',
    SPARKLE: 'sparkle',
    SMOKE: 'smoke',
    EXPLOSION: 'explosion'
};

// Achievement IDs
export const ACHIEVEMENT_IDS = {
    FIRST_GAME: 'first_game',
    SCORE_1000: 'score_1000',
    SCORE_5000: 'score_5000',
    LEVEL_5: 'level_5',
    COMBO_10: 'combo_10',
    GHOST_HUNTER: 'ghost_hunter',
    FRUIT_LOVER: 'fruit_lover',
    SURVIVOR: 'survivor',
    SPEED_DEMON: 'speed_demon',
    PERFECTIONIST: 'perfectionist',
    GHOST_BUSTER: 'ghost_buster',
    FRUIT_EXPERT: 'fruit_expert',
    COMBO_KING: 'combo_king',
    LEVEL_MASTER: 'level_master',
    PACMAN_LEGEND: 'pacman_legend',
    GHOST_HAUNTER: 'ghost_haunter',
    SPEEDRUNNER: 'speedrunner',
    COLLECTOR: 'collector'
};

// Fruit rarities
export const FRUIT_RARITIES = {
    COMMON: 'common',
    UNCOMMON: 'uncommon',
    RARE: 'rare',
    EPIC: 'epic',
    LEGENDARY: 'legendary'
};

// Rarity bonuses
export const RARITY_BONUSES = {
    [FRUIT_RARITIES.COMMON]: 1,
    [FRUIT_RARITIES.UNCOMMON]: 1.2,
    [FRUIT_RARITIES.RARE]: 1.5,
    [FRUIT_RARITIES.EPIC]: 2.0,
    [FRUIT_RARITIES.LEGENDARY]: 3.0
};

// Game settings
export const GAME_SETTINGS = {
    DEFAULT_CELL_SIZE: 22,
    DEFAULT_UPDATE_INTERVAL: 150,
    MIN_UPDATE_INTERVAL: 50,
    MAX_UPDATE_INTERVAL: 300,
    DEFAULT_PACMAN_SPEED: 2.5,
    DEFAULT_GHOST_SPEED: 0.8,
    POWER_MODE_DURATION: 10000,
    FRUIT_SPAWN_CHANCE: 0.005,
    COMBO_TIME_WINDOW: 2000,
    COMBO_MIN_COUNT: 3
};

// Collision settings
export const COLLISION_SETTINGS = {
    PACMAN_RADIUS: 8,
    GHOST_RADIUS: 8
};

// UI constants
export const UI_CONSTANTS = {
    MAX_HIGH_SCORES: 10
};