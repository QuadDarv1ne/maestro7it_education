package analyzer.scanner;

import java.io.Serializable;
import java.text.NumberFormat;
import java.util.Objects;

/**
 * Класс, представляющий токен с полной информацией и поддержкой сериализации
 */
public class Token implements Serializable, Comparable<Token> {
    private static final long serialVersionUID = 1L;
    
    private final TokenType type;
    private final String lexeme;
    private final Object value;
    private final int position;
    private final int line;
    private final int column;
    private final String sourceFile;
    private final long timestamp;
    
    /**
     * Конструктор токена
     */
    public Token(TokenType type, String lexeme, Object value, 
                 int position, int line, int column) {
        this(type, lexeme, value, position, line, column, null);
    }
    
    public Token(TokenType type, String lexeme, Object value,
                 int position, int line, int column, String sourceFile) {
        this.type = Objects.requireNonNull(type, "Тип токена не может быть null");
        this.lexeme = Objects.requireNonNull(lexeme, "Лексема не может быть null");
        this.value = value;
        this.position = position;
        this.line = line;
        this.column = column;
        this.sourceFile = sourceFile;
        this.timestamp = System.currentTimeMillis();
        
        validate();
    }
    
    /**
     * Валидация токена
     */
    private void validate() {
        if (position < 0) {
            throw new IllegalArgumentException("Позиция не может быть отрицательной: " + position);
        }
        if (line < 1) {
            throw new IllegalArgumentException("Номер строки должен быть >= 1: " + line);
        }
        if (column < 1) {
            throw new IllegalArgumentException("Номер колонки должен быть >= 1: " + column);
        }
    }
    
    // === ОСНОВНЫЕ ГЕТТЕРЫ ===
    
    public TokenType getType() { return type; }
    public String getLexeme() { return lexeme; }
    public Object getValue() { return value; }
    public int getPosition() { return position; }
    public int getLine() { return line; }
    public int getColumn() { return column; }
    public String getSourceFile() { return sourceFile; }
    public long getTimestamp() { return timestamp; }
    
    // === ПРОВЕРКИ ТИПА ===
    
    public boolean isWord() { return type.isWord(); }
    public boolean isNumber() { return type.isNumber(); }
    public boolean isInteger() { return type.isInteger(); }
    public boolean isFloat() { return type.isFloat(); }
    public boolean isString() { return type.isString(); }
    public boolean isLiteral() { return type.isLiteral(); }
    public boolean isWhitespace() { return type.isWhitespace(); }
    public boolean isPunctuation() { return type.isPunctuation(); }
    public boolean isBracket() { return type.isBracket(); }
    public boolean isQuote() { return type.isQuote(); }
    public boolean isOperator() { return type.isOperator(); }
    public boolean isSymbol() { return type.isSymbol(); }
    public boolean isSpecial() { return type.isSpecial(); }
    public boolean isSignificant() { return type.isSignificant(); }
    public boolean isSeparator() { return type.isSeparator(); }
    public boolean isEOF() { return type == TokenType.EOF; }
    public boolean isError() { return type == TokenType.ERROR; }
    public boolean isUnknown() { return type == TokenType.UNKNOWN; }
    
    // === МЕТОДЫ ДЛЯ ПОЛУЧЕНИЯ ЗНАЧЕНИЙ ===
    
    /**
     * Возвращает строковое значение токена
     */
    public String getStringValue() {
        if (value != null) {
            return value.toString();
        }
        return lexeme;
    }
    
    /**
     * Возвращает целочисленное значение
     */
    public Integer getIntValue() {
        if (value instanceof Integer) {
            return (Integer) value;
        } else if (value instanceof Number) {
            return ((Number) value).intValue();
        } else if (value instanceof String && type.isNumber()) {
            try {
                return Integer.parseInt((String) value);
            } catch (NumberFormatException e) {
                return null;
            }
        } else if (type.isInteger()) {
            try {
                return Integer.parseInt(lexeme);
            } catch (NumberFormatException e) {
                return null;
            }
        }
        return null;
    }
    
    /**
     * Возвращает значение с плавающей точкой
     */
    public Double getDoubleValue() {
        if (value instanceof Double) {
            return (Double) value;
        } else if (value instanceof Number) {
            return ((Number) value).doubleValue();
        } else if (value instanceof String && type.isNumber()) {
            try {
                return Double.parseDouble((String) value);
            } catch (NumberFormatException e) {
                return null;
            }
        } else if (type.isFloat()) {
            try {
                return Double.parseDouble(lexeme);
            } catch (NumberFormatException e) {
                return null;
            }
        }
        return null;
    }
    
