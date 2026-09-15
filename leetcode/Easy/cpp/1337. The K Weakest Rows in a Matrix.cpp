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
     * Возвращает индексы k самых слабых строк бинарной матрицы.
     *
     * Алгоритм:
     * - Для каждой строки считаем количество солдат (единиц) с помощью бинарного поиска,
     *   т.к. строка отсортирована (сначала все 1, потом 0).
     * - Сортируем индексы строк по паре (количество_солдат, индекс).
     * - Берём первые k индексов.
     *
     * @param mat матрица m x n из 0 и 1
     * @param k   количество слабейших строк
     * @return    вектор индексов от самой слабой к более сильной
     */
    vector<int> kWeakestRows(vector<vector<int>>& mat, int k) {
        int m = mat.size();
        int n = mat[0].size();
        vector<int> soldiers(m);
        
        for (int i = 0; i < m; ++i) {
            // бинарный поиск первого 0
            int left = 0, right = n;
            while (left < right) {
                int mid = left + (right - left) / 2;
                if (mat[i][mid] == 1)
                    left = mid + 1;
                else
                    right = mid;
            }
            soldiers[i] = left;   // количество солдат = индекс первого 0
        }
        
        vector<int> indices(m);
        for (int i = 0; i < m; ++i) indices[i] = i;
        
        // сортируем индексы по количеству солдат, затем по индексу
        sort(indices.begin(), indices.end(), [&](int a, int b) {
            if (soldiers[a] != soldiers[b])
                return soldiers[a] < soldiers[b];  // меньше солдат – слабее
            return a < b;                          // при равенстве – меньший индекс
        });
        
        return vector<int>(indices.begin(), indices.begin() + k);
    }
};