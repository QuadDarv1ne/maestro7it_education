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
    /**
     * Вычисляет зеркальное расстояние числа n.
     *
     * Зеркальное расстояние определяется как |n - reverse(n)|,
     * где reverse(n) - число, полученное записью цифр n в обратном порядке.
     *
     * @param n Исходное целое число.
     * @return Целое число, представляющее зеркальное расстояние.
     */
    public int mirrorDistance(int n) {
        // 1. Преобразуем число в строку.
        String s = Integer.toString(n);
        
        // 2. Переворачиваем строку с помощью StringBuilder.
        String reversedStr = new StringBuilder(s).reverse().toString();
        
        // 3. Парсим обратно в число (ведущие нули отбрасываются).
        int reversedN = Integer.parseInt(reversedStr);
        
        // 4. Возвращаем абсолютную разницу.
        return Math.abs(n - reversedN);
    }
}