/**
 * Задача G — «Любимая двоичная строка Качины»
 *
 * Условие:
 * Дана бинарная строка s длиной n.
 * Если строка состоит только из '0' или только из '1',
 * то однозначно восстановить её невозможно (функция f(1, n) == 0).
 * В этом случае выводим "IMPOSSIBLE".
 * Во всех остальных случаях выводим саму строку.
 *
 * Алгоритм:
 * 1. Считываем количество тестов t.
 * 2. Для каждого теста читаем n и строку s.
 * 3. Проверяем, есть ли в строке хотя бы один '0' и хотя бы один '1'.
 *    - Если оба символа присутствуют → выводим s.
 *    - Иначе → выводим "IMPOSSIBLE".
 *
 * Сложность:
 * Время — O(n) на каждый тест (проход по строке).
 * Память — O(1) дополнительная.
 */

import java.io.BufferedInputStream
import java.lang.StringBuilder

private class FastScanner {
    private val input = BufferedInputStream(System.`in`)
    private val buffer = ByteArray(1 shl 16)
    private var len = 0
    private var ptr = 0

    private fun readByte(): Int {
        if (ptr >= len) {
            len = input.read(buffer)
            ptr = 0
            if (len <= 0) return -1
        }
        return buffer[ptr++].toInt()
    }

    fun nextInt(): Long {
        var c = readByte()
        while (c <= 32) c = readByte()
        var sign = 1
        if (c == '-'.code) { sign = -1; c = readByte() }
        var x = 0L
        while (c > 32) {
            x = x * 10 + (c - '0'.code)
            c = readByte()
        }
        return x * sign
    }
}

fun main() {
    val fs = FastScanner()
    val t = fs.nextInt().toInt()

    repeat(t) {
        val n = fs.nextInt().toInt()

        // запрос f(1, i)
        fun ask(i: Int): Long {
            println("? 1 $i")
            System.out.flush()
            val ans = fs.nextInt()
            if (ans == -1L) {
                // на всякий случай — завершить при невалидном ответе
                System.exit(0)
            }
            return ans
        }

        val s = CharArray(n) { '?' }
        var prevF = 0L
        var zKnown = false
        var z = 0 // количество нулей в уже восстановленном префиксе
        var determined = false

        // Будем хранить первые p-1 позиций до момента первой Δ>0,
        // чтобы потом единым махом разложить как 1^a 0^b.
        var firstPosDelta = -1
        var firstDeltaVal = -1

        for (i in 2..n) {
            val curF = ask(i)
            val delta = curF - prevF
            prevF = curF

            if (!zKnown) {
                if (delta > 0) {
                    // нашлась первая положительная дельта
                    firstPosDelta = i
                    firstDeltaVal = delta.toInt()
                    val b = firstDeltaVal
                    val a = (i - 1) - b
                    if (a < 0 || b < 0) {
                        println("! IMPOSSIBLE")
                        System.out.flush()
                        determined = true
                        break
                    }
                    // префикс 1^a 0^b
                    for (j in 0 until a) s[j] = '1'
                    for (j in a until i - 1) s[j] = '0'
                    s[i - 1] = '1'
                    zKnown = true
                    z = b
                } else {
                    // пока ничего не знаем — откладываем решение
                    // (позиции 1..i-1 остаются '?')
                }
            } else {
                // z уже известен — двигаемся однозначно
                if (delta == 0L) {
                    s[i - 1] = '0'
                    z++
                } else if (delta == z.toLong()) {
                    s[i - 1] = '1'
                } else {
                    // противоречие
                    println("! IMPOSSIBLE")
                    System.out.flush()
                    determined = true
                    break
                }
            }
        }

        if (determined) return@repeat

        if (!zKnown) {
            // так и не встретили положительную дельту — строка не определяется
            println("! IMPOSSIBLE")
            System.out.flush()
            return@repeat
        }

        // Заполнить s[0], если ещё '?' (возможен только до первой положительной дельты)
        for (i in s.indices) if (s[i] == '?') s[i] = '0' // не должно остаться, но на всякий случай

        val ans = String(s)
        println("! $ans")
        System.out.flush()
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