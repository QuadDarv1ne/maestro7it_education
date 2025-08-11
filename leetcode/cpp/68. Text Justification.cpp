/**
 * https://leetcode.com/problems/text-justification/description/?envType=study-plan-v2&envId=top-interview-150
 */

#include <vector>
#include <string>

using namespace std;

class Solution {
public:
    /**
     * Форматирует текст с полным выравниванием по ширине maxWidth.
     * @param words вектор слов
     * @param maxWidth желаемая длина строки
     * @return вектор выровненных строк
     */
    vector<string> fullJustify(vector<string>& words, int maxWidth) {
        vector<string> res;
        int n = words.size();
        int i = 0;

        while (i < n) {
            int length = words[i].length();
            int j = i + 1;

            // Подбираем слова, которые войдут в текущую строку
            while (j < n && length + 1 + (int)words[j].length() <= maxWidth) {
                length += 1 + words[j].length();
                j++;
            }

            int numWords = j - i;
            string line;

            if (j == n || numWords == 1) {
                // Последняя строка или одна строка — выравнивание влево
                for (int k = i; k < j; k++) {
                    line += words[k];
                    if (k != j - 1) {
                        line += " ";
                    }
                }
                // Добавляем пробелы справа
                line += string(maxWidth - (int)line.length(), ' ');
            } else {
                // Полное выравнивание
                int totalSpaces = maxWidth;
                for (int k = i; k < j; k++) {
                    totalSpaces -= words[k].length();
                }
                int spaceBetween = totalSpaces / (numWords - 1);
                int extraSpaces = totalSpaces % (numWords - 1);

                for (int k = i; k < j - 1; k++) {
                    line += words[k];
                    line += string(spaceBetween, ' ');
                    if (k - i < extraSpaces) {
                        line += " ";
                    }
                }
                line += words[j - 1];
            }

            res.push_back(line);
            i = j;
        }

        return res;
    }
};

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