    /**
     * Возвращает значение как Number
     */
    public Number getNumberValue() {
        if (value instanceof Number) {
            return (Number) value;
        } else if (type.isInteger()) {
            return getIntValue();
        } else if (type.isFloat()) {
            return getDoubleValue();
        }
        return null;
    }
    
    /**
     * Возвращает длину лексемы
     */
    public int length() {
        return lexeme.length();
    }
    
    /**
     * Возвращает символ по индексу
     */
    public char charAt(int index) {
        return lexeme.charAt(index);
    }
    
    // === ПРЕОБРАЗОВАНИЕ РЕГИСТРА ===
    
    public String toLowerCase() {
        return lexeme.toLowerCase();
    }
    
    public String toUpperCase() {
        return lexeme.toUpperCase();
    }
    
    /**
     * Возвращает нормализованную форму слова
     */
    public String getNormalized() {
        if (isWord()) {
            return lexeme.toLowerCase();
        }
        return lexeme;
    }
    
    // === ИНФОРМАЦИЯ О МЕСТОПОЛОЖЕНИИ ===
    
    /**
     * Возвращает локацию в формате "строка:колонка"
     */
    public String getLocation() {
        return String.format("%d:%d", line, column);
    }
    
    /**
     * Возвращает полную локацию с именем файла
     */
    public String getFullLocation() {
        if (sourceFile != null) {
            return String.format("%s:%d:%d", sourceFile, line, column);
        }
        return getLocation();
    }
    
    /**
     * Проверяет, находится ли токен в указанном диапазоне строк
     */
    public boolean isInLineRange(int startLine, int endLine) {
        return line >= startLine && line <= endLine;
    }
    
    /**
     * Проверяет, находится ли токен в указанном диапазоне колонок
     */
    public boolean isInColumnRange(int startCol, int endCol) {
        return column >= startCol && column <= endCol;
    }
    
    /**
     * Возвращает позицию конца токена
     */
    public int getEndPosition() {
        return position + lexeme.length();
    }
    
    /**
     * Возвращает колонку конца токена
     */
    public int getEndColumn() {
        return column + lexeme.length();
    }
    
    // === ФОРМАТИРОВАНИЕ ===
    
    /**
     * Простое форматирование
     */
    public String format() {
        return String.format("%s '%s'", type.name(), lexeme);
    }
    
    /**
     * Форматирование с значением
     */
    public String formatWithValue() {
        if (value != null && !lexeme.equals(value.toString())) {
            return String.format("%s '%s' = %s", type.name(), lexeme, value);
        }
        return format();
    }
    
    /**
     * Подробное форматирование с локацией
     */
    public String formatDetailed() {
        return String.format("%s '%s' at %s (pos %d)", 
                type.name(), lexeme, getLocation(), position);
    }
    
    /**
     * Форматирование для отладки
     */
    public String formatDebug() {
        StringBuilder sb = new StringBuilder();
        sb.append("Token {\n");
        sb.append("  type: ").append(type).append("\n");
        sb.append("  lexeme: '").append(lexeme).append("'\n");
        sb.append("  value: ").append(value).append("\n");
        sb.append("  position: ").append(position).append("\n");
        sb.append("  location: ").append(getFullLocation()).append("\n");
        sb.append("  timestamp: ").append(timestamp).append("\n");
        sb.append("}");
        return sb.toString();
    }
    
    @Override
    public String toString() {
        return formatDetailed();
    }
    
