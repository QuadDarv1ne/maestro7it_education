import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class Solution {
    /**
     * Скользящее окно — это метод, при котором мы рассматриваем непрерывную подстроку (окно) и перемещаем (скользим) его по строке, проверяя выполнение определенных условий
     */
    
    /**
     * Находит все начальные индексы подстрок в строке `s`, которые являются конкатенацией 
     * всех слов из массива `words` ровно по одному разу в любом порядке. 
     * Все слова в массиве должны иметь одинаковую длину.
     *
     * <p>Алгоритм использует оптимизированный подход "скользящего окна" с обработкой смещений:
     * 1. Обрабатывает граничные случаи: пустая строка, пустой массив слов, недостаточная длина строки
     * 2. Строит частотный словарь целевых слов
     * 3. Обрабатывает строку в несколько проходов (по количеству возможных начальных смещений)
     * 4. Для каждого смещения поддерживает динамическое окно с отслеживанием частот слов:
     *    - При обнаружении валидного слова расширяет окно
     *    - При превышении частоты слова сужает окно
     *    - При обнаружении невалидного слова сбрасывает окно
     * 5. Фиксирует начальные индексы при полном совпадении всех слов
     *
     * <p><b>Анализ сложности:</b>
     * - Время: O(n * L), где:
     *      n = длина строки `s`
     *      L = длина одного слова
     * - Память: O(m * L), где:
     *      m = количество слов в массиве `words`
     *      L = длина одного слова
     *
     * <p><b>Пример использования:</b>
     * {@code
     * Solution sol = new Solution();
     * List<Integer> indices = sol.findSubstring("barfoothefoobarman", new String[]{"foo","bar"});
     * // Возвращает [0, 9]
     * }
     *
     * @param s      Строка для поиска (не может быть null)
     * @param words  Массив слов для конкатенации (все слова одинаковой длины, не может быть пустым)
     * @return       Список начальных индексов валидных подстрок (пустой список если совпадений нет)
     *
     * @implNote Детали реализации:
     * 1. Для каждого начального смещения (0 до L-1, где L = длина слова):
     *    - Инициализирует левую границу окна и временный частотный словарь
     * 2. Перемещает правую границу с шагом длины слова:
     *    a) Извлекает текущее слово
     *    b) Если слово присутствует в целевом словаре:
     *        - Увеличивает счетчик слова
     *        - Корректирует окно при превышении частоты (сдвигает левую границу)
     *        - При полном совпадении добавляет индекс и сдвигает окно
     *    c) При отсутствии слова в словаре:
     *        - Полностью сбрасывает окно (очищает словарь, обнуляет счетчик)
     *        - Перемещает левую границу за текущее слово
     */
    public List<Integer> findSubstring(String s, String[] words) {
        List<Integer> result = new ArrayList<>();
        if (words == null || words.length == 0 || s == null || s.isEmpty()) {
            return result;
        }
        
        int n = s.length();
        int m = words.length;
        int wordLen = words[0].length();
        int totalLen = m * wordLen;
        
        if (n < totalLen) {
            return result;
        }
        
        Map<String, Integer> wordCount = new HashMap<>();
        for (String word : words) {
            wordCount.put(word, wordCount.getOrDefault(word, 0) + 1);
        }
        
        for (int start = 0; start < wordLen; start++) {
            Map<String, Integer> currCount = new HashMap<>();
            int left = start;
            int count = 0;
            
            for (int right = start; right <= n - wordLen; right += wordLen) {
                String word = s.substring(right, right + wordLen);
                
                if (wordCount.containsKey(word)) {
                    currCount.put(word, currCount.getOrDefault(word, 0) + 1);
                    count++;
                    
                    while (currCount.get(word) > wordCount.get(word)) {
                        String leftWord = s.substring(left, left + wordLen);
                        currCount.put(leftWord, currCount.get(leftWord) - 1);
                        count--;
                        left += wordLen;
                    }
                    
                    if (count == m) {
                        result.add(left);
                        String leftWord = s.substring(left, left + wordLen);
                        currCount.put(leftWord, currCount.get(leftWord) - 1);
                        count--;
                        left += wordLen;
                    }
                } else {
                    currCount.clear();
                    count = 0;
                    left = right + wordLen;
                }
            }
        }
        
        return result;
    }
}

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/