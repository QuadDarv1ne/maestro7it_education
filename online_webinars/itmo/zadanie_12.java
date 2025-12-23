/* Задание 12. Минимизированная строковая запись выражений
 * Система классов для вычисления арифметических выражений с одной переменной типа int.
 * Реализуйте метод toMiniString, который возвращает минимизированную строковую запись выражения с учётом приоритетов и ассоциативности операций.
 * 
 * Например, для выражения new Add(new Const(2), new Multiply(new Variable("x"), new Const(3)))
 * метод должен вернуть строку "2 + x * 3", а не "(2 + (x * 3))".
 * 
 * Требования:
 * - Классы Const, Variable, Add, Subtract, Multiply, Divide для построения выражений
 * - Метод evaluate(x) - вычисление значения выражения при заданном x
 * - Метод toString() - полноскобочная запись выражения: ((2 * x) - 3)
 * - Метод toMiniString() - запись с минимальным числом скобок: 2 * x - 3
 * - Метод equals() - проверка совпадения двух выражений
 * 
 * Архитектура:
 * - Expression - базовый интерфейс
 * - ToMiniString - интерфейс для минимизированной записи
 * - AbstractExpression - базовый класс для простых выражений
 * - BinaryOperation - абстрактный класс для бинарных операций
 * - Const - класс для констант
 * - Variable - класс для переменных
 */

// Базовый интерфейс для всех выражений
interface Expression extends ToMiniString {
    int evaluate(int x);
}

/**
 * Интерфейс для минимизированной строковой записи выражений.
 * Позволяет получить строковое представление с минимальным количеством скобок.
 */
interface ToMiniString {
    /**
     * Возвращает строковое представление выражения с минимальным числом скобок.
     * @return минимизированная строковая запись
     */
    String toMiniString();
}

/**
 * Абстрактный базовый класс для простых выражений (константы и переменные).
 * Предоставляет реализацию по умолчанию для toMiniString().
 */
abstract class AbstractExpression implements Expression {
    @Override
    public abstract int evaluate(int x);

    @Override
    public abstract String toString();

    @Override
    public String toMiniString() {
        return toString();
    }
}

/**
 * Класс для представления константного значения в выражении.
 * Всегда возвращает одно и то же значение независимо от переменной x.
 */
class Const extends AbstractExpression {
    private final int value;

    /**
     * Создает константу с заданным значением.
     * @param value значение константы
     */
    public Const(int value) {
        this.value = value;
    }

    /**
     * Вычисляет значение константы (не зависит от x).
     * @param x значение переменной (не используется)
     * @return значение константы
     */
    @Override
    public int evaluate(int x) {
        return value;
    }

    @Override
    public String toString() {
        return Integer.toString(value);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Const other = (Const) obj;
        return this.value == other.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(value);
    }
}

/**
 * Класс для представления переменной в выражении.
 * При вычислении возвращает значение, переданное в метод evaluate.
 */
class Variable extends AbstractExpression {
    private final String name;

    /**
     * Создает переменную с заданным именем.
     * @param name имя переменной (например, "x")
     */
    public Variable(String name) {
        this.name = name;
    }

    /**
     * Вычисляет значение переменной.
     * @param x значение переменной
     * @return значение x
     */
    @Override
    public int evaluate(int x) {
        return x;
    }

    @Override
    public String toString() {
        return name;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Variable other = (Variable) obj;
        return this.name.equals(other.name);
    }

    @Override
    public int hashCode() {
        return name.hashCode();
    }
}

/**
 * Абстрактный базовый класс для всех бинарных операций (сложение, вычитание, умножение, деление).
 * Определяет общую структуру бинарных операций и логику расстановки скобок.
 * 
 * Каждая конкретная операция должна определить:
 * - apply(a, b) - способ применения операции
 * - getOperator() - строковое представление оператора
 * - getPriority() - приоритет операции для правильной расстановки скобок
 * - isLeftAssociative() - ассоциативность операции
 */
abstract class BinaryOperation extends AbstractExpression {
    protected final Expression left;
    protected final Expression right;
    
        /**
     * Создает бинарную операцию с левым и правым операндами.
     * @param left левый операнд
     * @param right правый операнд
     */
    public BinaryOperation(Expression left, Expression right) {
        this.left = left;
        this.right = right;
    }

    protected abstract int apply(int a, int b);
    protected abstract String getOperator();
    protected abstract int getPriority();
    protected abstract boolean isLeftAssociative();

    @Override
    public int evaluate(int x) {
        return apply(left.evaluate(x), right.evaluate(x));
    }

    @Override
    public String toString() {
        return "(" + left.toString() + " " + getOperator() + " " + right.toString() + ")";
    }

