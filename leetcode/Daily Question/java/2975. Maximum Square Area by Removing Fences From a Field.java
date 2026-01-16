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
class Solution {
    public int maximizeSquareArea(int m, int n, int[] hFences, int[] vFences) {
        final int MOD = 1_000_000_007;
        
        // 1. Добавляем граничные значения
        List<Integer> hList = new ArrayList<>();
        for (int fence : hFences) hList.add(fence);
        hList.add(1);
        hList.add(m);
        
        List<Integer> vList = new ArrayList<>();
        for (int fence : vFences) vList.add(fence);
        vList.add(1);
        vList.add(n);
        
        // 2. Сортируем
        Collections.sort(hList);
        Collections.sort(vList);
        
        // 3. Генерируем разницы
        Set<Integer> hDiffs = new HashSet<>();
        Set<Integer> vDiffs = new HashSet<>();
        
        for (int i = 0; i < hList.size(); i++) {
            for (int j = i + 1; j < hList.size(); j++) {
                hDiffs.add(hList.get(j) - hList.get(i));
            }
        }
        
        for (int i = 0; i < vList.size(); i++) {
            for (int j = i + 1; j < vList.size(); j++) {
                vDiffs.add(vList.get(j) - vList.get(i));
            }
        }
        
        // 4. Ищем максимальное пересечение
        int maxSide = 0;
        for (int diff : hDiffs) {
            if (vDiffs.contains(diff)) {
                maxSide = Math.max(maxSide, diff);
            }
        }
        
        // 5. Возвращаем результат
        if (maxSide == 0) return -1;
        return (int)((long)maxSide * maxSide % MOD);
    }
}