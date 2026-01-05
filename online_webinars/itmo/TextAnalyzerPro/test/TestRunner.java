import tasks.ReverseTask;
import tasks.WordStatTask;
import tasks.WordStatPlusTask;
import tasks.TextStatTask;
import tasks.TopWordsTask;
import analyzer.statistics.TextStatistics;
import java.io.*;
import java.nio.file.*;

/**
 * Комплексный тестовый запускатор для всех задач
 */
public class TestRunner {
    
    public static void main(String[] args) {
        System.out.println("=== ЗАПУСК ТЕСТОВ TextAnalyzerPro ===\n");
        
        // Создаем директорию для фактических результатов
        createDirectory("test/actual");
        
        int passed = 0;
        int total = 0;
        
        try {
            // Тест 1: ReverseTask
            total++;
            if (testReverseTask()) {
                passed++;
                System.out.println("✓ Тест ReverseTask пройден");
            } else {
                System.out.println("✗ Тест ReverseTask не пройден");
            }
            
            // Тест 2: WordStatTask
            total++;
            if (testWordStatTask()) {
                passed++;
                System.out.println("✓ Тест WordStatTask пройден");
            } else {
                System.out.println("✗ Тест WordStatTask не пройден");
            }
            
            // Тест 3: WordStatPlusTask
            total++;
            if (testWordStatPlusTask()) {
                passed++;
                System.out.println("✓ Тест WordStatPlusTask пройден");
            } else {
                System.out.println("✗ Тест WordStatPlusTask не пройден");
            }
            
            // Тест 4: TextStatistics
            total++;
            if (testTextStatistics()) {
                passed++;
                System.out.println("✓ Тест TextStatistics пройден");
            } else {
                System.out.println("✗ Тест TextStatistics не пройден");
            }
            
            // Тест 5: TextStatTask
            total++;
            if (testTextStatTask()) {
                passed++;
                System.out.println("✓ Тест TextStatTask пройден");
            } else {                System.out.println("✗ Тест TextStatTask не пройден");
            }
            
            // Тест 6: TopWordsTask
            total++;
            if (testTopWordsTask()) {
                passed++;
                System.out.println("✓ Тест TopWordsTask пройден");
            } else {                System.out.println("✗ Тест TextStatTask не пройден");
            }
            
        } catch (Exception e) {
            System.err.println("Ошибка при выполнении тестов: " + e.getMessage());
            e.printStackTrace();
        }
        
        System.out.println("\n=== РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ ===");
        System.out.printf("Пройдено тестов: %d/%d\n", passed, total);
        
        if (passed == total) {
            System.out.println("✅ Все тесты пройдены успешно!");
        } else {
            System.out.println("❌ Некоторые тесты не пройдены");
            System.exit(1);
        }
    }
    
    private static boolean testReverseTask() throws IOException {
        String inputFile = "test/input/reverse.txt";
        String outputFile = "test/actual/reverse_output.txt";
        String expectedFile = "test/expected/reverse_output.txt";
        
        // Создаем тестовый файл, если его нет
        if (!Files.exists(Paths.get(inputFile))) {
            createTestReverseFile(inputFile);
        }
        
        // Запускаем задачу
        ReverseTask.processFile(inputFile, outputFile);
        
        // Сравниваем с ожидаемым результатом
        return compareFiles(outputFile, expectedFile);
    }
    
    private static boolean testWordStatTask() throws IOException {
        String inputFile = "test/input/wordstat.txt";
        String outputFile = "test/actual/wordstat_output.txt";
        String expectedFile = "test/expected/wordstat_output.txt";
        
        // Создаем тестовый файл, если его нет
        if (!Files.exists(Paths.get(inputFile))) {
            createTestWordStatFile(inputFile);
        }
        
        // Запускаем задачу
        WordStatTask.processFile(inputFile, outputFile);
        
        // Сравниваем с ожидаемым результатом
        return compareFiles(outputFile, expectedFile);
    }
    
    private static boolean testWordStatPlusTask() throws IOException {
        String inputFile = "test/input/wordstat_plus.txt";
        String outputFile = "test/actual/wordstat_plus_output.txt";
        String expectedFile = "test/expected/wordstat_plus_output.txt";
        
        // Создаем тестовый файл, если его нет
        if (!Files.exists(Paths.get(inputFile))) {
            createTestWordStatPlusFile(inputFile);
        }
        
        // Запускаем задачу
        WordStatPlusTask.processFile(inputFile, outputFile);
        
        // Сравниваем с ожидаемым результатом
        return compareFiles(outputFile, expectedFile);
    }
    
    private static boolean testTextStatistics() throws IOException {
        String inputFile = "test/input/text_stats.txt";
        String outputFile = "test/actual/text_stats_output.txt";
        
        // Создаем тестовый файл, если его нет
        if (!Files.exists(Paths.get(inputFile))) {
            createTestTextStatsFile(inputFile);
        }
        
        // Запускаем анализ
        TextStatistics stats = new TextStatistics();
        stats.analyzeFile(inputFile);
        stats.exportToFile(outputFile);
        
        // Проверяем, что файл создан и не пустой
        File file = new File(outputFile);
        return file.exists() && file.length() > 0;
    }
    
