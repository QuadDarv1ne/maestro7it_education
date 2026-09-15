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
    /**
     * Находит размеры коробок для обмена, чтобы у Алисы и Боба стало поровну конфет.
     *
     * Алгоритм:
     * - Вычисляем общую сумму конфет у Алисы и Боба.
     * - Находим разницу diff = (sumA - sumB) / 2.
     * - Для каждой коробки Алисы a вычисляем необходимую коробку Боба b = a - diff.
     * - Если b есть у Боба (хранится в хеш-множестве), возвращаем [a, b].
     *
     * @param aliceSizes вектор коробок Алисы
     * @param bobSizes   вектор коробок Боба
     * @return вектор из двух чисел [коробка_Алисы, коробка_Боба]
     */
    vector<int> fairCandySwap(vector<int>& aliceSizes, vector<int>& bobSizes) {
        int sumA = accumulate(aliceSizes.begin(), aliceSizes.end(), 0);
        int sumB = accumulate(bobSizes.begin(), bobSizes.end(), 0);
        int diff = (sumA - sumB) / 2;
        unordered_set<int> setB(bobSizes.begin(), bobSizes.end());
        for (int a : aliceSizes) {
            if (setB.count(a - diff))
                return {a, a - diff};
        }
        return {};
    }
};