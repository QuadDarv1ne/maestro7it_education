/**
 * @class Solution
 * @brief Класс, содержащий метод для слияния k отсортированных связных списков.
 */

#include <vector>
#include <queue>
using namespace std;

/**
     * @brief Объединяет k отсортированных связных списков в один отсортированный список.
     * 
     * @details Использует минимальную кучу (приоритетную очередь) для эффективного
     * извлечения узлов с минимальными значениями. Алгоритм:
     * 1. Помещает головы всех непустых списков в приоритетную очередь
     * 2. Последовательно извлекает минимальный элемент из очереди
     * 3. Добавляет следующий узел из того же списка (если существует)
     * 4. Строит результирующий список с помощью фиктивной головы
     * 
     * @note Для сравнения узлов используется кастомный компаратор:
     * [](const ListNode* a, const ListNode* b) { return a->val > b->val; }
     * 
     * @complexity Временная сложность: O(N log K), где:
     *   - N = общее количество узлов во всех списках
     *   - K = количество связных списков
     * @complexity Пространственная сложность: O(K)
     * 
     * @param lists Вектор указателей на головы связных списков.
     *              Списки отсортированы в порядке возрастания.
     *              Может содержать nullptr для пустых списков.
     * 
     * @return Указатель на голову объединенного отсортированного списка.
     *         Возвращает nullptr если все списки пусты.
     * 
     * @example Пример вызова:
     * \code
     *   ListNode* list1 = new ListNode(1, new ListNode(4, new ListNode(5)));
     *   ListNode* list2 = new ListNode(1, new ListNode(3, new ListNode(4)));
     *   ListNode* list3 = new ListNode(2, new ListNode(6));
     *   vector<ListNode*> lists = {list1, list2, list3};
     *   Solution sol;
     *   ListNode* result = sol.mergeKLists(lists);
     *   // Результат: 1->1->2->3->4->4->5->6
     * \endcode
     * 
     * @see Структура ListNode определена как:
     * \code
     *   struct ListNode {
     *       int val;
     *       ListNode *next;
     *       ListNode() : val(0), next(nullptr) {}
     *       ListNode(int x) : val(x), next(nullptr) {}
     *       ListNode(int x, ListNode *next) : val(x), next(next) {}
     *   };
     * \endcode
     */
    
struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        // Компаратор для мини-кучи: сравниваем значения узлов
        auto cmp = [](const ListNode* a, const ListNode* b) {
            return a->val > b->val;
        };
        priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> min_heap(cmp);
        
        // Добавляем головы непустых списков в кучу
        for (ListNode* node : lists) {
            if (node != nullptr) {
                min_heap.push(node);
            }
        }
        
        // Фиктивная голова для удобства построения результата
        ListNode dummy(0);
        ListNode* current = &dummy;
        
        while (!min_heap.empty()) {
            // Извлекаем минимальный узел
            ListNode* min_node = min_heap.top();
            min_heap.pop();
            
            // Присоединяем его к результирующему списку
            current->next = min_node;
            current = current->next;
            
            // Если есть следующий узел, добавляем его в кучу
            if (min_node->next != nullptr) {
                min_heap.push(min_node->next);
            }
        }
        
        return dummy.next;
    }
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
