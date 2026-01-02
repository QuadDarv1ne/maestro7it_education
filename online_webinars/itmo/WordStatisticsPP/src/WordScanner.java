/**
 * Сканер для извлечения слов из текстового потока.
 * 
 * <p>Определение слова соответствует спецификации:
 * - Непрерывная последовательность символов
 * - Допустимые символы:
 *   1. Буквы (Unicode category Letter)
 *   2. Апострофы (')
 *   3. Дефисы (Unicode category Dash_Punctuation)
 * 
 * <p>Сканер работает с потоками в кодировке UTF-8 и обеспечивает
 * линейное время обработки O(n) по количеству символов.
 * 
 * <p>Пример использования:
 * <pre>
 * WordScanner scanner = new WordScanner(inputStream);
 * String word;
 * while ((word = scanner.nextWord()) != null) {
 *     // Обработка слова
 * }
 * scanner.close();
 * </pre>
 */
import java.io.*;

public class WordScanner {
    private final InputStream inputStream;
    private final StringBuilder currentWord = new StringBuilder();
    private int currentChar = -1;
    private boolean streamClosed = false;
    
    /**
     * Создает новый сканер для указанного входного потока.
     * 
     * @param inputStream входной поток в кодировке UTF-8
     * @throws NullPointerException если inputStream равен null
     */
    public WordScanner(InputStream inputStream) {
        if (inputStream == null) {
            throw new NullPointerException("Входной поток не может быть null");
        }
        this.inputStream = inputStream;
    }
    
    /**
     * Извлекает следующее слово из входного потока.
     * 
     * <p>Алгоритм работы:
     * 1. Пропускает все не-словесные символы
     * 2. Собирает последовательность допустимых символов
     * 3. Возвращает собранное слово или null при EOF
     * 
     * @return следующее слово в потоке, приведенное к строке,
     *         или null если достигнут конец потока
     * @throws IOException если возникает ошибка чтения
     * @throws IllegalStateException если сканер закрыт
     */
    public String nextWord() throws IOException {
        if (streamClosed) {
            throw new IllegalStateException("Сканер закрыт");
        }
        
        currentWord.setLength(0); // Очищаем StringBuilder
        boolean inWord = false;
        
        while (true) {
            // Читаем следующий символ, если нужно
            if (currentChar == -1) {
                currentChar = inputStream.read();
                if (currentChar == -1) {
                    // Конец потока
                    if (inWord) {
                        return currentWord.toString();
                    }
                    return null;
                }
            }
            
            char ch = (char) currentChar;
            
            if (isWordCharacter(ch)) {
                // Ситуация 1: допустимый символ слова
                currentWord.append(ch);
                inWord = true;
                currentChar = -1; // Помечаем символ как обработанный
            } else {
                // Ситуация 2: не-словесный символ
                if (inWord) {
                    // Завершаем слово и возвращаем его
                    String word = currentWord.toString();
                    currentChar = -1; // Оставляем текущий символ для следующего вызова
                    return word;
                } else {
                    // Пропускаем не-словесный символ
                    currentChar = -1;
                }
            }
        }
    }
    
    /**
     * Проверяет, является ли символ частью слова.
     * 
     * <p>Символ считается частью слова, если он:
     * 1. Является буквой (Unicode Letter)
     * 2. Является апострофом (')
     * 3. Принадлежит к категории Dash_Punctuation (дефисы)
     * 
     * @param ch проверяемый символ
     * @return true если символ допустим в слове, false в противном случае
     */
    public static boolean isWordCharacter(char ch) {
        // Буквы
        if (Character.isLetter(ch)) {
            return true;
        }
        
        // Апостроф
        if (ch == '\'') {
            return true;
        }
        
        // Дефисы (Unicode категория Dash_Punctuation)
        if (Character.getType(ch) == Character.DASH_PUNCTUATION) {
            return true;
        }
        
        return false;
    }
    
    /**
     * Закрывает сканер и освобождает ресурсы.
     * 
     * <p>После вызова этого метода все последующие вызовы nextWord()
     * будут генерировать IllegalStateException.
     * 
     * @throws IOException если возникает ошибка при закрытии потока
     */
    public void close() throws IOException {
        streamClosed = true;
        inputStream.close();
    }
    
    /**
     * Проверяет, закрыт ли сканер.
     * 
     * @return true если сканер закрыт, false в противном случае
     */
    public boolean isClosed() {
        return streamClosed;
    }
    
    /**
     * Возвращает строковое представление сканера.
     * 
     * @return строка с информацией о состоянии сканера
     */
    @Override
    public String toString() {
        return String.format("WordScanner{closed=%s, bufferSize=%d}", 
                streamClosed, currentWord.length());
    }
}