/**
 * https://leetcode.com/problems/fruits-into-baskets-iii/description/?envType=daily-question&envId=2025-08-06
 */

/**
 * Считает количество неразмещённых фруктов.
 *
 * Идея: сегментное дерево по максимуму для поиска самого левого индекса i,
 * где baskets[i] >= fruit, затем обновление (занятие корзины).
 *
 * Время: O(n log n), Память: O(n).
 *
 * @param {number[]} fruits
 * @param {number[]} baskets
 * @return {number}
 */
var numOfUnplacedFruits = function(fruits, baskets) {
  const n = baskets.length;
  if (n === 0) return 0;

  let size = 1;
  while (size < n) size <<= 1;
  const seg = new Array(size * 2).fill(-1);

  // build
  for (let i = 0; i < n; i++) seg[size + i] = baskets[i];
  for (let i = size - 1; i > 0; --i) seg[i] = Math.max(seg[i << 1], seg[i << 1 | 1]);

  function queryFirstGE(x) {
    let idx = 1;
    if (seg[idx] < x) return -1;
    let l = 0, r = size - 1;
    while (l !== r) {
      const left = idx << 1;
      const mid = (l + r) >> 1;
      if (seg[left] >= x) {
        idx = left;
        r = mid;
      } else {
        idx = left | 1;
        l = mid + 1;
      }
    }
    return l < n ? l : -1;
  }

  function update(pos, val) {
    let i = pos + size;
    seg[i] = val;
    for (i >>= 1; i > 0; i >>= 1) {
      seg[i] = Math.max(seg[i << 1], seg[i << 1 | 1]);
    }
  }

  let unplaced = 0;
  for (const f of fruits) {
    const i = queryFirstGE(f);
    if (i === -1) unplaced++;
    else update(i, -1);
  }
  return unplaced;
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