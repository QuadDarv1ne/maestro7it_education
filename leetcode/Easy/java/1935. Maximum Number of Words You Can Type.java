/**
 * https://leetcode.com/problems/maximum-number-of-words-you-can-type/description/?envType=daily-question&envId=2025-09-15
 */

public class Solution {
    /**
     * Подсчитывает количество слов в тексте, которые можно набрать, не используя сломанные клавиши.
     *
     * @param text Исходный текст, разделенный пробелами.
     * @param brokenLetters Строка с символами сломанных клавиш.
     * @return Количество слов, которые можно набрать без использования сломанных клавиш.
     */
    public int canBeTypedWords(String text, String brokenLetters) {
        String[] words = text.split(" ");
        int count = 0;
        for (String word : words) {
            boolean valid = true;
            for (char c : word.toCharArray()) {
                if (brokenLetters.indexOf(c) != -1) {
                    valid = false;
                    break;
                }
            }
            if (valid) {
                count++;
            }
        }
        return count;
    }
}

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1  @quadd4rv1n7
# 3. Telegram №2  @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/