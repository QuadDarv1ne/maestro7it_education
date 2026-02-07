/**
 * https://leetcode.com/problems/minimum-deletions-to-make-string-balanced/description/
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "1653. Minimum Deletions to Make String Balanced"
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
    /**
     * Находит минимальное количество удалений для получения сбалансированной строки.
     * Сбалансированная строка - строка, в которой все 'a' идут перед всеми 'b'.
     * 
     * @param s Входная строка, состоящая только из 'a' и 'b'
     * @return Минимальное количество удалений
     */
    public int MinimumDeletions(string s) {
        int totalA = s.Count(c => c == 'a');
        int leftB = 0, rightA = totalA;
        int minDeletions = leftB + rightA; // Разрез перед первым символом
        
        foreach (char ch in s) {
            if (ch == 'a') {
                rightA--;
            } else { // ch == 'b'
                leftB++;
            }
            minDeletions = Math.Min(minDeletions, leftB + rightA);
        }
        
        return minDeletions;
    }
}