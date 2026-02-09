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
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
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
     * @param head Голова односвязного списка
     * @return true, если список является палиндромом, иначе false
     * 
     * Примеры:
     * Вход: 1->2->2->1
     * Выход: true
     * Вход: 1->2
     * Выход: false
     */
    bool isPalindrome(ListNode* head) {
        if (!head || !head->next) {
            return true;
        }
        
        // Шаг 1: Находим середину списка
        ListNode* slow = head;
        ListNode* fast = head;
        
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        
        // Шаг 2: Разворачиваем вторую половину
        ListNode* secondHalf = reverseList(slow);
        ListNode* secondHalfCopy = secondHalf; // Для восстановления
        
        // Шаг 3: Сравниваем две половины
        ListNode* firstHalf = head;
        bool result = true;
        
        while (secondHalf) {
            if (firstHalf->val != secondHalf->val) {
                result = false;
                break;
            }
            firstHalf = firstHalf->next;
            secondHalf = secondHalf->next;
        }
        
        // Шаг 4: Восстанавливаем исходный список
        reverseList(secondHalfCopy);
        
        return result;
    }
    
private:
    /**
     * Разворачивает односвязный список.
     * 
     * @param head Голова списка для разворота
     * @return Голова развернутого списка
     */
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* current = head;
        
        while (current) {
            ListNode* nextNode = current->next;
            current->next = prev;
            prev = current;
            current = nextNode;
        }
        
        return prev;
    }
    
public:
    /**
     * Альтернативное решение с использованием вектора.
     * Проще, но использует O(n) дополнительной памяти.
     * 
     * @param head Голова списка
     * @return true, если список является палиндромом
     */
    bool isPalindromeWithVector(ListNode* head) {
        vector<int> values;
        ListNode* current = head;
        
        // Собираем значения в вектор
        while (current) {
            values.push_back(current->val);
            current = current->next;
        }
        
        // Проверяем, является ли вектор палиндромом
        int left = 0, right = values.size() - 1;
        while (left < right) {
            if (values[left] != values[right]) {
                return false;
            }
            left++;
            right--;
        }
        
        return true;
    }
};