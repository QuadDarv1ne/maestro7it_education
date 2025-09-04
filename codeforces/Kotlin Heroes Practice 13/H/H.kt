/**
 * Задача H — «Упорядочивание рабочего стола»
 *
 * Условие:
 * Имеется сетка n×m. Звёздочки (‘*’) можно появляться/исчезать по запросам.
 * После каждого запроса нужно вывести минимальное число перемещений,
 * чтобы все ‘*’ заняли первые k позиций в column-major порядке (столбец за столбцом).
 *
 * Алгоритм:
 * Используем Fenwick Tree (BIT) по общему индексу pos = j·n + i (1-based).
 * Поддерживаем текущее количество ‘*’ TOTAL.
 * После каждого запроса: узнаём сколько звезд в первых TOTAL позициях → cntInPrefix.
 * Ответ = TOTAL - cntInPrefix.
 *
 * Сложность: O((n·m + q)·log(n·m)).
 */

import java.io.BufferedReader
import java.io.InputStreamReader
import kotlin.text.StringBuilder

class FastScanner {
    private val br = BufferedReader(InputStreamReader(System.`in`))
    private val buf = ArrayDeque<String>()
    fun next(): String {
        while (buf.isEmpty()) buf.addAll(br.readLine()?.trim()?.split(" ") ?: emptyList())
        return buf.removeFirst()
    }
    fun nextInt(): Int = next().toInt()
}

class Fenwick(val n: Int) {
    private val f = IntArray(n + 1)
    fun add(i: Int, v: Int) {
        var x = i
        while (x <= n) {
            f[x] += v
            x += x and -x
        }
    }
    fun sum(i: Int): Int {
        var x = i; var s = 0
        while (x > 0) {
            s += f[x]
            x -= x and -x
        }
        return s
    }
}

fun main() {
    val fs = FastScanner()
    val n = fs.nextInt(); val m = fs.nextInt(); val q = fs.nextInt()
    val grid = Array(n) { fs.next() }
    val N = n * m
    val fenw = Fenwick(N)
    var total = 0
    for (i in 0 until n) for (j in 0 until m) {
        if (grid[i][j] == '*') {
            total++
            val pos = j * n + (i + 1)
            fenw.add(pos, 1)
        }
    }
    val out = StringBuilder()
    repeat(q) {
        val x = fs.nextInt() - 1; val y = fs.nextInt() - 1
        val pos = y * n + (x + 1)
        if (grid[x][y] == '*') {
            grid[x] = grid[x].substring(0, y) + '.' + grid[x].substring(y + 1)
            fenw.add(pos, -1)
            total--
        } else {
            grid[x] = grid[x].substring(0, y) + '*' + grid[x].substring(y + 1)
            fenw.add(pos, +1)
            total++
        }
        val cntInPrefix = if (total > 0) fenw.sum(total) else 0
        out.append(total - cntInPrefix).append('\n')
    }
    print(out)
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