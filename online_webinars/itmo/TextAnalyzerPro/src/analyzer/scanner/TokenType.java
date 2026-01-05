package analyzer.scanner;

/**
 * Типы токенов с расширенной функциональностью и поддержкой категорий
 */
public enum TokenType {
    // === ОСНОВНЫЕ ТОКЕНЫ ===
    WORD("Слово", Category.LITERAL),
    INTEGER("Целое число", Category.LITERAL),
    FLOAT("Десятичное число", Category.LITERAL),
    STRING("Строка", Category.LITERAL),
    PUNCTUATION("Знак препинания", Category.PUNCTUATION),
    
    // === ПРОБЕЛЬНЫЕ СИМВОЛЫ ===
    SPACE("Пробел", Category.WHITESPACE),
    TAB("Табуляция", Category.WHITESPACE),
    NEWLINE("Новая строка", Category.WHITESPACE),
    CARRIAGE_RETURN("Возврат каретки", Category.WHITESPACE),
    
    // === ЗНАКИ ПРЕПИНАНИЯ ===
    COMMA("Запятая", Category.PUNCTUATION),
    DOT("Точка", Category.PUNCTUATION),
    COLON("Двоеточие", Category.PUNCTUATION),
    SEMICOLON("Точка с запятой", Category.PUNCTUATION),
    EXCLAMATION("Восклицательный знак", Category.PUNCTUATION),
    QUESTION("Вопросительный знак", Category.PUNCTUATION),
    ELLIPSIS("Многоточие", Category.PUNCTUATION),
    HYPHEN("Дефис", Category.PUNCTUATION),
    DASH("Тире", Category.PUNCTUATION),
    SLASH("Слэш", Category.PUNCTUATION),
    BACKSLASH("Обратный слэш", Category.PUNCTUATION),
    VERTICAL_BAR("Вертикальная черта", Category.PUNCTUATION),
    
    // === СКОБКИ ===
    LEFT_PAREN("Левая круглая скобка", Category.BRACKET),
    RIGHT_PAREN("Правая круглая скобка", Category.BRACKET),
    LEFT_BRACKET("Левая квадратная скобка", Category.BRACKET),
    RIGHT_BRACKET("Правая квадратная скобка", Category.BRACKET),
    LEFT_BRACE("Левая фигурная скобка", Category.BRACKET),
    RIGHT_BRACE("Правая фигурная скобка", Category.BRACKET),
    LEFT_ANGLE("Левая угловая скобка", Category.BRACKET),
    RIGHT_ANGLE("Правая угловая скобка", Category.BRACKET),
    
    // === КАВЫЧКИ ===
    QUOTE_DOUBLE("Двойные кавычки", Category.QUOTE),
    QUOTE_SINGLE("Одинарные кавычки", Category.QUOTE),
    QUOTE_BACKTICK("Обратные кавычки", Category.QUOTE),
    
    // === МАТЕМАТИЧЕСКИЕ ОПЕРАТОРЫ ===
    PLUS("Плюс", Category.OPERATOR),
    MINUS("Минус", Category.OPERATOR),
    MULTIPLY("Умножение", Category.OPERATOR),
    DIVIDE("Деление", Category.OPERATOR),
    MODULO("Остаток от деления", Category.OPERATOR),
    EQUAL("Равно", Category.OPERATOR),
    NOT_EQUAL("Не равно", Category.OPERATOR),
    GREATER("Больше", Category.OPERATOR),
    LESS("Меньше", Category.OPERATOR),
    GREATER_EQUAL("Больше или равно", Category.OPERATOR),
    LESS_EQUAL("Меньше или равно", Category.OPERATOR),
    
    // === ЛОГИЧЕСКИЕ ОПЕРАТОРЫ ===
    AND("Логическое И", Category.OPERATOR),
    OR("Логическое ИЛИ", Category.OPERATOR),
    NOT("Логическое НЕ", Category.OPERATOR),
    
    // === ПРОЧИЕ СИМВОЛЫ ===
    AT("Символ @", Category.SYMBOL),
    HASH("Символ #", Category.SYMBOL),
    DOLLAR("Символ $", Category.SYMBOL),
    PERCENT("Символ %", Category.SYMBOL),
    CARET("Символ ^", Category.SYMBOL),
    AMPERSAND("Символ &", Category.SYMBOL),
    ASTERISK("Символ *", Category.SYMBOL),
    UNDERSCORE("Нижнее подчеркивание", Category.SYMBOL),
    TILDE("Тильда", Category.SYMBOL),
    
