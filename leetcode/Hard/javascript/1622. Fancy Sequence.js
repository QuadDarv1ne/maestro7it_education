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

var Fancy = function() {
    /**
     * Конструктор. Инициализирует пустую последовательность.
     * Устанавливает начальные значения: mul = 1, add = 0.
     */
    this.seq = [];
    this.mul = 1n;
    this.add = 0n;
    this.MOD = 1000000007n;
};

// Вспомогательная функция: быстрое возведение в степень (BigInt)
function modPow(a, b, mod) {
    let res = 1n;
    a %= mod;
    while (b > 0) {
        if (b & 1n) res = (res * a) % mod;
        a = (a * a) % mod;
        b >>= 1n;
    }
    return res;
}

/**
 * Добавляет число val в конец последовательности.
 * Сохраняет "сырое" значение, скорректированное с учётом текущих mul и add.
 * @param {number} val целое число для добавления
 */
Fancy.prototype.append = function(val) {
    let bigVal = BigInt(val);
    // raw = (val - add) * inv(mul) mod MOD
    let raw = (bigVal - this.add + this.MOD) % this.MOD;
    let invMul = modPow(this.mul, this.MOD - 2n, this.MOD);
    raw = (raw * invMul) % this.MOD;
    this.seq.push(raw);
};

/**
 * Увеличивает все существующие значения в последовательности на inc.
 * Обновляет только глобальную переменную add.
 * @param {number} inc число, на которое увеличиваются все элементы
 */
Fancy.prototype.addAll = function(inc) {
    this.add = (this.add + BigInt(inc)) % this.MOD;
};

/**
 * Умножает все существующие значения в последовательности на m.
 * Обновляет глобальные переменные mul и add.
 * @param {number} m множитель для всех элементов
 */
Fancy.prototype.multAll = function(m) {
    this.mul = (this.mul * BigInt(m)) % this.MOD;
    this.add = (this.add * BigInt(m)) % this.MOD;
};

/**
 * Возвращает текущее значение элемента по индексу idx (0-базовый).
 * Вычисляется как seq[idx] * mul + add по модулю MOD.
 * Если индекс вне диапазона, возвращает -1.
 * @param {number} idx индекс запрашиваемого элемента
 * @returns {number} значение элемента или -1
 */
Fancy.prototype.getIndex = function(idx) {
    if (idx >= this.seq.length) return -1;
    let val = (this.seq[idx] * this.mul + this.add) % this.MOD;
    return Number(val);
};