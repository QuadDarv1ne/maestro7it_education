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
 * <p>Сканер работает с потоками в кодировке UTF-8 и обеспечивает линейное время обработки O(n) по количеству символов.
 * 
 * ~ BufferedReader — это класс в Java, который предоставляет буферизованное чтение текста из потока ввода символов.
 * 
 * BufferedReader - используется для эффективного чтения символов из входного потока.
 * StringBuilder - используется для динамического построения слов по мере чтения символов.
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
import java.nio.charset.StandardCharsets;
import java.util.Objects;
import java.util.*;

public class WordScanner {
    private final BufferedReader reader;
    private final StringBuilder worldBuilder = new StringBuilder();
    private int currentChar = -1;
    private boolean closed = false; /* Stream Closed*/
    
    /**
     * Создает новый сканер для указанного входного потока.
     * 
     * @param inputStream входной поток в кодировке UTF-8
     * @throws NullPointerException если inputStream равен null
     */
    public WordScanner(InputStream inputStream) {
        // InputStreamReader конвертирует байты в символы с указанной кодировкой
        this.reader = new BufferedReader(new InputStreamReader(
                Objects.requireNonNull(inputStream, "Входной поток не может быть null"), 
                StandardCharsets.UTF_8));
    }

    /**
     * Создает сканер из Reader (например, для тестов)
     */
    public WordScanner(Reader reader) {
        this.reader = new BufferedReader(Objects.requireNonNull(reader, "Reader не может быть null"));
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
        if (closed) {
            throw new IllegalStateException("Сканер закрыт");
        }

        worldBuilder.setLength(0); // Очищаем StringBuilder
        boolean readingWord = false;
        
        while (true) {
            // Читаем следующий символ, если нужно
            if (currentChar == -1) {
                currentChar = reader.read();
            }
            
            if (currentChar == -1) {
                return readingWord ? worldBuilder.toString() : null;
            }
            
            char ch = (char) currentChar;
            
            if (isWordCharacter(ch)) {
                worldBuilder.append(ch);
                readingWord = true;
                currentChar = -1; // Сбрасываем для чтения следующего символа
            } else {
                if (readingWord) {
                    String result = worldBuilder.toString();
                    currentChar = -1; // Сбрасываем для чтения следующего символа
                    return result;
                }
                currentChar = -1; // Сбрасываем для чтения следующего символа
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
        return Character.isLetter(ch) || ch == '\'' || 
               Character.getType(ch) == Character.DASH_PUNCTUATION;
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
        if (!closed) {
            closed = true;
            reader.close();
        }
    }
    
    /**
     * Проверяет, закрыт ли сканер.
     * 
     * @return true если сканер закрыт, false в противном случае
     */
    public boolean isClosed() {
        return closed;
    }
    
    /**
     * Возвращает строковое представление сканера.
     * 
     * @return строка с информацией о состоянии сканера
     */
    @Override
    public String toString() {
        return String.format("WordScanner{closed=%s, bufferSize=%d}", 
                closed, worldBuilder.length());
    }
}