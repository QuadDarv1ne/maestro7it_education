/**
 * https://leetcode.com/problems/merge-k-sorted-lists/description/
 */

/**
 * ListNode — это базовая структура данных, используемая для представления узла в односвязном списке (singly linked list).
 * 
 * Фиктивная голова (Dummy Head) — это технический приём при работе со связными списками, который упрощает операции добавления/удаления элементов.
 * 
 * Deque (двусторонняя очередь) — это структура данных, которая позволяет добавлять и удалять элементы как в начале, так и в конце за константное время O(1).
 * Название произносится как "дек" (от англ. "deck") и является аббревиатурой от Double-Ended Queue.
 * 
 * Компаратор — это функция или функциональный объект, определяющий порядок сортировки элементов.
 * В контексте задачи со слиянием списков компаратор используется для настройки поведения приоритетной очереди (min-heap).
 */

/**
 * Объединяет k отсортированных связных списков в один отсортированный список.
 * 
 * <p>Алгоритм использует минимальную кучу (приоритетную очередь) для эффективного
 * извлечения узлов с минимальными значениями на каждом шаге. Основные этапы:
 * 1. Проверка граничных условий (пустой ввод)
 * 2. Инициализация приоритетной очереди с компаратором для сравнения значений узлов
 * 3. Добавление голов всех непустых списков в очередь
 * 4. Построение результирующего списка с использованием фиктивного головного узла
 * 5. Последовательное извлечение минимальных узлов из очереди и добавление их в результат
 * 6. Добавление следующего узла извлеченного списка в очередь (если существует)
 * 
 * <p><b>Сложность алгоритма:</b>
 * - Временная: O(N log K), где:
 *      N = общее количество узлов во всех списках,
 *      K = количество связных списков
 * - Пространственная: O(K) (для хранения узлов в очереди)
 *
 * <p><b>Пример использования:</b>
 * {@code
 * ListNode list1 = new ListNode(1, new ListNode(4, new ListNode(5)));
 * ListNode list2 = new ListNode(1, new ListNode(3, new ListNode(4)));
 * ListNode list3 = new ListNode(2, new ListNode(6));
 * 
 * ListNode[] lists = {list1, list2, list3};
 * ListNode result = new Solution().mergeKLists(lists);
 * // Результат: 1->1->2->3->4->4->5->6
 * }
 *
 * @param lists Массив голов связных списков, отсортированных в порядке возрастания.
 *             Может содержать пустые списки (null элементы).
 * @return Голова объединенного отсортированного связного списка. 
 *         Возвращает null если все входные списки пусты.
 *
 * @implNote Детали реализации:
 * 1. Используется фиктивный головной узел (dummy head) для упрощения кода
 * 2. Приоритетная очередь гарантирует извлечение минимального элемента за O(1)
 * 3. Каждое добавление/удаление в очередь выполняется за O(log K)
 * 4. Алгоритм устойчив к обработке пустых списков и null значениям
 */

import java.util.PriorityQueue;
import java.util.Comparator;

class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        // Проверка на пустые списки
        if (lists == null || lists.length == 0) return null;
        
        // Компаратор для сравнения узлов по значению
        Comparator<ListNode> comparator = (a, b) -> a.val - b.val;
        
        // Приоритетная очередь (минимальная куча)
        PriorityQueue<ListNode> minHeap = new PriorityQueue<>(comparator);
        
        // Добавляем первые узлы всех непустых списков
        for (ListNode node : lists) {
            if (node != null) {
                minHeap.offer(node);
            }
        }
        
        // Фиктивный узел для упрощения построения результата
        ListNode dummy = new ListNode(0);
        ListNode current = dummy;
        
        while (!minHeap.isEmpty()) {
            // Извлекаем узел с минимальным значением
            ListNode minNode = minHeap.poll();
            
            // Добавляем его в результирующий список
            current.next = minNode;
            current = current.next;
            
            // Если есть следующий узел, добавляем в кучу
            if (minNode.next != null) {
                minHeap.offer(minNode.next);
            }
        }
        
        return dummy.next;
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
