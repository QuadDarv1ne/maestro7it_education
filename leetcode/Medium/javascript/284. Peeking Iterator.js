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

/**
 * Класс PeekingIterator, который расширяет стандартный итератор методом peek().
 * 
 * Позволяет просматривать следующий элемент итерации без продвижения итератора.
 * 
 * Поля:
 *   iterator: Исходный итератор
 *   nextVal: Сохраненный следующий элемент
 *   hasNextVal: Флаг наличия следующего элемента
 * 
 * Методы:
 *   constructor(iterator): Конструктор, инициализирует итератор
 *   peek(): Возвращает следующий элемент без продвижения итератора
 *   next(): Возвращает следующий элемент и продвигает итератор
 *   hasNext(): Проверяет наличие следующего элемента
 * 
 * Исключения:
 *   Error: Вызывается при попытке peek() или next(), когда элементов нет
 * 
 * Пример использования:
 *   const nums = [1, 2, 3];
 *   const iterator = new Iterator(nums);
 *   const peekingIterator = new PeekingIterator(iterator);
 *   peekingIterator.peek();    // 1
 *   peekingIterator.next();    // 1
 *   peekingIterator.hasNext(); // true
 * 
 * Примечание:
 *   Iterator - абстрактный класс, предоставляемый LeetCode
 */

/**
 * // This is the Iterator's API interface.
 * // You should not implement it, or speculate about its implementation.
 * function Iterator() {
 *    @ return {number}
 *    this.next = function() { // return the next number of the iterator
 *       ...
 *    }; 
 *
 *    @return {boolean}
 *    this.hasNext = function() { // return true if it still has numbers
 *       ...
 *    };
 * };
 */

/**
 * @param {Iterator} iterator
 */
var PeekingIterator = function(iterator) {
    this.iterator = iterator;
    this.nextVal = null;
    this.hasNextVal = false;
    
    if (this.iterator.hasNext()) {
        this.nextVal = this.iterator.next();
        this.hasNextVal = true;
    }
};

/**
 * @return {number}
 */
PeekingIterator.prototype.peek = function() {
    if (!this.hasNextVal) {
        throw new Error("No more elements");
    }
    return this.nextVal;
};

/**
 * @return {number}
 */
PeekingIterator.prototype.next = function() {
    if (!this.hasNextVal) {
        throw new Error("No more elements");
    }
    
    const current = this.nextVal;
    if (this.iterator.hasNext()) {
        this.nextVal = this.iterator.next();
        this.hasNextVal = true;
    } else {
        this.nextVal = null;
        this.hasNextVal = false;
    }
    
    return current;
};

/**
 * @return {boolean}
 */
PeekingIterator.prototype.hasNext = function() {
    return this.hasNextVal;
};