/**
 * Максимальная площадь квадратного поля после удаления заборов
 * 
 * @param m Количество строк в поле (граничные заборы на 1 и m)
 * @param n Количество столбцов в поле (граничные заборы на 1 и n)
 * @param hFences Массив горизонтальных заборов (между строками)
 * @param vFences Массив вертикальных заборов (между столбцами)
 * @return Максимальная площадь квадрата (по модулю 1e9+7) или -1
 * 
 * Сложность: O(h² + v²), где h и v ≤ 600
 * 
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
    int maximizeSquareArea(int m, int n, vector<int>& hFences, vector<int>& vFences) {
        const int MOD = 1e9 + 7;
        
        // 1. Добавляем граничные заборы (которые нельзя удалить)
        hFences.push_back(1);
        hFences.push_back(m);
        vFences.push_back(1);
        vFences.push_back(n);
        
        // 2. Сортируем массивы
        sort(hFences.begin(), hFences.end());
        sort(vFences.begin(), vFences.end());
        
        // 3. Генерируем все возможные разницы (длины отрезков)
        unordered_set<int> hDiffs, vDiffs;
        for (int i = 0; i < hFences.size(); i++) {
            for (int j = i + 1; j < hFences.size(); j++) {
                hDiffs.insert(hFences[j] - hFences[i]);
            }
        }
        for (int i = 0; i < vFences.size(); i++) {
            for (int j = i + 1; j < vFences.size(); j++) {
                vDiffs.insert(vFences[j] - vFences[i]);
            }
        }
        
        // 4. Ищем максимальное общее значение
        int maxSide = 0;
        for (int diff : hDiffs) {
            if (vDiffs.count(diff)) {
                maxSide = max(maxSide, diff);
            }
        }
        
        // 5. Возвращаем результат
        if (maxSide == 0) return -1;
        return (1LL * maxSide * maxSide) % MOD;
    }
};