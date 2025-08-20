/**
 * https://leetcode.com/problems/soup-servings/description/?envType=daily-question&envId=2025-08-08
 */

/**
 * Вычисляет вероятность того, что суп A закончится раньше супа B,
 * плюс половина вероятности, что они закончатся одновременно.
 *
 * Идея:
 * - Масштабируем объём кратно 25 мл: m = ceil(n / 25).
 * - Рекурсивный DFS с мемоизацией по состояниям (a, b) — сколько «четвертушек» осталось.
 * - Базы:
 *     a <= 0 и b <= 0 → 0.5
 *     a <= 0 → 1.0
 *     b <= 0 → 0.0
 * - Переход:
 *     dfs(a,b) = 0.25 * [ dfs(a-4,b) + dfs(a-3,b-1) + dfs(a-2,b-2) + dfs(a-1,b-3) ]
 * - Для больших n (≈ > 4800) ответ стремится к 1.0 → возвращаем 1.0.
 *
 * Сложность:
 * - По числу уникальных состояний O(m^2), где m = ceil(n/25).
 * - Память O(m^2) на кэш.
 *
 * @param {number} n - миллилитры каждого вида супа (0 ≤ n ≤ 1e9)
 * @return {number} вероятность (погрешность ≤ 1e-5)
 */
var soupServings = function(n) {
  if (n > 4800) return 1.0;

  const m = Math.ceil(n / 25);
  const memo = new Map();

  function key(a, b) { return a + ',' + b; }

  function dfs(a, b) {
    if (a <= 0 && b <= 0) return 0.5;
    if (a <= 0) return 1.0;
    if (b <= 0) return 0.0;

    const k = key(a, b);
    if (memo.has(k)) return memo.get(k);

    const res = 0.25 * (
      dfs(a - 4, b) +
      dfs(a - 3, b - 1) +
      dfs(a - 2, b - 2) +
      dfs(a - 1, b - 3)
    );
    memo.set(k, res);
    return res;
  }

  return dfs(m, m);
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