    private static boolean testTextStatTask() throws IOException {
        String inputFile = "test/input/text_stats.txt";
        String outputFile = "test/actual/text_stat_task_output.txt";
        
        // Создаем тестовый файл, если его нет
        if (!Files.exists(Paths.get(inputFile))) {
            createTestTextStatsFile(inputFile);
        }
        
        // Запускаем задачу
        TextStatTask.processFile(inputFile, outputFile);
        
        // Проверяем, что файл создан и не пустой
        File file = new File(outputFile);
        return file.exists() && file.length() > 0;
    }
    
    private static boolean testTopWordsTask() throws IOException {
        String inputFile = "test/input/words.txt";
        String outputFile = "test/actual/top_words_output.txt";
        String expectedFile = "test/expected/top_words_output.txt";
        
        // Создаем тестовый файл, если его нет
        if (!Files.exists(Paths.get(inputFile))) {
            createTestWordStatFile(inputFile);
        }
        
        // Запускаем задачу (топ 5 слов)
        TopWordsTask.processFile(inputFile, outputFile, 5);
        
        // Сравниваем с ожидаемым результатом
        return compareFiles(outputFile, expectedFile);
    }
    
    private static void createTestReverseFile(String filePath) throws IOException {
        String content = "1 2 3\n4 5 6\n7 8 9\n";
        Files.write(Paths.get(filePath), content.getBytes());
        
        // Создаем ожидаемый результат
        String expectedContent = "9 8 7\n6 5 4\n3 2 1";
        Path expectedDir = Paths.get("test/expected");
        if (!Files.exists(expectedDir)) {
            Files.createDirectories(expectedDir);
        }
        Files.write(expectedDir.resolve("reverse_output.txt"), expectedContent.getBytes());
    }
    
    private static void createTestWordStatFile(String filePath) throws IOException {
        String content = "To be or not to be, that is the question!\n" +
                        "Hello world, hello Java!";
        Files.write(Paths.get(filePath), content.getBytes());
        
        // Создаем ожидаемый результат для wordstat
        String expectedContent = "to 2\nbe 2\nor 1\nnot 1\nthat 1\nis 1\nthe 1\n" +
                                "question 1\nhello 2\nworld 1\njava 1";
        Path expectedDir = Paths.get("test/expected");
        if (!Files.exists(expectedDir)) {
            Files.createDirectories(expectedDir);
        }
        Files.write(expectedDir.resolve("wordstat_output.txt"), expectedContent.getBytes());
        
        // Создаем ожидаемый результат для topwords (топ 5)
        String topWordsExpected = "be 2\nhello 2\nto 2\nnot 1\nor 1";
        Files.write(expectedDir.resolve("top_words_output.txt"), topWordsExpected.getBytes());
    }
    
    private static void createTestWordStatPlusFile(String filePath) throws IOException {
        String content = "To be or not to be\n" +
                        "That is the question!";
        Files.write(Paths.get(filePath), content.getBytes());
        
        // Создаем ожидаемый результат
        String expectedContent = "to 2 1 5\nbe 2 2 6\nor 1 3\nnot 1 4\n" +
                                "that 1 7\nis 1 8\nthe 1 9\nquestion 1 10";
        Path expectedDir = Paths.get("test/expected");
        if (!Files.exists(expectedDir)) {
            Files.createDirectories(expectedDir);
        }
        Files.write(expectedDir.resolve("wordstat_plus_output.txt"), expectedContent.getBytes());
    }
    
    private static void createTestTextStatsFile(String filePath) throws IOException {
        String content = "Это тестовый текст.\n" +
                        "Он содержит несколько предложений.\n" +
                        "И несколько слов для анализа статистики.\n" +
                        "Hello World! Привет мир!";
        Files.write(Paths.get(filePath), content.getBytes("UTF-8"));
    }
    
    private static boolean compareFiles(String actualFile, String expectedFile) throws IOException {
        if (!Files.exists(Paths.get(expectedFile))) {
            System.out.println("  Предупреждение: файл с ожидаемым результатом не найден: " + expectedFile);
            return false;
        }
        
        String actual = new String(Files.readAllBytes(Paths.get(actualFile)), "UTF-8").trim().replace("\r\n", "\n").replace("\r", "\n");
        String expected = new String(Files.readAllBytes(Paths.get(expectedFile)), "UTF-8").trim().replace("\r\n", "\n").replace("\r", "\n");
        
        return actual.equals(expected);
    }
    
    private static void createDirectory(String path) {
        try {
            Files.createDirectories(Paths.get(path));
        } catch (IOException e) {
            System.err.println("Не удалось создать директорию: " + path);
        }
    }
}