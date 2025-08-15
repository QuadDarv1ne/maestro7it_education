/**
 * https://leetcode.com/problems/intersection-of-two-linked-lists/description/
 */

/**
 * Находит узел пересечения двух односвязных списков.
 * Если пересечения нет, возвращает null.
 *
 * Алгоритм:
 * 1. Определяем длину списков
 * 2. Выравниваем указатели
 * 3. Двигаем указатели одновременно до пересечения
 * Время: O(A + B), Память: O(1)
 */
class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        if (headA == null || headB == null) return null;

        ListNode currA = headA, currB = headB;
        int lenA = 0, lenB = 0;

        while (currA != null) { lenA++; currA = currA.next; }
        while (currB != null) { lenB++; currB = currB.next; }

        currA = headA;
        currB = headB;
        if (lenA > lenB) {
            for (int i = 0; i < lenA - lenB; i++) currA = currA.next;
        } else {
            for (int i = 0; i < lenB - lenA; i++) currB = currB.next;
        }

        while (currA != null && currB != null) {
            if (currA == currB) return currA;
            currA = currA.next;
            currB = currB.next;
        }

        return null;
    }
}

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