    // === СПЕЦИАЛЬНЫЕ ТОКЕНЫ ===
    EOF("Конец файла", Category.SPECIAL),
    ERROR("Ошибка", Category.SPECIAL),
    COMMENT("Комментарий", Category.SPECIAL),
    UNKNOWN("Неизвестный символ", Category.SPECIAL);
    
    private final String description;
    private final Category category;
    
    TokenType(String description, Category category) {
        this.description = description;
        this.category = category;
    }
    
    public String getDescription() {
        return description;
    }
    
    public Category getCategory() {
        return category;
    }
    
    // === МЕТОДЫ ПРОВЕРКИ КАТЕГОРИЙ ===
    
    public boolean isLiteral() {
        return category == Category.LITERAL;
    }
    
    public boolean isWord() {
        return this == WORD;
    }
    
    public boolean isNumber() {
        return this == INTEGER || this == FLOAT;
    }
    
    public boolean isInteger() {
        return this == INTEGER;
    }
    
    public boolean isFloat() {
        return this == FLOAT;
    }
    
    public boolean isString() {
        return this == STRING;
    }
    
    public boolean isWhitespace() {
        return category == Category.WHITESPACE;
    }
    
    public boolean isPunctuation() {
        return category == Category.PUNCTUATION;
    }
    
    public boolean isBracket() {
        return category == Category.BRACKET;
    }
    
    public boolean isQuote() {
        return category == Category.QUOTE;
    }
    
    public boolean isOperator() {
        return category == Category.OPERATOR;
    }
    
    public boolean isSymbol() {
        return category == Category.SYMBOL;
    }
    
    public boolean isSpecial() {
        return category == Category.SPECIAL;
    }
    
    public boolean isSignificant() {
        // Токены, которые имеют значение для анализа
        return isLiteral() || isPunctuation() || isBracket() || 
               isQuote() || isOperator() || isSymbol();
    }
    
    public boolean isSeparator() {
        // Токены, которые разделяют другие токены
        return isWhitespace() || this == COMMA || this == SEMICOLON || 
               this == COLON || this == DOT;
    }
    
    // === ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ===
    
    /**
     * Возвращает открывающую скобку для закрывающей или null
     */
    public TokenType getMatchingBracket() {
        switch (this) {
            case RIGHT_PAREN: return LEFT_PAREN;
            case RIGHT_BRACKET: return LEFT_BRACKET;
            case RIGHT_BRACE: return LEFT_BRACE;
            case RIGHT_ANGLE: return LEFT_ANGLE;
            case LEFT_PAREN: return RIGHT_PAREN;
            case LEFT_BRACKET: return RIGHT_BRACKET;
            case LEFT_BRACE: return RIGHT_BRACE;
            case LEFT_ANGLE: return RIGHT_ANGLE;
            default: return null;
        }
    }
    
    /**
     * Проверяет, является ли токен открывающей скобкой
     */
    public boolean isOpeningBracket() {
        return this == LEFT_PAREN || this == LEFT_BRACKET || 
               this == LEFT_BRACE || this == LEFT_ANGLE;
    }
    
    /**
     * Проверяет, является ли токен закрывающей скобкой
     */
    public boolean isClosingBracket() {
        return this == RIGHT_PAREN || this == RIGHT_BRACKET || 
               this == RIGHT_BRACE || this == RIGHT_ANGLE;
    }
    
    /**
     * Возвращает приоритет оператора (для математических выражений)
     */
    public int getOperatorPrecedence() {
        switch (this) {
            case NOT: return 7;
            case MULTIPLY:
            case DIVIDE:
            case MODULO: return 6;
            case PLUS:
            case MINUS: return 5;
            case GREATER:
            case LESS:
            case GREATER_EQUAL:
            case LESS_EQUAL: return 4;
            case EQUAL:
            case NOT_EQUAL: return 3;
            case AND: return 2;
            case OR: return 1;
            default: return 0;
        }
    }
    
    /**
     * Проверяет, является ли оператор унарным
     */
    public boolean isUnaryOperator() {
        return this == PLUS || this == MINUS || this == NOT;
    }
    
