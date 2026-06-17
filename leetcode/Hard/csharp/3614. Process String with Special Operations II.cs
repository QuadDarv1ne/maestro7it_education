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
    /// <summary>
    /// Возвращает k-й символ (0-индексация) строки, полученной после обработки s.
    ///
    /// Правила обработки s слева направо:
    /// - Строчная буква: добавляется в конец result.
    /// - '*': удаляет последний символ result, если он есть.
    /// - '#': дублирует result (result = result + result).
    /// - '%': переворачивает result.
    ///
    /// Поскольку k может достигать 10^15, прямое построение строки невозможно.
    /// Алгоритм:
    /// 1. Прямой проход: вычисляем длину result после каждой операции.
    /// 2. Если k >= итоговой длины, возвращаем '.'.
    /// 3. Обратный проход с отслеживанием позиции p и флага переворота r.
    ///    Флаг r позволяет обрабатывать '%' без точного значения длины.
    ///
    /// Ограничения: 1 <= s.Length <= 10^5, 0 <= k <= 10^15.
    /// Промежуточная длина не превышает 10^15 + |s|, что помещается в long.
    ///
    /// Сложность: время O(n), память O(n), где n = s.Length.
    /// </summary>
    public char ProcessStr(string s, long k) {
        int n = s.Length;
        // L[i] — длина result после обработки s[0..i-1]. L[0] = 0.
        long[] L = new long[n + 1];
        for (int i = 0; i < n; i++) {
            char c = s[i];
            if (c == '*') {
                L[i + 1] = Math.Max(0L, L[i] - 1);
            } else if (c == '#') {
                L[i + 1] = L[i] * 2;
            } else if (c == '%') {
                L[i + 1] = L[i];
            } else {
                L[i + 1] = L[i] + 1;
            }
        }

        if (k >= L[n]) {
            return '.';
        }

        long p = k;
        bool r = false;
        for (int i = n - 1; i >= 0; i--) {
            char c = s[i];
            if (c == '*') {
                if (r) p += 1;
            } else if (c == '#') {
                long half = L[i];
                if (p >= half) p -= half;
            } else if (c == '%') {
                r = !r;
            } else {
                // Строчная буква
                if (!r) {
                    if (p == L[i + 1] - 1) {
                        return c;
                    }
                } else {
                    if (p == 0) {
                        return c;
                    }
                    p -= 1;
                }
            }
        }
        return '.';
    }
}