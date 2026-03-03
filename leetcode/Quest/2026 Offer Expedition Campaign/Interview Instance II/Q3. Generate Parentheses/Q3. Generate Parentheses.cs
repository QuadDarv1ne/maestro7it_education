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

public class Solution {
    public IList<string> GenerateParenthesis(int n) {
        List<string> result = new List<string>();
        Backtrack(result, "", 0, 0, n);
        return result;
    }
    
    private void Backtrack(List<string> result, string current, int open, int close, int max) {
        if (current.Length == max * 2) {
            result.Add(current);
            return;
        }
        if (open < max) {
            Backtrack(result, current + "(", open + 1, close, max);
        }
        if (close < open) {
            Backtrack(result, current + ")", open, close + 1, max);
        }
    }
}