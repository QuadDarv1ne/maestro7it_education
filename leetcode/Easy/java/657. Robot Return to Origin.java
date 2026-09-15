/**
 * https://leetcode.com/problems/robot-return-to-origin/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Robot Return to Origin" на Java
 * 
 * Задача: Определить, возвращается ли робот в начальную точку (0,0) после выполнения всех команд.
 * 
 * Алгоритм:
 * 1. Инициализируем счётчики для вертикального (x) и горизонтального (y) перемещений
 * 2. Для каждой команды:
 *    - 'U' (up): увеличиваем x
 *    - 'D' (down): уменьшаем x
 *    - 'R' (right): увеличиваем y
 *    - 'L' (left): уменьшаем y
 * 3. Робот вернулся в начало, если x == 0 && y == 0
 * 
 * Сложность: O(n) времени, O(1) памяти
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
    public boolean judgeCircle(String moves) {
        int x = 0, y = 0;
        
        for (char move : moves.toCharArray()) {
            switch (move) {
                case 'U': x++; break;
                case 'D': x--; break;
                case 'R': y++; break;
                case 'L': y--; break;
            }
        }
        
        return x == 0 && y == 0;
    }
}