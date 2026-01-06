import tasks.ReverseTask;
import tasks.WordStatPlusTask;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;

/**
 * Тестовый запускатор для проверки корректности реализации
 */
public class TestRunner {
    
    public static void main(String[] args) {
        System.out.println("=== Тестирование TextAnalyzerPro ===\n");
        
        // Создаем директорию для фактических результатов
        new File("test/actual").mkdirs();
        
        boolean allTestsPassed = true;
        
        // Тест 1: Задача "Реверс"
        System.out.println("Тест 1: Задача 'Реверс'");
        try {
            ReverseTask.processFile("test/input/reverse.txt", "test/actual/reverse_output.txt");
            
            String expected = readFile("test/expected/reverse_output.txt");
            String actual = readFile("test/actual/reverse_output.txt");
            
            if (expected.equals(actual)) {
                System.out.println("✓ Тест пройден");
            } else {
                System.out.println("✗ Тест не пройден");
                System.out.println("Ожидалось:\n" + expected);
                System.out.println("Получено:\n" + actual);
                allTestsPassed = false;
            }
        } catch (Exception e) {
            System.out.println("✗ Ошибка при выполнении теста: " + e.getMessage());
            allTestsPassed = false;
        }
        
        System.out.println();
        
        // Тест 2: Задача "Статистика слов++"
        System.out.println("Тест 2: Задача 'Статистика слов++'");
        try {
            WordStatPlusTask.processFile("test/input/wordstat_plus.txt", "test/actual/wordstat_plus_output.txt");
            
            String expected = readFile("test/expected/wordstat_plus_output.txt");
            String actual = readFile("test/actual/wordstat_plus_output.txt");
            
            if (expected.equals(actual)) {
                System.out.println("✓ Тест пройден");
            } else {
                System.out.println("✗ Тест не пройден");
                System.out.println("Ожидалось:\n" + expected);
                System.out.println("Получено:\n" + actual);
                allTestsPassed = false;
            }
        } catch (Exception e) {
            System.out.println("✗ Ошибка при выполнении теста: " + e.getMessage());
            allTestsPassed = false;
        }
        
        System.out.println();
        
        // Итог
        if (allTestsPassed) {
            System.out.println("=== Все тесты успешно пройдены! ===");
        } else {
            System.out.println("=== Некоторые тесты не пройдены ===");
            System.exit(1);
        }
    }
    
    private static String readFile(String filePath) throws IOException {
        byte[] bytes = Files.readAllBytes(Paths.get(filePath));
        return new String(bytes, "UTF-8");
    }
}