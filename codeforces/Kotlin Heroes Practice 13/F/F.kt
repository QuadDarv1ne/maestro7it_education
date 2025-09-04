/**
 * Задача F — «Перестановка строк и столбцов»
 *
 * Условие:
 * Даны две матрицы A и B размера n×m с числами от 1 до n·m (уникальны).
 * Нужно проверить, можно ли перестановками строк и столбцов превратить A в B.
 *
 * Алгоритм:
 * Для каждого числа v из 1..n*m определяем его (строка, столбец) в A и B.
 * Строим отображения rowMap и colMap: каждая строка i из A
 * должна отображаться в строку rowMap[i] в B и аналогично для столбцов.
 * Проверяем, что отображения согласованы и биективны.
 *
 * Сложность: O(n·m).
 */

fun main() {
    val t = readLine()!!.toInt()
    repeat(t) {
        val (n, m) = readLine()!!.split(" ").map { it.toInt() }
        val nm = n * m
        val rowA = IntArray(nm + 1); val colA = IntArray(nm + 1)
        repeat(n) { i ->
            readLine()!!.split(" ").map { it.toInt() }
                .forEachIndexed { j, v -> rowA[v] = i; colA[v] = j }
        }
        val rowB = IntArray(nm + 1); val colB = IntArray(nm + 1)
        repeat(n) { i ->
            readLine()!!.split(" ").map { it.toInt() }
                .forEachIndexed { j, v -> rowB[v] = i; colB[v] = j }
        }

        val mapRow = IntArray(n) { -1 }
        val mapCol = IntArray(m) { -1 }
        var ok = true
        for (v in 1..nm) {
            val ra = rowA[v]; val rb = rowB[v]
            if (mapRow[ra] == -1) mapRow[ra] = rb
            else if (mapRow[ra] != rb) ok = false
            val ca = colA[v]; val cb = colB[v]
            if (mapCol[ca] == -1) mapCol[ca] = cb
            else if (mapCol[ca] != cb) ok = false
            if (!ok) break
        }

        if (ok) {
            if (mapRow.any { it == -1 } || mapRow.toSet().size != n) ok = false
            if (mapCol.any { it == -1 } || mapCol.toSet().size != m) ok = false
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