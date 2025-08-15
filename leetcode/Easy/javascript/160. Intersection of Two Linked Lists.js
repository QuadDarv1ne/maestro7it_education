/**
 * https://leetcode.com/problems/intersection-of-two-linked-lists/description/
 */

/**
 * Находит узел пересечения двух односвязных списков.
 * Если пересечения нет, возвращает null.
 * Алгоритм:
 * 1. Определяем длину списков
 * 2. Выравниваем указатели
 * 3. Двигаем указатели одновременно до пересечения
 * Время: O(A + B), Память: O(1)
 * @param {ListNode} headA — голова первого списка
 * @param {ListNode} headB — голова второго списка
 * @return {ListNode|null} — узел пересечения или null
 */
var getIntersectionNode = function(headA, headB) {
    if (!headA || !headB) return null;

    let currA = headA, currB = headB;
    let lenA = 0, lenB = 0;

    while (currA) { lenA++; currA = currA.next; }
    while (currB) { lenB++; currB = currB.next; }

    currA = headA;
    currB = headB;

    if (lenA > lenB) {
        for (let i = 0; i < lenA - lenB; i++) currA = currA.next;
    } else {
        for (let i = 0; i < lenB - lenA; i++) currB = currB.next;
    }

    while (currA && currB) {
        if (currA === currB) return currA;
        currA = currA.next;
        currB = currB.next;
    }

    return null;
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/