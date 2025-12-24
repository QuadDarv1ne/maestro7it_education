/**
 * @file ExpressionParser.java
 * @brief Парсер арифметических выражений с переменными методом рекурсивного спуска
 * 
 * Программа разбирает арифметические выражения, содержащие:
 * - бинарные операции: *, /, +, -
 * - унарный минус: -
 * - переменные: $0, $1, ...
 * - целочисленные константы в 32-битном диапазоне
 * - круглые скобки для задания приоритета
 * - пробелы между токенами
 * 
 * Приоритет операций (от высшего к низшему):
 * 1. Унарный минус
 * 2. Умножение и деление
 * 3. Сложение и вычитание
 * 
 * Алгоритм:
 * Используется метод рекурсивного спуска, который строит абстрактное
 * синтаксическое дерево (AST). Каждый узел дерева представляет собой:
 * - константу (Constant)
 * - переменную (Variable)
 * - бинарную операцию (BinaryOperation)
 * - унарный минус (UnaryMinus)
 * 
 * Пример выражения: "$0 * ($0 - 2)*$0 + 1"
 * 
 * При вычислении переменные $0, $1, ... заменяются на значение x,
 * переданное в метод evaluate().
 * 
 * Сложность алгоритма: O(n), где n - длина входной строки.
 * 
 * Обработка ошибок:
 * - Синтаксические ошибки в выражении
 * - Деление на ноль при вычислении
 * - Константы вне 32-битного диапазона
 * 
 * Формат ввода:
 * Каждая строка содержит одно выражение.
 * Программа вычисляет значение выражения для x от 0 до 10.
 */

import java.io.*;
import java.util.*;

/**
 * @brief Абстрактный базовый класс для всех выражений
 */
abstract class Expression {
    /**
     * @brief Вычисляет значение выражения
     * @param x Значение переменной
     * @return Результат вычисления
     */
    public abstract int evaluate(int x);
}

/**
 * @brief Класс для представления целочисленной константы
 */
class Constant extends Expression {
    private final int value;
    
    public Constant(int value) {
        this.value = value;
    }
    
    @Override
    public int evaluate(int x) {
        return value;
    }
}

/**
 * @brief Класс для представления переменной
 * 
 * Переменные вида $0, $1, ... заменяются на значение x.
 * В текущей реализации все переменные имеют одинаковое значение.
 */
class Variable extends Expression {
    private final int index;
    
    public Variable(int index) {
        this.index = index;
    }
    
    @Override
    public int evaluate(int x) {
        return x; // Все переменные заменяются на x
    }
}

/**
 * @brief Класс для представления бинарной операции
 * 
 * Поддерживает операции: +, -, *, /
 */
class BinaryOperation extends Expression {
    private final char op;
    private final Expression left;
    private final Expression right;
    
    public BinaryOperation(char op, Expression left, Expression right) {
        this.op = op;
        this.left = left;
        this.right = right;
    }
    
    @Override
    public int evaluate(int x) {
        int l = left.evaluate(x);
        int r = right.evaluate(x);
        switch (op) {
            case '+':
                return l + r;
            case '-':
                return l - r;
            case '*':
                return l * r;
            case '/':
                if (r == 0) {
                    throw new ArithmeticException("Division by zero");
                }
                return l / r;
            default:
                throw new IllegalArgumentException("Unknown operation: " + op);
        }
    }
}

/**
 * @brief Класс для представления унарного минуса
 */
class UnaryMinus extends Expression {
    private final Expression expr;
    
    public UnaryMinus(Expression expr) {
        this.expr = expr;
    }
    
    @Override
    public int evaluate(int x) {
        return -expr.evaluate(x);
    }
}

/**
 * @brief Парсер выражений методом рекурсивного спуска
 * 
 * Грамматика:
 *   expression  ::= addsub
 *   addsub      ::= muldiv (('+' | '-') muldiv)*
 *   muldiv      ::= unary (('*' | '/') unary)*
 *   unary       ::= '-' unary | primary
 *   primary     ::= '(' expression ')' | '$' number | number
 *   number      ::= digit+
 */
class Parser {
    private final String input;
    private int pos;
    
    /**
     * @brief Конструктор парсера
     * @param input Входная строка с выражением
     */
    public Parser(String input) {
        this.input = input;
        this.pos = 0;
    }
    
    /**
     * @brief Пропускает пробельные символы
     */
    private void skipSpaces() {
        while (pos < input.length() && Character.isWhitespace(input.charAt(pos))) {
            pos++;
        }
    }
    
    /**
     * @brief Возвращает текущий символ без продвижения
     * @return Текущий символ или '\0', если достигнут конец строки
     */
    private char peek() {
        skipSpaces();
        if (pos < input.length()) {
            return input.charAt(pos);
        }
        return '\0';
    }
    
    /**
     * @brief Читает текущий символ с продвижением
     * @return Считанный символ или '\0', если достигнут конец строки
     */
    private char get() {
        skipSpaces();
        if (pos < input.length()) {
            return input.charAt(pos++);
        }
        return '\0';
    }
    
