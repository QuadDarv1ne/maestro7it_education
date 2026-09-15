/**
 * https://leetcode.com/problems/walking-robot-simulation-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Walking Robot Simulation II" на JavaScript
 * 
 * Алгоритм аналогичен C++ версии.
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

var Robot = function(width, height) {
    this.perimeter = 2 * (width + height) - 4;
    this.steps = 0;
    this.positions = [];
    this.directions = [];
    
    // East
    for (let x = 0; x < width; x++) {
        this.positions.push([x, 0]);
        this.directions.push("East");
    }
    // North
    for (let y = 1; y < height; y++) {
        this.positions.push([width - 1, y]);
        this.directions.push("North");
    }
    // West
    for (let x = width - 2; x >= 0; x--) {
        this.positions.push([x, height - 1]);
        this.directions.push("West");
    }
    // South
    for (let y = height - 2; y > 0; y--) {
        this.positions.push([0, y]);
        this.directions.push("South");
    }
};

Robot.prototype.step = function(num) {
    this.steps += num;
};

Robot.prototype.getPos = function() {
    if (this.perimeter === 0) return [0, 0];
    const idx = this.steps % this.perimeter;
    return this.positions[idx];
};

Robot.prototype.getDir = function() {
    if (this.perimeter === 0) return "East";
    const idx = this.steps % this.perimeter;
    if (this.steps > 0 && idx === 0) return "South";
    return this.directions[idx];
};