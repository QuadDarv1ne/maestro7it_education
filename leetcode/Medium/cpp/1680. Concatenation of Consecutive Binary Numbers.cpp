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
public:
    int concatenatedBinary(int n) {
        const int MOD = 1'000'000'007;
        long long ans = 0;   // используем 64-битный тип для промежуточных вычислений
        int bits = 0;         // текущая длина двоичного представления числа i

        for (int i = 1; i <= n; ++i) {
            // Если i — степень двойки, увеличиваем количество бит
            if ((i & (i - 1)) == 0) {
                ++bits;
            }
            // "Дописываем" i справа к ans:
            // сдвигаем ans влево на bits и прибавляем i
            ans = ((ans << bits) | i) % MOD;
        }
        return ans;
    }
};