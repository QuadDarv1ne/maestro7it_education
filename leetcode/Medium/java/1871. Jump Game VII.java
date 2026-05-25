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

class Solution {
    /**
     * Решение задачи Jump Game VII.
     * 
     * Метод определяет, можно ли добраться до последнего индекса бинарной строки s.
     * Движение возможно только вперед на расстояние от minJump до maxJump.
     * Посадка разрешена только на символы '0'.
     * 
     * Алгоритм:
     * 1. Массив dp[] хранит информацию о достижимости каждого индекса.
     * 2. Переменная count отслеживает количество достижимых позиций в окне
     *    [i - maxJump, i - minJump], откуда можно прыгнуть в текущую позицию i.
     * 3. Сложность O(N) по времени и O(N) по памяти.
     * 
     * @param s Бинарная строка (состоит из '0' и '1').
     * @param minJump Минимальная длина прыжка.
     * @param maxJump Максимальная длина прыжка.
     * @return boolean true, если последний индекс достижим.
     */
    public boolean canReach(String s, int minJump, int maxJump) {
        int n = s.length();
        boolean[] dp = new boolean[n];
        dp[0] = true;
        int count = 0;

        for (int i = 1; i < n; i++) {
            // Если индекс входит в правую часть окна источников
            if (i >= minJump && dp[i - minJump]) {
                count++;
            }
            // Если индекс выходит из левой части окна источников
            if (i > maxJump && dp[i - maxJump - 1]) {
                count--;
            }

            // Если текущий символ '0' и есть доступные источники прыжка (count > 0)
            if (s.charAt(i) == '0' && count > 0) {
                dp[i] = true;
            }
        }
        
        return dp[n - 1];
    }
}