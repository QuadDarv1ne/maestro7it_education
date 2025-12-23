import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;

/**
 * Класс для демонстрации работы с массивами и коллекциями в Java.
 * 
 * <p>Класс демонстрирует различные способы создания и использования:
 * <ul>
 *   <li>Одномерных массивов (литералы и конструктор new)</li>
 *   <li>Многомерных массивов</li>
 *   <li>Коллекций (ArrayList) как динамических массивов</li>
 * </ul>
 */
public class ArrayDemo {
    
    /**
     * Главный метод программы, демонстрирующий различные операции с массивами.
     * 
     * <p>Метод последовательно выполняет:
     * <ol>
     *   <li>Создание массива строк через литерал</li>
     *   <li>Создание массива чисел через конструктор new</li>
     *   <li>Создание и заполнение пустого массива</li>
     *   <li>Работу с двумерным массивом (матрицей)</li>
     *   <li>Использование ArrayList для динамического хранения данных</li>
     * </ol>
     * 
     * @param args аргументы командной строки. В данной демонстрации не используются.
     * 
     * @throws ArithmeticException если возникает ошибка при математических операциях
     *         (в текущем коде исключение не генерируется)
     * 
     * @see #printArrayInfo(int[])
     * @see #printMatrix(int[][])
     * 
     * @example
     * <pre>{@code
     * // Запуск программы:
     * java ArrayDemo
     * 
     * // Пример вывода:
     * // Фрукты: [apple, banana, cherry]
     * // Числа: [1, 2, 3, 4]
     * // ...
     * }</pre>
     */
    public static void main(String[] args) {
        // 1. Литерал массива
        String[] fruits = {"apple", "banana", "cherry"};
        System.out.println("Фрукты: " + Arrays.toString(fruits));
        
        // 2. Через new с инициализацией
        int[] numbers = new int[]{1, 2, 3, 4};
        System.out.println("Числа: " + Arrays.toString(numbers));
        printArrayInfo(numbers); // Пример вызова вспомогательного метода
        
        // 3. Создание пустого массива
        double[] prices = new double[3];
        prices[0] = 12.5;
        prices[1] = 7.99;
        prices[2] = 3.49;
        System.out.println("Цены: " + Arrays.toString(prices));
        
        // 4. Многомерный массив
        int[][] matrix = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        System.out.println("\nМатрица 3x3:");
        printMatrix(matrix);
        
        // 5. ArrayList (динамический массив)
        demonstrateArrayList();
    }
    
    /**
     * Вспомогательный метод для вывода информации об одномерном массиве целых чисел.
     * 
     * <p>Метод выводит:
     * <ul>
     *   <li>Длину массива</li>
     *   <li>Все элементы массива</li>
     *   <li>Сумму элементов</li>
     * </ul>
     * 
     * @param array массив целых чисел для анализа
     * 
     * @throws NullPointerException если переданный массив равен null
     * 
     * @see Arrays#toString(int[])
     */
    private static void printArrayInfo(int[] array) {
        if (array == null) {
            throw new NullPointerException("Массив не может быть null");
        }
        
        System.out.println("\n=== Информация о массиве ===");
        System.out.println("Длина массива: " + array.length);
        System.out.println("Элементы: " + Arrays.toString(array));
        
        int sum = 0;
        for (int num : array) {
            sum += num;
        }
        System.out.println("Сумма элементов: " + sum);
    }
    
    /**
     * Метод для вывода матрицы (двумерного массива) на консоль.
     * 
     * <p>Каждая строка матрицы выводится в отдельной строке консоли
     * в формате: [элемент1, элемент2, ...]
     * 
     * @param matrix двумерный массив (матрица) для вывода
     * 
     * @throws IllegalArgumentException если матрица равна null
     * 
     * @see Arrays#toString(int[])
     */
    private static void printMatrix(int[][] matrix) {
        if (matrix == null) {
            throw new IllegalArgumentException("Матрица не может быть null");
        }
        
        for (int[] row : matrix) {
            System.out.println(Arrays.toString(row));
        }
    }
    
    /**
     * Демонстрирует основные операции с ArrayList.
     * 
     * <p>Показывает:
     * <ul>
     *   <li>Создание ArrayList</li>
     *   <li>Добавление элементов (add)</li>
     *   <li>Удаление элементов по значению и индексу (remove)</li>
     *   <li>Получение элементов (get)</li>
     *   <li>Получение размера коллекции (size)</li>
     *   <li>Проверку на наличие элемента (contains)</li>
     * </ul>
     * 
     * @see ArrayList
     * @see List
     */
    private static void demonstrateArrayList() {
        System.out.println("\n=== Демонстрация ArrayList ===");
        
        // Создание ArrayList
        List<String> fruitList = new ArrayList<>();
        
        // Добавление элементов
        System.out.println("Добавляем элементы...");
        fruitList.add("apple");
        fruitList.add("banana");
        fruitList.add("cherry");
        fruitList.add("orange");
        System.out.println("Исходный список: " + fruitList);
        
        // Получение элемента по индексу
        System.out.println("Элемент с индексом 1: " + fruitList.get(1));
        
        // Удаление элемента по значению
        System.out.println("\nУдаляем 'cherry' по значению...");
        fruitList.remove("cherry");
        System.out.println("После удаления: " + fruitList);
        
        // Удаление элемента по индексу
        System.out.println("\nУдаляем элемент с индексом 0...");
        fruitList.remove(0);
        System.out.println("После удаления: " + fruitList);
        
        // Проверка наличия элемента
        System.out.println("\nСодержит ли список 'banana'? " + fruitList.contains("banana"));
        System.out.println("Содержит ли список 'apple'? " + fruitList.contains("apple"));
        
        // Размер коллекции
        System.out.println("Текущий размер списка: " + fruitList.size());
        
        // Очистка коллекции
        System.out.println("\nОчищаем список...");
        fruitList.clear();
        System.out.println("Список после очистки: " + fruitList);
        System.out.println("Размер после очистки: " + fruitList.size());
    }
}