/**
 * https://leetcode.com/problems/text-justification/description/?envType=study-plan-v2&envId=top-interview-150
 */

import java.util.ArrayList;
import java.util.List;

public class Solution {
    /**
     * Метод форматирует текст с полным выравниванием по ширине maxWidth.
     *
     * @param words массив слов
     * @param maxWidth длина каждой строки
     * @return список строк, выровненных по ширине
     */
    public List<String> fullJustify(String[] words, int maxWidth) {
        List<String> res = new ArrayList<>();
        int n = words.length;
        int i = 0;

        while (i < n) {
            int length = words[i].length();
            int j = i + 1;

            // Подбираем слова для текущей строки
            while (j < n && length + 1 + words[j].length() <= maxWidth) {
                length += 1 + words[j].length();
                j++;
            }

            int numWords = j - i;
            StringBuilder line = new StringBuilder();

            // Если последняя строка или в строке одно слово — выравниваем влево
            if (j == n || numWords == 1) {
                for (int k = i; k < j; k++) {
                    line.append(words[k]);
                    if (k != j - 1) {
                        line.append(" ");
                    }
                }
                // Добавляем пробелы справа
                int remaining = maxWidth - line.length();
                for (int k = 0; k < remaining; k++) {
                    line.append(" ");
                }
            } else {
                // Полное выравнивание: распределяем пробелы равномерно
                int totalSpaces = maxWidth;
                for (int k = i; k < j; k++) {
                    totalSpaces -= words[k].length();
                }
                int spaceBetween = totalSpaces / (numWords - 1);
                int extraSpaces = totalSpaces % (numWords - 1);

                for (int k = i; k < j - 1; k++) {
                    line.append(words[k]);
                    for (int s = 0; s < spaceBetween; s++) {
                        line.append(" ");
                    }
                    if (k - i < extraSpaces) {
                        line.append(" ");
                    }
                }
                line.append(words[j - 1]);
            }

            res.add(line.toString());
            i = j;
        }

        return res;
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