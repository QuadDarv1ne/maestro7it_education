package analyzer.scanner;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.function.Predicate;

/**
 * Универсальный сканер с блочным чтением для выделения токенов
 */
public class TextScanner implements AutoCloseable {
    private static final int DEFAULT_BUFFER_SIZE = 8192;
    private static final int MAX_TOKEN_LENGTH = 100000;
    
    private final Reader reader;
    private final char[] buffer;
    private int bufferPos;
    private int bufferSize;
    private boolean closed;
    private int currentPosition;
    private int currentLine;
    private int currentColumn;
    private boolean lastCharWasNewline;
    
    // Предикаты для разных типов токенов
    public static final Predicate<Character> WORD_PREDICATE = ch ->
            Character.isLetter(ch) || 
            ch == '\'' || 
            Character.getType(ch) == Character.DASH_PUNCTUATION;
    
    public static final Predicate<Character> NUMBER_PREDICATE = ch ->
            Character.isDigit(ch) || ch == '-';
    
    public static final Predicate<Character> WHITESPACE_PREDICATE = Character::isWhitespace;
    
    public TextScanner(Reader reader) {
        this(reader, DEFAULT_BUFFER_SIZE);
    }
    
    public TextScanner(Reader reader, int bufferSize) {
        this.reader = new BufferedReader(reader);
        this.buffer = new char[bufferSize];
        this.bufferPos = 0;
        this.bufferSize = 0;
        this.closed = false;
        this.currentPosition = 0;
        this.currentLine = 1;
        this.currentColumn = 1;
        this.lastCharWasNewline = false;
    }
    
    public TextScanner(InputStream inputStream) {
        this(new InputStreamReader(inputStream, StandardCharsets.UTF_8));
    }
    
    public TextScanner(String text) {
        this(new StringReader(text));
    }
    
    /**
     * Основной метод чтения следующего токена
     */
    public Token nextToken() throws IOException {
        if (closed) {
            throw new IllegalStateException("Сканер закрыт");
        }
        
        skipWhitespace();
        
        if (bufferPos >= bufferSize) {
            if (!fillBuffer()) {
                return new Token(TokenType.EOF, "", null, currentPosition, currentLine, currentColumn);
            }
        }
        
        if (bufferPos >= bufferSize) {
            return new Token(TokenType.EOF, "", null, currentPosition, currentLine, currentColumn);
        }
        
        char firstChar = buffer[bufferPos];
        int startPos = currentPosition;
        int startLine = currentLine;
        int startColumn = currentColumn;
        
        // Определяем тип токена по первому символу
        if (firstChar == '\n') {
            bufferPos++;
            currentPosition++;
            currentLine++;
            currentColumn = 1;
            lastCharWasNewline = true;
            return new Token(TokenType.NEWLINE, "\n", "\n", startPos, startLine, startColumn);
        }
        
        Predicate<Character> predicate;
        TokenType type;
        
        if (WORD_PREDICATE.test(firstChar)) {
            predicate = WORD_PREDICATE;
            type = TokenType.WORD;
        } else if (NUMBER_PREDICATE.test(firstChar)) {
            predicate = NUMBER_PREDICATE;
            type = TokenType.INTEGER;
        } else {
            // Знак препинания или другой символ
            bufferPos++;
            currentPosition++;
            currentColumn++;
            return new Token(TokenType.PUNCTUATION, String.valueOf(firstChar), String.valueOf(firstChar), 
                           startPos, startLine, startColumn);
        }
        
        // Читаем весь токен
        StringBuilder tokenBuilder = new StringBuilder();
        
        while (true) {
            if (bufferPos >= bufferSize) {
                if (!fillBuffer()) {
                    break;
                }
            }
            
            if (bufferPos >= bufferSize) {
                break;
            }
            
            char ch = buffer[bufferPos];
            
            if (!predicate.test(ch)) {
                break;
            }
            
            tokenBuilder.append(ch);
            bufferPos++;
            currentPosition++;
            
            if (type == TokenType.WORD) {
                currentColumn++;
            } else {
                // Для чисел проверяем корректность
                if (ch == '-' && tokenBuilder.length() > 1) {
                    // Минус не в начале числа - откатываем
                    tokenBuilder.deleteCharAt(tokenBuilder.length() - 1);
                    bufferPos--;
                    currentPosition--;
                    break;
                }
                currentColumn++;
            }
            
            // Защита от слишком длинных токенов
            if (tokenBuilder.length() > MAX_TOKEN_LENGTH) {
                throw new IOException("Слишком длинный токен");
            }
        }
        
        String tokenValue = tokenBuilder.toString();
        
        // Проверка корректности числа
        if (type == TokenType.INTEGER) {
            if (!isValidNumber(tokenValue)) {
                // Если токен не является корректным числом, пробуем прочитать следующий
                resetToPosition(startPos, startLine, startColumn);
                return nextToken();
            }
        }
        
        return new Token(type, tokenValue, tokenValue, startPos, startLine, startColumn);
    }
    
    /**
     * Читает следующее слово
     */
    public String nextWord() throws IOException {
        while (true) {
            Token token = nextToken();
            if (token.getType() == TokenType.EOF) {
                return null;
            }
            if (token.getType() == TokenType.WORD) {
                return (String) token.getValue();
            }
        }
    }
    
