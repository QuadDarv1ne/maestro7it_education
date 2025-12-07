/**
 * @param {ListNode} head
 * @param {number} k
 * @return {ListNode}
 */
var rotateRight = function(head, k) {
    /**
     * Автор: Дуплей Максим Игоревич
     * ORCID: https://orcid.org/0009-0007-7605-539X
     * GitHub: https://github.com/QuadDarv1ne/
     * 
     * Задача: Rotate List (LeetCode)
     * Алгоритм: Вращение связного списка вправо на k позиций
     * Сложность: O(n) по времени, O(1) по памяти
     * 
     * Идея решения:
     * 1. Находим длину списка и последний узел
     * 2. Нормализуем k через модуль (k % length)
     * 3. Находим новый хвост на позиции (length - k - 1)
     * 4. Переподключаем узлы: новая голова, разрыв и соединение
     */
    
    // Обработка граничных случаев
    if (!head || !head.next || k === 0) {
        return head;
    }
    
    // Шаг 1: Найти длину списка и последний узел
    let length = 1;
    let last = head;
    while (last.next) {
        last = last.next;
        length++;
    }
    
    // Шаг 2: Нормализовать k (обработать случай k > length)
    k = k % length;
    if (k === 0) {
        return head; // Вращение не требуется
    }
    
    // Шаг 3: Найти новый хвост (на позиции length - k - 1)
    let newTail = head;
    for (let i = 0; i < length - k - 1; i++) {
        newTail = newTail.next;
    }
    
    // Шаг 4: Установить новую голову и переподключить
    let newHead = newTail.next;
    newTail.next = null;      // Разорвать связь
    last.next = head;         // Соединить старый хвост со старой головой
    
    return newHead;
};

/*
 * Полезные ссылки автора:
 * Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * Telegram: @quadd4rv1n7, @dupley_maxim_1999
 * Rutube: https://rutube.ru/channel/4218729/
 * Plvideo: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * YouTube: https://www.youtube.com/@it-coders
 * VK: https://vk.com/science_geeks
 */