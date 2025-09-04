/**
 * Задача E — «Ива и Пав»
 *
 * Условие:
 * Для строки s проверить, можно ли вырезать подстроку s[k..r]
 * и присоединить её в начало, чтобы получить новое s,
 * такое что s == reversed(s), т.е. строка станет палиндромом.
 *
 * Алгоритм:
 * Простой линейный перебор k от 0 до n и проверка, даёт ли при
 * циклическом сдвиге палиндром s. Для каждого k формируем строку t:
 *  t = s.substring(k) + s.substring(0, k)
 *  проверяем t == t.reversed()
 * Если хотя бы один k подходит — YES, иначе — NO.
 *
 * Сложность: O(n^2) в худшем случае, n ≤ 10^3 — допустимо.
 */

fun main() {
    val t = readLine()!!.toInt()
    repeat(t) {
        val n = readLine()!!.toInt()
        val s = readLine()!!
        var ok = false
        for (k in 0 until n) {
            val tStr = s.substring(k) + s.substring(0, k)
            if (tStr == tStr.reversed()) {
                ok = true
                break
            }
        }
        println(if (ok) "YES" else "NO")
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