/**
 * Задача A — «Шпион обнаружен!»
 *
 * Условие:
 * Дана последовательность чисел. Нужно определить, есть ли среди них
 * число, которое встречается больше половины раз (более n/2).
 * Если такое число есть — вывести его, иначе — вывести -1.
 *
 * Алгоритм (Boyer–Moore Majority Vote):
 * 1. Инициализируем кандидат = -1, count = 0.
 * 2. Проходим по массиву:
 *    - Если count == 0 → кандидат = текущий элемент
 *    - Если текущий элемент == кандидат → count++
 *    - Иначе → count--
 * 3. После прохода проверяем, действительно ли кандидат встречается > n/2 раз.
 *
 * Сложность:
 * Время — O(n), память — O(1).
 */

fun main() {
    val t = readLine()!!.toInt()
    repeat(t) {
        val n = readLine()!!.toInt()
        val arr = readLine()!!.split(" ").map { it.toInt() }
        var candidate = -1
        var count = 0
        for (x in arr) {
            if (count == 0) {
                candidate = x
                count = 1
            } else if (x == candidate) count++
            else count--
        }
        val freq = arr.count { it == candidate }
        if (freq > n / 2) println(candidate) else println(-1)
    }
}


/**
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */