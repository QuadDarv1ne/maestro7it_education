/**
 * https://leetcode.com/problems/4sum/description/
 */

/**
 * Описание:
 *   Возвращает все уникальные четвёрки чисел из массива nums,
 *   сумма которых равна target.
 *
 * Параметры:
 *   @param {number[]} nums - массив целых чисел
 *   @param {number} target - целевая сумма
 *
 * Возвращает:
 *   @return {number[][]} список уникальных квартетов
 *
 * Идея и сложность:
 *   Сортируем, фиксируем i и j, затем два указателя для поиска оставшихся.
 *   Пропускаем дубликаты. Время O(n^3), память O(1) доп.
 */
var fourSum = function(nums, target) {
  nums.sort((a, b) => a - b);
  const n = nums.length;
  const res = [];

  for (let i = 0; i < n - 3; i++) {
    if (i > 0 && nums[i] === nums[i - 1]) continue;

    for (let j = i + 1; j < n - 2; j++) {
      if (j > i + 1 && nums[j] === nums[j - 1]) continue;

      let l = j + 1, r = n - 1;
      while (l < r) {
        const sum = nums[i] + nums[j] + nums[l] + nums[r];
        if (sum === target) {
          res.push([nums[i], nums[j], nums[l], nums[r]]);
          l++; r--;
          while (l < r && nums[l] === nums[l - 1]) l++;
          while (l < r && nums[r] === nums[r + 1]) r--;
        } else if (sum < target) {
          l++;
        } else {
          r--;
        }
      }
    }
  }
  return res;
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