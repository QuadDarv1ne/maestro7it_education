/**
 * https://leetcode.com/problems/print-in-order/description/
 * Автор: Дуплей Максим Игоревич- AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "1114. Print in Order"
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
 * Задача 1114. Печать по порядку (Print in Order)
 *
 * Класс Foo управляет порядком вызова трёх функций из разных потоков.
 * Метод first() должен выполниться первым, second() — вторым, third() — третьим,
 * независимо от того, в каком порядке потоки вызывают эти методы.
 *
 * Решение использует цепочку Promise: first() разрешает первый промис,
 * second() ждёт его, затем разрешает второй, third() ждёт второй.
 */

class Foo {
    /**
     * Конструктор инициализирует два промиса и сохраняет функции resolve
     * для последующего ручного разрешения.
     */
    constructor() {
        this.promise1 = new Promise(resolve => { this.resolve1 = resolve; });
        this.promise2 = new Promise(resolve => { this.resolve2 = resolve; });
    }

    /**
     * Первый метод. Вызывает printFirst() и разрешает первый промис,
     * позволяя выполняться second().
     *
     * @param {function} printFirst - функция, выводящая "first"
     */
    async first(printFirst) {
        printFirst();
        this.resolve1();
    }

    /**
     * Второй метод. Ожидает разрешения первого промиса,
     * затем вызывает printSecond() и разрешает второй промис для third().
     *
     * @param {function} printSecond - функция, выводящая "second"
     */
    async second(printSecond) {
        await this.promise1;
        printSecond();
        this.resolve2();
    }

    /**
     * Третий метод. Ожидает разрешения второго промиса,
     * затем вызывает printThird().
     *
     * @param {function} printThird - функция, выводящая "third"
     */
    async third(printThird) {
        await this.promise2;
        printThird();
    }
}