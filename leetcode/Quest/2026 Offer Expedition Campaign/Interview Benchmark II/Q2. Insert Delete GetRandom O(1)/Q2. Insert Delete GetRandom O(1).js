/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
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

var RandomizedSet = function() {
    this.values = [];
    this.indexMap = new Map();
};

RandomizedSet.prototype.insert = function(val) {
    if (this.indexMap.has(val)) return false;
    this.indexMap.set(val, this.values.length);
    this.values.push(val);
    return true;
};

RandomizedSet.prototype.remove = function(val) {
    if (!this.indexMap.has(val)) return false;
    const idx = this.indexMap.get(val);
    const lastVal = this.values[this.values.length - 1];
    this.values[idx] = lastVal;
    this.indexMap.set(lastVal, idx);
    this.values.pop();
    this.indexMap.delete(val);
    return true;
};

RandomizedSet.prototype.getRandom = function() {
    const randomIndex = Math.floor(Math.random() * this.values.length);
    return this.values[randomIndex];
};