    @Override
    public String toMiniString() {
        StringBuilder sb = new StringBuilder();

        // Левый операнд
        if (needLeftParentheses()) {
            sb.append("(").append(left.toMiniString()).append(")");
        } else {
            sb.append(left.toMiniString());
        }

        sb.append(" ").append(getOperator()).append(" ");

        // Правый операнд
        if (needRightParentheses()) {
            sb.append("(").append(right.toMiniString()).append(")");
        } else {
            sb.append(right.toMiniString());
        }

        return sb.toString();
    }

    private boolean needLeftParentheses() {
        if (!(left instanceof BinaryOperation)) return false;
        BinaryOperation leftOp = (BinaryOperation) left;
        return leftOp.getPriority() < this.getPriority();
    }

    private boolean needRightParentheses() {
        if (!(right instanceof BinaryOperation)) return false;
        BinaryOperation rightOp = (BinaryOperation) right;

        // Правый операнд требует скобок, если:
        // 1. Его приоритет ниже текущего
        // 2. Его приоритет равен текущему, но операция левоассоциативна (для - и /)
        if (rightOp.getPriority() < getPriority()) {
            return true;
        }
        if (rightOp.getPriority() == getPriority() && isLeftAssociative()) {
            return true;
        }

        return false;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        BinaryOperation other = (BinaryOperation) obj;
        return this.left.equals(other.left) && this.right.equals(other.right);
    }

    @Override
    public int hashCode() {
        return 31 * left.hashCode() + right.hashCode();
    }
}

/**
 * Класс для операции сложения.
 * Вычисляет сумму двух выражений: a + b
 */
class Add extends BinaryOperation {
    public Add(Expression left, Expression right) {
        super(left, right);
    }
    
    @Override
    protected int apply(int a, int b) {
        return a + b;
    }
    
    @Override
    protected String getOperator() {
        return "+";
    }
    
    @Override
    protected int getPriority() {
        return 1; // Низкий приоритет
    }
    
    @Override
    protected boolean isLeftAssociative() {
        return true;
    }
}

/**
 * Класс для операции вычитания.
 * Вычисляет разность двух выражений: a - b
 */
class Subtract extends BinaryOperation {
    public Subtract(Expression left, Expression right) {
        super(left, right);
    }
    
    @Override
    protected int apply(int a, int b) {
        return a - b;
    }
    
    @Override
    protected String getOperator() {
        return "-";
    }
    
    @Override
    protected int getPriority() {
        return 1; // Низкий приоритет
    }
    
    @Override
    protected boolean isLeftAssociative() {
        return true;
    }
}

// Класс для умножения
class Multiply extends BinaryOperation {
    public Multiply(Expression left, Expression right) {
        super(left, right);
    }
    
    @Override
    protected int apply(int a, int b) {
        return a * b;
    }
    
    @Override
    protected String getOperator() {
        return "*";
    }
    
    @Override
    protected int getPriority() {
        return 2; // Высокий приоритет
    }
    
    @Override
    protected boolean isLeftAssociative() {
        return true;
    }
}

// Класс для деления
class Divide extends BinaryOperation {
    public Divide(Expression left, Expression right) {
        super(left, right);
    }
    
    @Override
    protected int apply(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("Division by zero");
        }
        return a / b;
    }
    
    @Override
    protected String getOperator() {
        return "/";
    }
    
    @Override
    protected int getPriority() {
        return 2; // Высокий приоритет
    }
    
    @Override
    protected boolean isLeftAssociative() {
        return true;
    }
}

// Главный класс для тестирования
public class Main {
    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("Запустите программу с аргументами для тестирования.\nЗапуск: java Main <значение_x>");
            return;
        }

        int x = Integer.parseInt(args[0]);

        // Создание выражения x^2 - 2*x + 1
        Expression expr = new Add(
            new Subtract(
                new Multiply(
                    new Variable("x"),
                    new Variable("x")
                ),
                new Multiply(
                    new Const(2),
                    new Variable("x")
                )
            ),
            new Const(1)
        );
    
        System.out.println("Выражение (полная форма): " + expr.toString());
        System.out.println("Выражение (минимальная форма): " + expr.toMiniString());
        System.out.println("Значение при x = " + x + ": " + expr.evaluate(x));
    
        // Демонстрация других примеров
        System.out.println("\n--- Дополнительные примеры ---");
        
        Expression example1 = new Subtract(
            new Multiply(
                new Const(2),
                new Variable("x")
            ),
            new Const(3)
        );
        System.out.println("Пример 1 (toString): " + example1.toString());
        System.out.println("Пример 1 (toMiniString): " + example1.toMiniString());
        System.out.println("Пример 1 (evaluate(5)): " + example1.evaluate(5));
        
        // Проверка equals
        Expression e1 = new Multiply(new Const(2), new Variable("x"));
        Expression e2 = new Multiply(new Const(2), new Variable("x"));
        Expression e3 = new Multiply(new Variable("x"), new Const(2));
        
        System.out.println("\n--- Проверка equals ---");
        System.out.println("e1.equals(e2): " + e1.equals(e2)); // true
        System.out.println("e1.equals(e3): " + e1.equals(e3)); // false
    }
}