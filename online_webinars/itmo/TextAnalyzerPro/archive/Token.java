package analyzer.scanner;

/**
 * Улучшенный класс токена с дополнительной информацией
 */
public class Token {
    private final TokenType type;
    private final String lexeme;     // Строковое представление токена
    private final Object literal;    // Значение для литералов (String, Integer, Double)
    private final int position;      // Позиция в потоке (байт)
    private final int line;          // Номер строки (1-based)
    private final int column;        // Номер столбца (1-based)
    private final String fileName;   // Имя файла (опционально)
    
    public Token(TokenType type, String lexeme, Object literal, 
                 int position, int line, int column) {
        this(type, lexeme, literal, position, line, column, null);
    }
    
    public Token(TokenType type, String lexeme, Object literal,
                 int position, int line, int column, String fileName) {
        this.type = type;
        this.lexeme = lexeme;
        this.literal = literal;
        this.position = position;
        this.line = line;
        this.column = column;
        this.fileName = fileName;
    }
    
    // Геттеры
    public TokenType getType() { return type; }
    public String getLexeme() { return lexeme; }
    public Object getLiteral() { return literal; }
    public int getPosition() { return position; }
    public int getLine() { return line; }
    public int getColumn() { return column; }
    public String getFileName() { return fileName; }
    
    // Вспомогательные методы
    public String getLiteralAsString() {
        return literal != null ? literal.toString() : lexeme;
    }
    
    public Integer getLiteralAsInt() {
        if (literal instanceof Integer) {
            return (Integer) literal;
        } else if (literal instanceof String && type == TokenType.NUMBER) {
            try {
                return Integer.parseInt((String) literal);
            } catch (NumberFormatException e) {
                return null;
            }
        }
        return null;
    }
    
    public Double getLiteralAsDouble() {
        if (literal instanceof Double) {
            return (Double) literal;
        } else if (literal instanceof String && type == TokenType.NUMBER) {
            try {
                return Double.parseDouble((String) literal);
            } catch (NumberFormatException e) {
                return null;
            }
        }
        return null;
    }
    
    public boolean isWord() {
        return type == TokenType.WORD;
    }
    
    public boolean isNumber() {
        return type == TokenType.NUMBER;
    }
    
    public boolean isString() {
        return type == TokenType.STRING;
    }
    
    public boolean isLiteral() {
        return type.isLiteral();
    }
    
    public boolean isWhitespace() {
        return type.isWhitespace();
    }
    
    public boolean isPunctuation() {
        return type.isPunctuation();
    }
    
    public boolean isOperator() {
        return type.isOperator();
    }
    
    public boolean isBracket() {
        return type.isBracket();
    }
    
    public boolean isEOF() {
        return type == TokenType.EOF;
    }
    
    // Форматированный вывод
    public String format() {
        String base = String.format("%s '%s'", type, lexeme);
        if (literal != null && !lexeme.equals(literal.toString())) {
            base += String.format(" (value: %s)", literal);
        }
        return base;
    }
    
    public String formatWithLocation() {
        String location;
        if (fileName != null) {
            location = String.format("%s:%d:%d", fileName, line, column);
        } else {
            location = String.format("%d:%d", line, column);
        }
        return String.format("[%s] %s", location, format());
    }
    
    @Override
    public String toString() {
        return formatWithLocation();
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        
        Token other = (Token) obj;
        return type == other.type &&
               lexeme.equals(other.lexeme) &&
               position == other.position &&
               line == other.line &&
               column == other.column;
    }
    
    @Override
    public int hashCode() {
        int result = type.hashCode();
        result = 31 * result + lexeme.hashCode();
        result = 31 * result + position;
        result = 31 * result + line;
        result = 31 * result + column;
        return result;
    }
}