/**
 * https://leetcode.com/problems/compare-version-numbers/description/?envType=daily-question&envId=2025-09-23
 */

public class Solution {
    /// <summary>
    /// Сравнение двух версий version1 и version2.
    /// 
    /// Алгоритм:
    /// 1. Разделить строки по точке.
    /// 2. Преобразовать части в числа и сравнивать их.
    /// 3. Недостающие части приравнять к 0.
    /// 4. Вернуть -1, 1 или 0.
    /// </summary>
    public int CompareVersion(string version1, string version2) {
        var parts1 = version1.Split('.');
        var parts2 = version2.Split('.');
        int n1 = parts1.Length, n2 = parts2.Length;
        int maxLen = Math.Max(n1, n2);
        for (int i = 0; i < maxLen; i++) {
            int v1 = i < n1 ? Int32.Parse(parts1[i]) : 0;
            int v2 = i < n2 ? Int32.Parse(parts2[i]) : 0;
            if (v1 < v2) return -1;
            if (v1 > v2) return 1;
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