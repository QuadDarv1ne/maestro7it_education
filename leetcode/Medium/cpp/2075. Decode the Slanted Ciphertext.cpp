/**
 * https://leetcode.com/problems/decode-the-slanted-ciphertext/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Decode the Slanted Ciphertext" на C++
 * 
 * Задача: Расшифровать строку, закодированную наклонной транспозицией.
 * 
 * Алгоритм:
 * 1. Вычисляем количество столбцов: cols = encodedText.length() / rows
 * 2. Создаём виртуальную матрицу rows x cols
 * 3. Заполняем матрицу по строкам из encodedText
 * 4. Читаем символы по диагоналям (слева-направо, сверху-вниз)
 * 5. Удаляем конечные пробелы
 * 
 * Ключевое наблюдение:
 * Исходный текст читается по диагоналям, начиная с позиции (0,0),
 * затем (1,1), (2,2) и так далее до конца строки.
 * 
 * Сложность: O(rows * cols) = O(n) времени, O(n) памяти
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

class Solution {
public:
    string decodeCiphertext(string encodedText, int rows) {
        // Обработка пустой строки
        if (encodedText.empty()) return "";
        
        int n = encodedText.length();
        int cols = n / rows;  // Количество столбцов
        
        string result;
        
        // Проходим по диагоналям, начиная с первого столбца
        for (int startCol = 0; startCol < cols; startCol++) {
            // Идём по диагонали: row++, col++
            for (int i = 0, j = startCol; i < rows && j < cols; i++, j++) {
                int index = i * cols + j;
                result += encodedText[index];
            }
        }
        
        // Удаляем конечные пробелы (originalText не содержит их в конце)
        while (!result.empty() && result.back() == ' ') {
            result.pop_back();
        }
        
        return result;
    }
};