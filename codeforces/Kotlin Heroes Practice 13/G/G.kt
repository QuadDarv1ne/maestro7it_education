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

import java.io.BufferedReader
import java.io.InputStreamReader
import kotlin.text.StringBuilder

fun main() {
    val br = BufferedReader(InputStreamReader(System.`in`))
    val t = br.readLine()?.toIntOrNull() ?: return
    val out = StringBuilder()

    repeat(t) {
        val n = br.readLine()?.toIntOrNull() ?: return
        val s = br.readLine()?.trim() ?: return
        val hasZero = '0' in s
        val hasOne = '1' in s
        if (hasZero && hasOne) {
            out.append(s).append('\n')
        } else {
            out.append("IMPOSSIBLE\n")
        }
    }
    print(out.toString())
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