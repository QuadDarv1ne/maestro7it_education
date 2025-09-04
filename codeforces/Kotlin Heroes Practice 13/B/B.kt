/**
 * Задача B — «Нелюбовь к тройкам»
 *
 * Условие:
 * Найти k-й положительный целый, который не делится на 3 и не оканчивается цифрой 3.
 *
 * Алгоритм:
 * Перебирать числа x начиная с 1, проверять условия:
 *  - x % 3 != 0
 *  - x % 10 != 3
 * Считать количество подходящих чисел, пока не достигнем k.
 *
 * Сложность:
 * Время — O(k) на тест, что достаточно при k ≤ 1000.
 * Память — O(1).
 */

fun main() {
    val t = readLine()!!.toInt()
    repeat(t) {
        val k = readLine()!!.toInt()
        var count = 0
        var x = 0
        while (count < k) {
            x++
            if (x % 3 != 0 && x % 10 != 3) {
                count++
            }
        }
        println(x)
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