/**
 * Задача D — «Удаление некрасивых пар»
 *
 * Условие:
 * Из строки можно удалять пары разных символов.
 * Требуется минимальная возможная длина строки.
 *
 * Алгоритм:
 * Пусть mx = максимум по количеству одной буквы, n = длина строки.
 * Минимальная длина = max(n % 2, 2*mx - n).
 *
 * Сложность:
 * Время — O(n) на подсчёт частот.
 * Память — O(1).
 */

fun main() {
    val t = readLine()!!.toInt()
    repeat(t) {
        val n = readLine()!!.toInt()
        val s = readLine()!!
        val cnt = IntArray(26)
        for (ch in s) cnt[ch - 'a']++
        val mx = cnt.maxOrNull()!!
        val ans = maxOf(n % 2, 2 * mx - n)
        println(ans)
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