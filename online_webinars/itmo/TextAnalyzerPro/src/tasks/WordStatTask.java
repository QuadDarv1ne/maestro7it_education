package tasks;

import analyzer.scanner.TextScanner;
import analyzer.utils.FileUtils;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

/**
 * Решение задачи "Статистика слов" (базовая версия)
 * Подсчитывает частоту слов без учета позиций
 */
public class WordStatTask {
    
    /**
     * Обрабатывает файл и подсчитывает статистику слов
     */
    public static void processFile(String inputFile, String outputFile) throws IOException {
        Map<String, Integer> wordFrequency = new LinkedHashMap<>();
        
        try (TextScanner scanner = new TextScanner(new InputStreamReader(new FileInputStream(inputFile), StandardCharsets.UTF_8))) {
            String word;
            while ((word = scanner.nextWord()) != null) {
                word = normalizeWord(word);
                wordFrequency.put(word, wordFrequency.getOrDefault(word, 0) + 1);
            }
        }
        
        writeStatistics(outputFile, wordFrequency);
    }
    
    /**
     * Нормализует слово (приводит к нижнему регистру)
     */
    private static String normalizeWord(String word) {
        return word.toLowerCase();
    }
    
    /**
     * Записывает статистику в файл
     */
    private static void writeStatistics(String outputFile, Map<String, Integer> wordFrequency) 
            throws IOException {
        
        try (BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(outputFile), StandardCharsets.UTF_8))) {
            
            for (Map.Entry<String, Integer> entry : wordFrequency.entrySet()) {
                writer.write(entry.getKey() + " " + entry.getValue());
                writer.newLine();
            }
        }
    }
    
    /**
     * Вспомогательный метод для обработки текста из строки
     */
    public static Map<String, Integer> processText(String text) throws IOException {
        Map<String, Integer> wordFrequency = new LinkedHashMap<>();
        
        try (Scanner scanner = new Scanner(new StringReader(text))) {
            String word;
            while ((word = scanner.nextWord()) != null) {
                word = normalizeWord(word);
                wordFrequency.put(word, wordFrequency.getOrDefault(word, 0) + 1);
            }
        }
        
        return wordFrequency;
    }
    
    /**
     * Возвращает топ N самых частых слов
     */
    public static List<Map.Entry<String, Integer>> getTopWords(
            Map<String, Integer> wordFrequency, int n) {
        
        List<Map.Entry<String, Integer>> entries = new ArrayList<>(wordFrequency.entrySet());
        
        // Сортируем по убыванию частоты, затем по алфавиту
        entries.sort((a, b) -> {
            int freqCompare = b.getValue().compareTo(a.getValue());
            if (freqCompare != 0) {
                return freqCompare;
            }
            return a.getKey().compareTo(b.getKey());
        });
        
        return entries.subList(0, Math.min(n, entries.size()));
    }
    
    /**
     * Форматирует статистику для отображения
     */
    public static String formatStatistics(Map<String, Integer> wordFrequency) {
        StringBuilder result = new StringBuilder();
        
        for (Map.Entry<String, Integer> entry : wordFrequency.entrySet()) {
            result.append(String.format("%-20s: %d\n", entry.getKey(), entry.getValue()));
        }
        
        return result.toString();
    }
    
    /**
     * Основной метод для командной строки
     */
    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Использование: java WordStatTask <входной-файл> <выходной-файл>");
            System.err.println("Пример: java WordStatTask input.txt output.txt");
            return;
        }
        
        try {
            processFile(args[0], args[1]);
            System.out.println("Статистика успешно записана в: " + args[1]);
        } catch (IOException e) {
            System.err.println("Ошибка: " + e.getMessage());
        }
    }
    
    /**
     * Метод для тестирования
     */
    public static void test() {
        String testText = "To be, or not to be, that is the question!";
        
        try {
            Map<String, Integer> stats = processText(testText);
            System.out.println("Тестовая статистика:");
            System.out.println(formatStatistics(stats));
            
            List<Map.Entry<String, Integer>> topWords = getTopWords(stats, 3);
            System.out.println("Топ 3 слова:");
            for (Map.Entry<String, Integer> entry : topWords) {
                System.out.println(entry.getKey() + ": " + entry.getValue());
            }
        } catch (IOException e) {
            System.err.println("Ошибка при тестировании: " + e.getMessage());
        }
    }
}