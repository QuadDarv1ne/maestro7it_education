/**
 * https://leetcode.com/problems/maximum-69-number/description/?envType=daily-question&envId=2025-08-16
 */

public class Solution {
    /// <summary>
    /// Возвращает максимально возможное число,
    /// заменяя первую цифру '6' на '9'.
    /// </summary>
    public int Maximum69Number (int num) {
        char[] arr = num.ToString().ToCharArray();
        for (int i = 0; i < arr.Length; i++) {
            if (arr[i] == '6') {
                arr[i] = '9';
                break;
            }
        }
        return int.Parse(new string(arr));
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