/**
 * https://leetcode.com/problems/house-robber-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "2619. Array Prototype Last"
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

class Calculator {
    /**
     * @param {number} value - Начальное значение
     */
    constructor(value) {
        this.result = value;
    }

    /**
     * Добавляет число к результату.
     * @param {number} value
     * @return {Calculator}
     */
    add(value) {
        this.result += value;
        return this; // Возвращаем текущий экземпляр для цепочки вызовов
    }

    /**
     * Вычитает число из результата.
     * @param {number} value
     * @return {Calculator}
     */
    subtract(value) {
        this.result -= value;
        return this;
    }

    /**
     * Умножает результат на число.
     * @param {number} value
     * @return {Calculator}
     */
    multiply(value) {
        this.result *= value;
        return this;
    }

    /**
     * Делит результат на число.
     * @param {number} value
     * @return {Calculator}
     * @throws {Error} При делении на 0.
     */
    divide(value) {
        if (value === 0) {
            throw new Error("Division by zero is not allowed");
        }
        this.result /= value;
        return this;
    }

    /**
     * Возводит результат в степень.
     * @param {number} value
     * @return {Calculator}
     */
    power(value) {
        this.result **= value;
        return this;
    }

    /**
     * Возвращает текущий результат.
     * @return {number}
     */
    getResult() {
        return this.result;
    }
}