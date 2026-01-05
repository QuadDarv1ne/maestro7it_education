package analyzer.scanner;

/**
 * Типы токенов с группировкой по категориям
 */
public enum TokenType {
    // === БАЗОВЫЕ ТОКЕНЫ ===
    
    // Литералы (основные для задач)
    WORD,           // Слово (буквы, апострофы, дефисы)
    NUMBER,         // Целое число
    DECIMAL,        // Десятичное число
    TEXT,           // Текст (строка)
    
    // === РАЗДЕЛИТЕЛИ ===
    
    // Пробельные символы
    SPACE,          // Пробел
    TAB,            // Табуляция
    NEWLINE,        // Перевод строки (\n)
    CARRIAGE_RETURN,// Возврат каретки (\r)
    
    // Знаки препинания
    COMMA,          // ,
    DOT,            // .
    COLON,          // :
    SEMICOLON,      // ;
    EXCLAMATION,    // !
    QUESTION,       // ?
    ELLIPSIS,       // ...
    DASH,           // — (длинное тире)
    HYPHEN,         // - (дефис)
    
    // === СКОБКИ И КАВЫЧКИ ===
    
    // Круглые скобки
    LPAREN,         // (
    RPAREN,         // )
    
    // Квадратные скобки
    LBRACKET,       // [
    RBRACKET,       // ]
    
    // Фигурные скобки
    LBRACE,         // {
    RBRACE,         // }
    
    // Угловые скобки
    LANGLE,         // <
    RANGLE,         // >
    
    // Кавычки
    QUOTE_DOUBLE,   // "
    QUOTE_SINGLE,   // '
    QUOTE_BACKTICK, // `
    
    // === МАТЕМАТИЧЕСКИЕ СИМВОЛЫ ===
    
    // Арифметические операторы
    PLUS,           // +
    MINUS,          // -
    MULTIPLY,       // *
    DIVIDE,         // /
    MODULO,         // %
    POWER,          // ^
    
    // Операторы сравнения
    EQUAL,          // =
    NOT_EQUAL,      // !=
    GREATER,        // >
    LESS,           // <
    GREATER_EQUAL,  // >=
    LESS_EQUAL,     // <=
    
    // === ЛОГИЧЕСКИЕ ОПЕРАТОРЫ ===
    AND,            // &&
    OR,             // ||
    NOT,            // !
    
    // === СПЕЦИАЛЬНЫЕ ===
    EOF,            // Конец файла
    ERROR,          // Ошибка/неизвестный символ
    COMMENT,        // Комментарий
    DIRECTIVE       // Директива/команда
}