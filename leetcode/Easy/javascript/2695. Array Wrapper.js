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

/**
 * @param {number[]} nums
 * @return {void}
 */
class ArrayWrapper {
    constructor(nums) {
        this.nums = nums;
    }

    /**
     * @return {number}
     */
    valueOf() {
        // Этот метод вызывается JavaScript при попытке преобразовать объект в примитив,
        // например, при использовании оператора +.
        // Возвращаем сумму всех элементов массива.
        return this.nums.reduce((sum, num) => sum + num, 0);
    }

    /**
     * @return {string}
     */
    toString() {
        // Этот метод вызывается при преобразовании объекта в строку,
        // например, при вызове String(instance) или при конкатенации со строкой.
        // Возвращаем строковое представление массива в нужном формате.
        return `[${this.nums.join(',')}]`;
    }
}