    /**
     * Проверяет, является ли оператор бинарным
     */
    public boolean isBinaryOperator() {
        return getOperatorPrecedence() > 0 && !isUnaryOperator();
    }
    
    @Override
    public String toString() {
        return String.format("%s (%s, %s)", name(), description, category);
    }
    
    // === ВЛОЖЕННЫЕ КЛАССЫ ===
    
    /**
     * Категории токенов для группировки
     */
    public enum Category {
        LITERAL("Литерал"),
        WHITESPACE("Пробельный символ"),
        PUNCTUATION("Знак препинания"),
        BRACKET("Скобка"),
        QUOTE("Кавычки"),
        OPERATOR("Оператор"),
        SYMBOL("Символ"),
        SPECIAL("Специальный");
        
        private final String description;
        
        Category(String description) {
            this.description = description;
        }
        
        public String getDescription() {
            return description;
        }
    }
    
    // === СТАТИЧЕСКИЕ МЕТОДЫ ===
    
    /**
     * Определяет тип токена по символу
     */
    public static TokenType fromChar(char ch) {
        switch (ch) {
            case ' ': return SPACE;
            case '\t': return TAB;
            case '\n': return NEWLINE;
            case '\r': return CARRIAGE_RETURN;
            case ',': return COMMA;
            case '.': return DOT;
            case ':': return COLON;
            case ';': return SEMICOLON;
            case '!': return EXCLAMATION;
            case '?': return QUESTION;
            case '-': return HYPHEN;
            case '\\': return BACKSLASH;
            case '|': return VERTICAL_BAR;
            case '(': return LEFT_PAREN;
            case ')': return RIGHT_PAREN;
            case '[': return LEFT_BRACKET;
            case ']': return RIGHT_BRACKET;
            case '{': return LEFT_BRACE;
            case '}': return RIGHT_BRACE;
            case '<': return LEFT_ANGLE;
            case '>': return RIGHT_ANGLE;
            case '"': return QUOTE_DOUBLE;
            case '\'': return QUOTE_SINGLE;
            case '`': return QUOTE_BACKTICK;
            case '+': return PLUS;
            case '*': return ASTERISK;
            case '/': return SLASH;
            case '%': return PERCENT;
            case '=': return EQUAL;
            case '@': return AT;
            case '#': return HASH;
            case '$': return DOLLAR;
            case '^': return CARET;
            case '&': return AMPERSAND;
            case '_': return UNDERSCORE;
            case '~': return TILDE;
            default: 
                if (Character.isLetter(ch)) return WORD;
                if (Character.isDigit(ch)) return INTEGER;
                return UNKNOWN;
        }
    }
    
    /**
     * Определяет, является ли символ частью слова
     */
    public static boolean isWordChar(char ch) {
        return Character.isLetter(ch) || 
               ch == '\'' || ch == '’' || ch == 'ʻ' ||
               Character.getType(ch) == Character.DASH_PUNCTUATION;
    }
    
    /**
     * Определяет, является ли символ частью числа
     */
    public static boolean isNumberChar(char ch) {
        return Character.isDigit(ch) || ch == '-' || ch == '+' || ch == '.';
    }
    
    /**
     * Определяет, является ли символ пробельным
     */
    public static boolean isWhitespaceChar(char ch) {
        return Character.isWhitespace(ch) || 
               ch == '\n' || ch == '\r' || ch == '\t' || ch == ' ';
    }
    
    /**
     * Определяет, является ли символ разделителем
     */
    public static boolean isSeparatorChar(char ch) {
        return isWhitespaceChar(ch) || ch == ',' || ch == ';' || ch == ':';
    }
    
    /**
     * Определяет, является ли символ оператором
     */
    public static boolean isOperatorChar(char ch) {
        return ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '%' ||
               ch == '=' || ch == '!' || ch == '<' || ch == '>' || ch == '&' || ch == '|';
    }
    
    /**
     * Определяет, является ли символ скобкой
     */
    public static boolean isBracketChar(char ch) {
        return ch == '(' || ch == ')' || ch == '[' || ch == ']' || 
               ch == '{' || ch == '}' || ch == '<' || ch == '>';
    }
    
    /**
     * Определяет, является ли символ кавычкой
     */
    public static boolean isQuoteChar(char ch) {
        return ch == '"' || ch == '\'' || ch == '`';
    }
}