class Solution {
    public List<Integer> getRow(int rowIndex) {
        /**
         * Возвращает k-ю строку треугольника Паскаля (индексация с 0)
         * 
         * Алгоритм: используем формулу сочетаний C(n, k) = n! / (k! * (n-k)!)
         * с оптимизацией через рекуррентное соотношение
         * 
         * Сложность: O(k) по времени, O(k) по памяти
         * 
         * @param rowIndex индекс строки (0-based)
         * @return список целых чисел, представляющий k-ю строку
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
        List<Integer> row = new ArrayList<>(rowIndex + 1);
        
        // Первый элемент всегда 1
        row.add(1);
        
        // Используем формулу C(n, k) = C(n, k-1) * (n - k + 1) / k
        for (int i = 1; i <= rowIndex; i++) {
            long value = (long) row.get(i - 1) * (rowIndex - i + 1) / i;
            row.add((int) value);
        }
        
        return row;
    }
}