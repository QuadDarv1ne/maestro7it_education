/**
 * https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/
 */

import java.util.*;

/**
 * Генерирует все возможные комбинации букв для строки цифр digits.
 */
class Solution {
    private String[] digitMap = {
        "", "", "abc", "def", "ghi", "jkl",
        "mno", "pqrs", "tuv", "wxyz"
    };

    public List<String> letterCombinations(String digits) {
        List<String> result = new ArrayList<>();
        if (digits.isEmpty()) return result;
        backtrack(digits, 0, "", result);
        return result;
    }

    private void backtrack(String digits, int index, String current, List<String> result) {
        if (index == digits.length()) {
            result.add(current);
            return;
        }
        String letters = digitMap[digits.charAt(index) - '0'];
        for (char c : letters.toCharArray()) {
            backtrack(digits, index + 1, current + c, result);
        }
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