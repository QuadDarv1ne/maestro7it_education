/**
 * [ Итеративная сортировка слиянием для связного списка ]
 * Для решения задачи сортировки связного списка с временной сложностью O(n log n) и константной памятью O(1) используется итеративный подход (bottom-up merge sort).
 * Алгоритм разбивает список на блоки экспоненциально увеличивающегося размера, попарно сливает их и формирует отсортированный список.
 */

/**
 * Определение узла связного списка.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    /**
     * Сортирует связный список в порядке возрастания.
     * 
     * Алгоритм:
     * 1. Подсчитывается длина списка.
     * 2. Используется фиктивный узел (dummy) для упрощения обработки.
     * 3. Внешний цикл увеличивает размер блока (step) от 1 до n/2:
     *    - Начинаем с блоков размером 1
     *    - На каждом шаге удваиваем размер блоков
     * 4. Внутренний цикл обрабатывает список блоками:
     *    - Разделяет список на блоки текущего размера
     *    - Попарно сливает соседние блоки
     *    - Соединяет отсортированные блоки в новый список
     * 5. Процесс повторяется до полной сортировки списка.
     * 
     * Сложность:
     * - Время: O(n log n)
     * - Память: O(1)
     * 
     * @param head Указатель на голову списка
     * @return Указатель на голову отсортированного списка
     */
    ListNode* sortList(ListNode* head) {
        if (!head || !head->next) return head;
        
        // Подсчет длины списка
        int n = 0;
        ListNode* node = head;
        while (node) {
            n++;
            node = node->next;
        }
        
        ListNode dummy(0);
        dummy.next = head;
        
        // Основной цикл: размер блока step = 1, 2, 4, 8...
        for (int step = 1; step < n; step <<= 1) {
            ListNode* prev = &dummy;
            ListNode* curr = dummy.next;
            
            // Обработка всех блоков текущего размера
            while (curr) {
                // Получаем левый блок
                ListNode* left = curr;
                // Отрезаем правый блок и получаем начало следующего блока
                ListNode* right = split(left, step);
                // Обновляем curr на следующий блок
                curr = split(right, step);
                
                // Сливаем два блока
                ListNode* merged = merge(left, right);
                // Присоединяем слитый блок к результату
                prev->next = merged;
                
                // Перемещаем prev в конец слитого блока
                while (prev->next) {
                    prev = prev->next;
                }
            }
        }
        
        return dummy.next;
    }
    
private:
    /**
     * Разделяет список на блок заданного размера.
     * 
     * Отрезает первые `step` узлов от списка и возвращает начало следующего блока.
     * 
     * @param head Начало блока для разделения
     * @param step Требуемое количество узлов в блоке
     * @return Начало следующего блока (nullptr если блок последний)
     */
    ListNode* split(ListNode* head, int step) {
        if (!head) return nullptr;
        
        // Проходим (step-1) узлов для нахождения конца блока
        ListNode* cur = head;
        for (int i = 1; i < step && cur->next; i++) {
            cur = cur->next;
        }
        
        // Сохраняем начало следующего блока
        ListNode* next_block = cur->next;
        // Отрезаем текущий блок
        cur->next = nullptr;
        
        return next_block;
    }
    
    /**
     * Сливает два отсортированных списка в один.
     * 
     * Стандартный алгоритм слияния с использованием фиктивного узла.
     * Сравнивает узлы из обоих списков и последовательно соединяет их.
     * 
     * @param l1 Первый отсортированный список
     * @param l2 Второй отсортированный список
     * @return Начало объединенного отсортированного списка
     */
    ListNode* merge(ListNode* l1, ListNode* l2) {
        ListNode dummy(0);
        ListNode* tail = &dummy;
        
        // Слияние пока оба списка не пусты
        while (l1 && l2) {
            if (l1->val <= l2->val) {
                tail->next = l1;
                l1 = l1->next;
            } else {
                tail->next = l2;
                l2 = l2->next;
            }
            tail = tail->next;
        }
        
        // Присоединение остатка
        tail->next = l1 ? l1 : l2;
        
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
