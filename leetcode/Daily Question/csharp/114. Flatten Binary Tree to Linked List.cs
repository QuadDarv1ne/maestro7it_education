/**
 * Преобразование бинарного дерева в связный список на месте
 * 
 * @param root Корень бинарного дерева
 * @return void - дерево модифицируется на месте
 * 
 * Сложность: Время O(N), Память O(1)
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
public class Solution {
    public void Flatten(TreeNode root) {
        TreeNode curr = root;
        
        while (curr != null) {
            // Если у текущего узла есть левый потомок
            if (curr.left != null) {
                // Находим самый правый узел в левом поддереве
                TreeNode rightmost = curr.left;
                while (rightmost.right != null) {
                    rightmost = rightmost.right;
                }
                
                // Перенаправляем указатели
                rightmost.right = curr.right;  // Присоединяем правое поддерево
                curr.right = curr.left;        // Переносим левое поддерево вправо
                curr.left = null;              // Обнуляем левый указатель
            }
            
            // Переходим к следующему узлу
            curr = curr.right;
        }
    }
}