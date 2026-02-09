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
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
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
     * @param node Узел, который нужно удалить из списка
     * 
     * Пример:
     * Исходный список: 4 -> 5 -> 1 -> 9
     * Удаляем узел со значением 5
     * Результат: 4 -> 1 -> 9
     * 
     * Примечание:
     * - Узел не является хвостовым (гарантируется, что node->next != nullptr)
     * - В C++ можно было бы освободить память, но в задаче это не требуется
     */
    void deleteNode(ListNode* node) {
        // Копируем значение следующего узла в текущий узел
        node->val = node->next->val;
        
        // Пропускаем следующий узел
        ListNode* toDelete = node->next;
        node->next = node->next->next;
        
        // В условиях LeetCode обычно не требуется освобождать память,
        // но в реальном коде нужно:
        // delete toDelete;
    }
    
    /**
     * Более безопасная версия с проверками.
     * 
     * @param node Узел для удаления
     */
    void deleteNodeSafe(ListNode* node) {
        // Проверяем, что узел не является nullptr и не хвостовым
        if (node == nullptr || node->next == nullptr) {
            return; // Нельзя удалить
        }
        
        // Копируем данные следующего узла
        ListNode* nextNode = node->next;
        node->val = nextNode->val;
        node->next = nextNode->next;
        
        // Освобождаем память следующего узла
        delete nextNode;
    }
};