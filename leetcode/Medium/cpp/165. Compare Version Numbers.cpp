/**
 * https://leetcode.com/problems/compare-version-numbers/description/?envType=daily-question&envId=2025-09-23
 */

#include <string>
using namespace std;

class Solution {
public:
    /**
     * Сравнение двух версий version1 и version2.
     *
     * Алгоритм:
     * 1. Считываем по очереди части (revision), разделённые точкой.
     * 2. Преобразуем каждую часть в число.
     * 3. Сравниваем текущие части:
     *    - если одна строка закончилась раньше, считаем недостающую часть равной 0.
     *    - если части отличаются, возвращаем -1 или 1.
     * 4. Если все части равны — возвращаем 0.
     *
     * @param version1 строка первой версии
     * @param version2 строка второй версии
     * @return -1, если version1 < version2;
     *          1, если version1 > version2;
     *          0, если равны
     */
    int compareVersion(string version1, string version2) {
        int i = 0, j = 0;
        int n1 = version1.size(), n2 = version2.size();
        while (i < n1 || j < n2) {
            long v1 = 0;
            while (i < n1 && version1[i] != '.') {
                v1 = v1 * 10 + (version1[i] - '0');
                i++;
            }
            long v2 = 0;
            while (j < n2 && version2[j] != '.') {
                v2 = v2 * 10 + (version2[j] - '0');
                j++;
            }
            if (v1 < v2) return -1;
            if (v1 > v2) return 1;
            i++;
            j++;
        }
        return 0;
    }
};

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/