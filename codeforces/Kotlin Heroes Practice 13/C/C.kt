/**
 * Задача C — «YetnotherrokenKeoard»
 *
 * Условие:
 * Нужно обработать строку нажатий клавиш.
 * - 'b' удаляет последнюю строчную букву.
 * - 'B' удаляет последнюю заглавную букву.
 * Остальные символы добавляются.
 *
 * Алгоритм:
 * - Поддерживаем список символов res.
 * - Для строчных и заглавных букв храним стеки их индексов.
 * - При удалении ('b' или 'B') убираем последнюю букву из соответствующего стека и помечаем её удалённой.
 * - В конце собираем строку без удалённых символов.
 *
 * Сложность:
 * O(n) на строку (каждый символ добавляется/удаляется не более 1 раза).
 */

fun main() {
    val t = readLine()!!.toInt()
    repeat(t) {
        val s = readLine()!!
        val res = ArrayList<Char>(s.length)
        val lower = ArrayDeque<Int>()
        val upper = ArrayDeque<Int>()
        val deleted = BooleanArray(s.length)

        for (ch in s) {
            when (ch) {
                'b' -> {
                    while (lower.isNotEmpty() && deleted[lower.last()]) lower.removeLast()
                    if (lower.isNotEmpty()) deleted[lower.removeLast()] = true
                }
                'B' -> {
                    while (upper.isNotEmpty() && deleted[upper.last()]) upper.removeLast()
                    if (upper.isNotEmpty()) deleted[upper.removeLast()] = true
                }
                else -> {
                    val idx = res.size
                    res.add(ch)
                    if (ch.isLowerCase()) lower.addLast(idx) else upper.addLast(idx)
                }
            }
        }

        val sb = StringBuilder()
        for (i in res.indices) if (!deleted[i]) sb.append(res[i])
        println(sb.toString())
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