    /**
     * @brief Основной метод разбора выражения
     * @return Корень AST
     * @throws IllegalArgumentException при синтаксической ошибке
     */
    public Expression parse() {
        Expression result = parseExpression();
        skipSpaces();
        if (pos < input.length()) {
            throw new IllegalArgumentException("Unexpected characters at end of input");
        }
        return result;
    }
    
    /**
     * @brief Разбор выражения (стартовая точка)
     * @return Разобранное выражение
     */
    private Expression parseExpression() {
        return parseAddSub();
    }
    
    /**
     * @brief Разбор операций сложения и вычитания
     * 
     * Грамматика: muldiv (('+' | '-') muldiv)*
     * Обрабатывает левую ассоциативность операций.
     */
    private Expression parseAddSub() {
        Expression left = parseMulDiv();
        
        while (true) {
            char op = peek();
            if (op == '+' || op == '-') {
                get();
                Expression right = parseMulDiv();
                left = new BinaryOperation(op, left, right);
            } else {
                break;
            }
        }
        return left;
    }
    
    /**
     * @brief Разбор операций умножения и деления
     * 
     * Грамматика: unary (('*' | '/') unary)*
     * Обрабатывает левую ассоциативность операций.
     */
    private Expression parseMulDiv() {
        Expression left = parseUnary();
        
        while (true) {
            char op = peek();
            if (op == '*' || op == '/') {
                get();
                Expression right = parseUnary();
                left = new BinaryOperation(op, left, right);
            } else {
                break;
            }
        }
        return left;
    }
    
    /**
     * @brief Разбор унарных операций
     * 
     * Грамматика: '-' unary | primary
     * Унарный минус имеет наивысший приоритет.
     */
    private Expression parseUnary() {
        skipSpaces();
        
        if (peek() == '-') {
            get();
            Expression expr = parseUnary();
            return new UnaryMinus(expr);
        }
        
        return parsePrimary();
    }
    
    /**
     * @brief Разбор первичных выражений
     * 
     * Грамматика: '(' expression ')' | '$' number | number
     * Обрабатывает:
     * - выражения в скобках
     * - переменные вида $0, $1, ...
     * - целочисленные константы
     */
    private Expression parsePrimary() {
        skipSpaces();
        char c = get();
        
        // Обработка скобок
        if (c == '(') {
            Expression expr = parseExpression();
            skipSpaces();
            if (get() != ')') {
                throw new IllegalArgumentException("Expected ')'");
            }
            return expr;
        }
        
        // Обработка переменных
        if (c == '$') {
            StringBuilder num = new StringBuilder();
            while (pos < input.length() && Character.isDigit(input.charAt(pos))) {
                num.append(get());
            }
            if (num.length() == 0) {
                throw new IllegalArgumentException("Expected variable index after '$'");
            }
            int index = Integer.parseInt(num.toString());
            return new Variable(index);
        }
        
        // Обработка чисел (может начинаться с цифры, '+' или '-')
        if (Character.isDigit(c) || c == '-' || c == '+') {
            StringBuilder num = new StringBuilder();
            num.append(c);
            while (pos < input.length() && Character.isDigit(input.charAt(pos))) {
                num.append(get());
            }
            
            // Проверка, что это не просто знак
            String numStr = num.toString();
            if (numStr.equals("-") || numStr.equals("+")) {
                throw new IllegalArgumentException("Invalid number format");
            }
            
            // Проверка диапазона 32-битного числа
            try {
                long val = Long.parseLong(numStr);
                if (val < Integer.MIN_VALUE || val > Integer.MAX_VALUE) {
                    throw new IllegalArgumentException("Constant out of 32-bit range");
                }
                return new Constant((int) val);
            } catch (NumberFormatException e) {
                throw new IllegalArgumentException("Invalid number format");
            }
        }
        
        // Неизвестный символ
        throw new IllegalArgumentException("Unexpected character: " + c);
    }
}

/**
 * Основная функция Main() - запуск программы калькулятора
 * @brief Основной класс программы
 * 
 * Читает выражения из стандартного ввода, парсит их и вычисляет
 * значения для x от 0 до 10.
 * 
 * Формат вывода: для каждого x выводится результат через пробел,
 * в случае ошибки - "ERROR" для соответствующего x.
 */
public class ExpressionParser {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        while (scanner.hasNextLine()) {
            String line = scanner.nextLine();
            try {
                Parser parser = new Parser(line);
                Expression expr = parser.parse();
                
                // Вычисление для x от 0 до 10
                StringBuilder result = new StringBuilder();
                for (int x = 0; x <= 10; x++) {
                    try {
                        result.append(expr.evaluate(x)).append(" ");
                    } catch (ArithmeticException e) {
                        result.append("ERROR ");
                    }
                }
                System.out.println(result.toString().trim());
                
            } catch (IllegalArgumentException e) {
                // Синтаксическая ошибка во всем выражении
                System.out.println("ERROR");
            }
        }
        
        scanner.close();
    }
}