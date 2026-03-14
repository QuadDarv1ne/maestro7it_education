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

/**
 * Возвращает k-ю счастливую строку длины n в лексикографическом порядке.
 *
 * Счастливая строка состоит только из 'a', 'b', 'c' и не имеет двух одинаковых соседних символов.
 * Если количество таких строк меньше k, возвращается пустая строка.
 *
 * Алгоритм: математический подход без генерации всех строк.
 * Общее количество строк = 3 * 2^(n-1). Если k выходит за пределы, возвращаем "".
 * Затем строим строку посимвольно, выбирая символ на основе того,
 * сколько строк начинается с каждого возможного префикса (2^(n - len - 1)).
 *
 * @param n длина строки (1 ≤ n ≤ 10)
 * @param k порядковый номер строки (1-индексация, 1 ≤ k ≤ 100)
 * @return k-я счастливая строка или пустая строка, если ее нет
 */

class Solution {
    public String getHappyString(int n, int k) {
        // Общее количество строк: 3 * 2^(n-1)
        int total = 3 * (1 << (n - 1)); // 1 << (n-1) = 2^(n-1)
        if (k > total) return "";

        StringBuilder result = new StringBuilder();
        char prev = 0; // предыдущий символ (0 означает, что его нет)

        for (int i = 0; i < n; i++) {
            // Перебираем символы в лексикографическом порядке
            for (char c : new char[]{'a', 'b', 'c'}) {
                if (c == prev) continue; // соседние не могут быть равны

                // Количество строк с текущим префиксом для оставшихся позиций
                int count = 1 << (n - i - 1); // 2^(n - i - 1)

                if (k > count) {
                    k -= count; // пропускаем этот блок
                } else {
                    result.append(c); // фиксируем символ
                    prev = c;
                    break;
                }
            }
        }
        return result.toString();
    }
}