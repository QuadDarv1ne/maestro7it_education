/**
 * Максимальная площадь квадратного поля после удаления заборов
 * 
 * @param m Количество строк в поле
 * @param n Количество столбцов в поле
 * @param hFences Массив горизонтальных заборов
 * @param vFences Массив вертикальных заборов
 * @return Максимальная площадь квадрата (по модулю 1_000_000_007) или -1
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
public class Solution {
    public int MaximizeSquareArea(int m, int n, int[] hFences, int[] vFences) {
        const int MOD = 1_000_000_007;
        
        // 1. Добавляем граничные значения
        var hList = new List<int>(hFences) { 1, m };
        var vList = new List<int>(vFences) { 1, n };
        
        // 2. Сортируем
        hList.Sort();
        vList.Sort();
        
        // 3. Генерируем разницы
        var hDiffs = new HashSet<int>();
        var vDiffs = new HashSet<int>();
        
        for (int i = 0; i < hList.Count; i++) {
            for (int j = i + 1; j < hList.Count; j++) {
                hDiffs.Add(hList[j] - hList[i]);
            }
        }
        
        for (int i = 0; i < vList.Count; i++) {
            for (int j = i + 1; j < vList.Count; j++) {
                vDiffs.Add(vList[j] - vList[i]);
            }
        }
        
        // 4. Ищем максимальное пересечение
        int maxSide = 0;
        foreach (int diff in hDiffs) {
            if (vDiffs.Contains(diff)) {
                maxSide = Math.Max(maxSide, diff);
            }
        }
        
        // 5. Возвращаем результат
        if (maxSide == 0) return -1;
        return (int)((long)maxSide * maxSide % MOD);
    }
}