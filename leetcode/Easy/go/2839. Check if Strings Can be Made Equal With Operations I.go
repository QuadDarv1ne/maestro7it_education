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
 * 
 * Проверяет, можно ли сделать две строки длины 4 равными,
 * меняя местами символы на позициях, разница между которыми равна 2.
 * 
 * Параметры:
 *     s1 (string): первая строка
 *     s2 (string): вторая строка
 * 
 * Возвращает:
 *     bool: True, если строки можно сделать равными, иначе False
 * 
 * Примечания:
 *     - Длина строк равна 4
 *     - Доступны только два возможных обмена: (0,2) и (1,3)
 *     - Сложность: O(1) по времени и памяти
 */

package main

func canBeEqual(s1 string, s2 string) bool {
    // Проверяем мультимножества символов на позициях (0,2)
    if !isPairEqual(s1[0], s1[2], s2[0], s2[2]) {
        return false
    }
    
    // Проверяем мультимножества символов на позициях (1,3)
    if !isPairEqual(s1[1], s1[3], s2[1], s2[3]) {
        return false
    }
    
    return true
}

// isPairEqual проверяет, равны ли мультимножества двух пар символов
func isPairEqual(a1, a2, b1, b2 byte) bool {
    // Сортируем пары и сравниваем
    // Пара (a1, a2)
    minA := min(a1, a2)
    maxA := max(a1, a2)
    
    // Пара (b1, b2)
    minB := min(b1, b2)
    maxB := max(b1, b2)
    
    return minA == minB && maxA == maxB
}

func min(a, b byte) byte {
    if a < b {
        return a
    }
    return b
}

func max(a, b byte) byte {
    if a > b {
        return a
    }
    return b
}