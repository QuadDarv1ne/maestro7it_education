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
 * function ListNode(val) {
 *     this.val = val;
 *     this.next = null;
 * }
 */
/**
 * Удаляет узел из односвязного списка без доступа к голове списка.
 * 
 * Алгоритм:
 * 1. Копирует значение следующего узла в текущий узел.
 * 2. Изменяет указатель текущего узла на узел через один.
 * 
 * Сложность:
 * Время: O(1)
 * Пространство: O(1)
 * 
 * @param {ListNode} node - Узел, который нужно удалить из списка
 * @return {void} Не возвращает значение, модифицирует список на месте
 * 
 * @example
 * // Исходный список: 4 -> 5 -> 1 -> 9
 * // Удаляем узел со значением 5
 * // Результат: 4 -> 1 -> 9
 * 
 * Примечание:
 * - Узел не является хвостовым (гарантируется, что node.next != null)
 * - В JavaScript не нужно явно освобождать память
 */
var deleteNode = function(node) {
    // Копируем значение следующего узла в текущий узел
    node.val = node.next.val;
    
    // Пропускаем следующий узел
    node.next = node.next.next;
};

/**
 * Альтернативная реализация с явным сохранением следующего узла.
 * 
 * @param {ListNode} node - Узел для удаления
 */
var deleteNodeAlternative = function(node) {
    // Проверяем, что узел не является null и не хвостовым
    if (!node || !node.next) {
        return;
    }
    
    // Получаем следующий узел
    const nextNode = node.next;
    
    // Копируем значение и указатель
    node.val = nextNode.val;
    node.next = nextNode.next;
    
    // Обнуляем ссылку для помощи сборщику мусора
    nextNode.next = null;
};