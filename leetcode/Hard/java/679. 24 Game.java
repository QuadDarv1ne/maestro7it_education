/**
 * https://leetcode.com/problems/24-game/description/
 */
class Solution {
    /**
     * Определяет, можно ли составить из четырех карт арифметическое выражение, равное 24,
     * используя операторы +, -, *, / и скобки.
     *
     * @param cards массив из 4 чисел [1..9]
     * @return true, если выражение, равное 24, существует; иначе — false
     *
     * Алгоритм:
     * Рекурсивный бэктрекинг: выбираем пару чисел, применяем все возможные бинарные операции,
     * рекурсивно проверяем получившиеся числа.
     *
     * Время: эффективно при фиксированном размере (4 числа)
     * Память: O(n) — глубина рекурсии
     */
    public boolean judgePoint24(int[] cards) {
        List<Double> nums = new ArrayList<>();
        for (int c : cards) nums.add((double) c);
        return dfs(nums);
    }

    private boolean dfs(List<Double> nums) {
        final double EPS = 1e-6;
        if (nums.size() == 1) {
            return Math.abs(nums.get(0) - 24.0) < EPS;
        }
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                List<Double> next = new ArrayList<>();
                for (int k = 0; k < n; k++) {
                    if (k != i && k != j) next.add(nums.get(k));
                }
                double a = nums.get(i), b = nums.get(j);
                List<Double> results = Arrays.asList(
                    a + b, a - b, b - a, a * b,
                    b != 0 ? a / b : Double.MAX_VALUE,
                    a != 0 ? b / a : Double.MAX_VALUE
                );
                for (double r : results) {
                    next.add(r);
                    if (dfs(next)) return true;
                    next.remove(next.size() - 1);
                }
            }
        }
        return false;
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