    /**
     * Читает следующее число
     */
    public Integer nextInt() throws IOException {
        while (true) {
            Token token = nextToken();
            if (token.getType() == TokenType.EOF) {
                return null;
            }
            if (token.getType() == TokenType.INTEGER) {
                try {
                    return Integer.parseInt((String) token.getValue());
                } catch (NumberFormatException e) {
                    // Пропускаем некорректное число
                    continue;
                }
            }
        }
    }
    
    /**
     * Проверяет наличие следующего токена указанного типа
     */
    public boolean hasNext(Predicate<Character> predicate) throws IOException {
        if (closed) {
            return false;
        }
        
        // Сохраняем текущее состояние
        int savedBufferPos = bufferPos;
        int savedBufferSize = bufferSize;
        int savedPosition = currentPosition;
        int savedLine = currentLine;
        int savedColumn = currentColumn;
        boolean savedLastCharWasNewline = lastCharWasNewline;
        
        try {
            skipWhitespace();
            
            if (bufferPos >= bufferSize) {
                if (!fillBuffer()) {
                    return false;
                }
            }
            
            if (bufferPos >= bufferSize) {
                return false;
            }
            
            char ch = buffer[bufferPos];
            return predicate.test(ch);
        } finally {
            // Восстанавливаем состояние
            bufferPos = savedBufferPos;
            bufferSize = savedBufferSize;
            currentPosition = savedPosition;
            currentLine = savedLine;
            currentColumn = savedColumn;
            lastCharWasNewline = savedLastCharWasNewline;
        }
    }
    
    public boolean hasNextWord() throws IOException {
        return hasNext(WORD_PREDICATE);
    }
    
    public boolean hasNextInt() throws IOException {
        return hasNext(NUMBER_PREDICATE);
    }
    
    /**
     * Пропускает пробельные символы
     */
    private void skipWhitespace() throws IOException {
        while (true) {
            if (bufferPos >= bufferSize) {
                if (!fillBuffer()) {
                    return;
                }
            }
            
            if (bufferPos >= bufferSize) {
                return;
            }
            
            char ch = buffer[bufferPos];
            
            if (!WHITESPACE_PREDICATE.test(ch) || ch == '\n') {
                return;
            }
            
            bufferPos++;
            currentPosition++;
            
            if (lastCharWasNewline) {
                currentColumn = 1;
                lastCharWasNewline = false;
            } else {
                currentColumn++;
            }
        }
    }
    
    /**
     * Заполняет буфер данными
     */
    private boolean fillBuffer() throws IOException {
        if (closed) {
            return false;
        }
        
        bufferSize = reader.read(buffer);
        bufferPos = 0;
        
        return bufferSize > 0;
    }
    
    /**
     * Проверяет корректность числа
     */
    private boolean isValidNumber(String token) {
        if (token.isEmpty()) {
            return false;
        }
        
        // Проверяем, что минус только в начале
        if (token.indexOf('-', 1) != -1) {
            return false;
        }
        
        // Проверяем, что после минуса есть цифры
        if (token.startsWith("-")) {
            if (token.length() == 1) {
                return false;
            }
            for (int i = 1; i < token.length(); i++) {
                if (!Character.isDigit(token.charAt(i))) {
                    return false;
                }
            }
        } else {
            // Проверяем, что все символы - цифры
            for (int i = 0; i < token.length(); i++) {
                if (!Character.isDigit(token.charAt(i))) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
    /**
     * Возвращает сканер в указанную позицию
     */
    private void resetToPosition(int position, int line, int column) {
        // Эта реализация упрощенная, в реальности нужно переоткрыть поток
        currentPosition = position;
        currentLine = line;
        currentColumn = column;
    }
    
    @Override
    public void close() throws IOException {
        if (!closed) {
            closed = true;
            reader.close();
        }
    }
    
    public boolean isClosed() {
        return closed;
    }
    
    public int getCurrentLine() {
        return currentLine;
    }
    
    public int getCurrentColumn() {
        return currentColumn;
    }
    
    public int getCurrentPosition() {
        return currentPosition;
    }
    
    /**
     * Читает следующую строку
     */
    public String nextLine() throws IOException {
        StringBuilder line = new StringBuilder();
        
        while (true) {
            if (bufferPos >= bufferSize) {
                if (!fillBuffer()) {
                    // Конец файла
                    if (line.length() > 0) {
                        break;
                    } else {
                        return null;
                    }
                }
            }
            
            if (bufferPos >= bufferSize) {
                break;
            }
            
            char ch = buffer[bufferPos];
            bufferPos++;
            currentPosition++;
            
            if (ch == '\n') {
                currentLine++;
                currentColumn = 1;
                lastCharWasNewline = true;
                break;
            } else if (ch == '\r') {
                // Проверяем следующий символ
                if (bufferPos < bufferSize) {
                    if (buffer[bufferPos] == '\n') {
                        bufferPos++;
                        currentPosition++;
                    }
                }
                currentLine++;
                currentColumn = 1;
                lastCharWasNewline = true;
                break;
            } else {
                line.append(ch);
                currentColumn++;
                lastCharWasNewline = false;
            }
        }
        
        return line.toString();
    }
    
    @Override
    public String toString() {
        return String.format("TextScanner[pos=%d, line=%d, col=%d, closed=%s]",
                currentPosition, currentLine, currentColumn, closed);
    }
}