    // === СРАВНЕНИЕ И РАВЕНСТВО ===
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        
        Token other = (Token) obj;
        return type == other.type &&
               lexeme.equals(other.lexeme) &&
               position == other.position &&
               line == other.line &&
               column == other.column &&
               Objects.equals(sourceFile, other.sourceFile);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(type, lexeme, position, line, column, sourceFile);
    }
    
    @Override
    public int compareTo(Token other) {
        if (this.line != other.line) {
            return Integer.compare(this.line, other.line);
        }
        if (this.column != other.column) {
            return Integer.compare(this.column, other.column);
        }
        return Integer.compare(this.position, other.position);
    }
    
    // === СТАТИЧЕСКИЕ ФАБРИЧНЫЕ МЕТОДЫ ===
    
    public static Token word(String word, int position, int line, int column) {
        return new Token(TokenType.WORD, word, word.toLowerCase(), 
                        position, line, column);
    }
    
    public static Token word(String word, int position, int line, int column, String sourceFile) {
        return new Token(TokenType.WORD, word, word.toLowerCase(), 
                        position, line, column, sourceFile);
    }
    
    public static Token integer(String number, int position, int line, int column) {
        Integer value = null;
        try {
            value = Integer.parseInt(number);
        } catch (NumberFormatException e) {
            // Значение останется null
        }
        return new Token(TokenType.INTEGER, number, value, position, line, column);
    }
    
    public static Token integer(int number, int position, int line, int column) {
        return new Token(TokenType.INTEGER, String.valueOf(number), number, 
                        position, line, column);
    }
    
    public static Token floatNumber(String number, int position, int line, int column) {
        Double value = null;
        try {
            value = Double.parseDouble(number);
        } catch (NumberFormatException e) {
            // Значение останется null
        }
        return new Token(TokenType.FLOAT, number, value, position, line, column);
    }
    
    public static Token floatNumber(double number, int position, int line, int column) {
        return new Token(TokenType.FLOAT, String.valueOf(number), number, 
                        position, line, column);
    }
    
    public static Token string(String text, int position, int line, int column) {
        return new Token(TokenType.STRING, "\"" + text + "\"", text, 
                        position, line, column);
    }
    
    public static Token eof(int position, int line, int column) {
        return new Token(TokenType.EOF, "", null, position, line, column);
    }
    
    public static Token space(int position, int line, int column) {
        return new Token(TokenType.SPACE, " ", null, position, line, column);
    }
    
    public static Token newline(int position, int line, int column) {
        return new Token(TokenType.NEWLINE, "\n", null, position, line, column);
    }
    
    public static Token punctuation(char ch, int position, int line, int column) {
        TokenType type = TokenType.fromChar(ch);
        return new Token(type, String.valueOf(ch), null, position, line, column);
    }
    
    public static Token error(String lexeme, int position, int line, int column) {
        return new Token(TokenType.ERROR, lexeme, null, position, line, column);
    }
    
    // === УТИЛИТНЫЕ МЕТОДЫ ===
    
    /**
     * Проверяет, совпадает ли лексема (без учета регистра)
     */
    public boolean matchesIgnoreCase(String text) {
        return lexeme.equalsIgnoreCase(text);
    }
    
    /**
     * Проверяет, начинается ли лексема с указанного префикса
     */
    public boolean startsWith(String prefix) {
        return lexeme.startsWith(prefix);
    }
    
    /**
     * Проверяет, заканчивается ли лексема указанным суффиксом
     */
    public boolean endsWith(String suffix) {
        return lexeme.endsWith(suffix);
    }
    
    /**
     * Проверяет, содержит ли лексема указанную подстроку
     */
    public boolean contains(String substring) {
        return lexeme.contains(substring);
    }
    
    /**
     * Возвращает подстроку лексемы
     */
    public String substring(int beginIndex) {
        return lexeme.substring(beginIndex);
    }
    
    public String substring(int beginIndex, int endIndex) {
        return lexeme.substring(beginIndex, endIndex);
    }
    
    /**
     * Клонирует токен с новыми координатами
     */
    public Token cloneAt(int newPosition, int newLine, int newColumn) {
        return new Token(type, lexeme, value, newPosition, newLine, newColumn, sourceFile);
    }
    
    /**
     * Клонирует токен с новым значением
     */
    public Token cloneWithValue(Object newValue) {
        return new Token(type, lexeme, newValue, position, line, column, sourceFile);
    }
    
    /**
     * Клонирует токен с новым типом
     */
    public Token cloneWithType(TokenType newType) {
        return new Token(newType, lexeme, value, position, line, column, sourceFile);
    }
    
    // === СТАТИЧЕСКИЕ МЕТОДЫ ДЛЯ СРАВНЕНИЯ ===
    
    public static boolean areAdjacent(Token first, Token second) {
        if (first == null || second == null) return false;
        return first.getEndPosition() == second.getPosition();
    }
    
    public static int distance(Token first, Token second) {
        if (first == null || second == null) return -1;
        return Math.abs(first.getPosition() - second.getPosition());
    }
    
    /**
     * Проверяет, образуют ли два токена пару скобок
     */
    public static boolean isBracketPair(Token opening, Token closing) {
        if (opening == null || closing == null) return false;
        if (!opening.isBracket() || !closing.isBracket()) return false;
        
        TokenType matchingType = opening.getType().getMatchingBracket();
        return matchingType == closing.getType();
    }
}