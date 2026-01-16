/**
 * Преобразование бинарного дерева в связный список на месте
 * 
 * @param root Корень бинарного дерева
 * @return void - дерево модифицируется на месте
 * 
 * Сложность: Время O(N), Память O(1)
 *
 * Алгоритм:
 * 1. Итеративно проходим по дереву
 * 2. Если у узла есть левый потомок:
 *    a) Находим самый правый узел в левом поддереве
 *    b) Присоединяем правое поддерево к найденному узлу
 *    c) Переносим левое поддерево вправо
 *    d) Обнуляем левый указатель
 * 3. Переходим к следующему правому узлу
 *
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
class Solution {
public:
    void flatten(TreeNode* root) {
        TreeNode* curr = root;
        
        while (curr != nullptr) {
            // Если у текущего узла есть левый потомок
            if (curr->left != nullptr) {
                // Находим самый правый узел в левом поддереве
                TreeNode* rightmost = curr->left;
                while (rightmost->right != nullptr) {
                    rightmost = rightmost->right;
                }
                
                // Перенаправляем указатели
                // 1. Подсоединяем правое поддерево текущего узла к rightmost
                rightmost->right = curr->right;
                // 2. Переносим левое поддерево вправо
                curr->right = curr->left;
                // 3. Обнуляем левый указатель
                curr->left = nullptr;
            }
            
            // Переходим к следующему узлу (который теперь в правом потомке)
            curr = curr->right;
        }
    }
};