package tasks;

import analyzer.scanner.TextScanner;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import analyzer.utils.Logger;

/**
 * Решение задачи "Анализ длины слов"
 * Выводит статистику по длинам слов в тексте
 */
public class WordLengthTask {

    /**
     * Обрабатывает входной файл и записывает статистику длин слов в выходной
     */
    public static void processFile(String inputFile, String outputFile) throws IOException {
        Logger.logTaskStart("Анализ длины слов", inputFile);
        long startTime = System.currentTimeMillis();

        Map<Integer, Integer> lengthStats = new TreeMap<>();

        try (TextScanner scanner = new TextScanner(new InputStreamReader(new FileInputStream(inputFile), StandardCharsets.UTF_8))) {
            String word;
            while ((word = scanner.nextWord()) != null) {
                int length = word.length();
                lengthStats.put(length, lengthStats.getOrDefault(length, 0) + 1);
            }
        }

        writeLengthStatistics(outputFile, lengthStats);

        long endTime = System.currentTimeMillis();
        Logger.logTaskEnd("Анализ длины слов", outputFile, endTime - startTime);
    }

    /**
     * Записывает статистику длин слов в файл
     */
    private static void writeLengthStatistics(String outputFile, Map<Integer, Integer> lengthStats)
            throws IOException {

        try (BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(outputFile), StandardCharsets.UTF_8))) {

            writer.write("Длина слова\tКоличество слов\n");
            writer.write("------------\t--------------\n");

            int totalWords = 0;
            int totalLength = 0;

            for (Map.Entry<Integer, Integer> entry : lengthStats.entrySet()) {
                writer.write(String.format("%d\t\t%d\n", entry.getKey(), entry.getValue()));
                totalWords += entry.getValue();
                totalLength += entry.getKey() * entry.getValue();
            }

            writer.write("\n");
            writer.write(String.format("Всего слов: %d\n", totalWords));
            writer.write(String.format("Средняя длина слова: %.2f\n", totalWords > 0 ? (double) totalLength / totalWords : 0));
            writer.write(String.format("Минимальная длина: %d\n", lengthStats.isEmpty() ? 0 : lengthStats.keySet().iterator().next()));
            writer.write(String.format("Максимальная длина: %d\n", lengthStats.isEmpty() ? 0 : ((TreeMap<Integer, Integer>) lengthStats).lastKey()));
        }
    }

    /**
     * Основной метод для запуска из командной строки
     */
    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Использование: java WordLengthTask <входной-файл> <выходной-файл>");
            System.err.println("Пример: java WordLengthTask input.txt output.txt");
            return;
        }

        try {
            processFile(args[0], args[1]);
            System.out.println("Анализ длин слов завершён. Результат сохранён в: " + args[1]);
        } catch (IOException e) {
            Logger.logTaskError("Анализ длины слов", e.getMessage());
            System.err.println("Ошибка: " + e.getMessage());
        }
    }
}