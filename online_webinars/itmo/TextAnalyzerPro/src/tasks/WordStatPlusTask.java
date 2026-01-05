package tasks;

import analyzer.scanner.TextScanner;
import analyzer.statistics.WordStatistics;
import java.io.*;
import java.nio.charset.StandardCharsets;

/**
 * Решение задачи "Статистика слов++"
 * Выводит слова в порядке их появления с количеством и позициями
 */
public class WordStatPlusTask {
    
    /**
     * Обрабатывает входной файл и записывает статистику в выходной
     */
    public static void processFile(String inputFile, String outputFile) throws IOException {
        WordStatistics statistics = new WordStatistics();
        
        try (TextScanner scanner = new TextScanner(new InputStreamReader(new FileInputStream(inputFile), StandardCharsets.UTF_8))) {
            String word;
            while ((word = scanner.nextWord()) != null) {
                statistics.addWord(word);
            }
        }
        
        writeStatistics(outputFile, statistics);
    }
    
    /**
     * Записывает статистику в файл
     */
    private static void writeStatistics(String outputFile, WordStatistics statistics) 
            throws IOException {
        
        try (BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(outputFile), StandardCharsets.UTF_8))) {
            
            writer.write(statistics.exportStatistics());
        }
    }
    
    /**
     * Основной метод для запуска из командной строки
     */
    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Использование: java WordStatPlusTask <входной-файл> <выходной-файл>");
            System.err.println("Пример: java WordStatPlusTask input.txt output.txt");
            return;
        }
        
        try {
            long startTime = System.currentTimeMillis();
            
            processFile(args[0], args[1]);
            
            long endTime = System.currentTimeMillis();
            System.out.printf("Статистика записана в файл: %s%n", args[1]);
            System.out.printf("Время выполнения: %d мс%n", endTime - startTime);
            
        } catch (FileNotFoundException e) {
            System.err.println("Ошибка: Файл не найден - " + e.getMessage());
        } catch (IOException e) {
            System.err.println("Ошибка ввода-вывода: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("Неожиданная ошибка: " + e.getMessage());
            e.printStackTrace();
        }
    }
}