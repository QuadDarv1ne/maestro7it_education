/**
 * https://leetcode.com/problems/compare-version-numbers/description/?envType=daily-question&envId=2025-09-23
 */

class Solution {
    /**
     * Сравнение двух версий version1 и version2.
     *
     * Алгоритм:
     * 1. Разделить строки по точке.
     * 2. Сравнивать числа по очереди (учитывать ведущие нули).
     * 3. Недостающие части считаются равными 0.
     * 4. Возвращаем -1, 1 или 0 в зависимости от результата сравнения.
     *
     * @param version1 строка первой версии
     * @param version2 строка второй версии
     * @return -1 если version1 < version2,
     *          1 если version1 > version2,
     *          0 если равны
     */
    public int compareVersion(String version1, String version2) {
        String[] parts1 = version1.split("\\.");
        String[] parts2 = version2.split("\\.");
        int n1 = parts1.length;
        int n2 = parts2.length;
        int maxLen = Math.max(n1, n2);
        for (int i = 0; i < maxLen; i++) {
            int v1 = i < n1 ? Integer.parseInt(parts1[i]) : 0;
            int v2 = i < n2 ? Integer.parseInt(parts2[i]) : 0;
            if (v1 < v2) return -1;
            else if (v1 > v2) return 1;
        }
        return 0;
    }
}

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