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
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * Проверяет, является ли односвязный список палиндромом.
 * 
 * Алгоритм:
 * 1. Находит середину списка с помощью быстрого и медленного указателей.
 * 2. Разворачивает вторую половину списка.
 * 3. Сравнивает первую и развернутую вторую половины.
 * 4. Восстанавливает исходный список.
 * 
 * Сложность:
 * Время: O(n)
 * Пространство: O(1)
 * 
 * @param {ListNode} head - Голова односвязного списка
 * @return {boolean} true, если список является палиндромом, иначе false
 * 
 * @example
 * // Вход: 1->2->2->1
 * // Выход: true
 * // Вход: 1->2
 * // Выход: false
 */
var isPalindrome = function(head) {
    if (!head || !head.next) {
        return true;
    }
    
    // Шаг 1: Находим середину списка
    let slow = head;
    let fast = head;
    
    while (fast && fast.next) {
        slow = slow.next;
        fast = fast.next.next;
    }
    
    // Шаг 2: Разворачиваем вторую половину
    let secondHalf = reverseList(slow);
    let secondHalfCopy = secondHalf; // Для восстановления
    
    // Шаг 3: Сравниваем две половины
    let firstHalf = head;
    let result = true;
    
    while (secondHalf) {
        if (firstHalf.val !== secondHalf.val) {
            result = false;
            break;
        }
        firstHalf = firstHalf.next;
        secondHalf = secondHalf.next;
    }
    
    // Шаг 4: Восстанавливаем исходный список
    reverseList(secondHalfCopy);
    
    return result;
};

/**
 * Разворачивает односвязный список.
 * 
 * @param {ListNode} head - Голова списка для разворота
 * @return {ListNode} Голова развернутого списка
 */
function reverseList(head) {
    let prev = null;
    let current = head;
    
    while (current) {
        let nextNode = current.next;
        current.next = prev;
        prev = current;
        current = nextNode;
    }
    
    return prev;
}

/**
 * Альтернативное решение с использованием массива.
 * Проще, но использует O(n) дополнительной памяти.
 * 
 * @param {ListNode} head - Голова списка
 * @return {boolean} true, если список является палиндромом
 */
var isPalindromeWithArray = function(head) {
    const values = [];
    let current = head;
    
    // Собираем значения в массив
    while (current) {
        values.push(current.val);
        current = current.next;
    }
    
    // Проверяем, является ли массив палиндромом
    let left = 0, right = values.length - 1;
    while (left < right) {
        if (values[left] !== values[right]) {
            return false;
        }
        left++;
        right--;
    }
    
    return true;
};