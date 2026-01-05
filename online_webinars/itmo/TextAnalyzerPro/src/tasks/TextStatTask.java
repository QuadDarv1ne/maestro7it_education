package tasks;

import analyzer.statistics.TextStatistics;
import java.io.*;
import java.nio.charset.StandardCharsets;

/**
 * Решение задачи "Статистика текста"
 * Выводит комплексную статистику текста
 */
public class TextStatTask {

    /**
     * Обрабатывает входной файл и записывает статистику в выходной
     */
    public static void processFile(String inputFile, String outputFile) throws IOException {
        TextStatistics statistics = new TextStatistics();

        statistics.analyzeFile(inputFile);

        writeStatistics(outputFile, statistics);
    }

    /**
     * Записывает статистику в файл
     */
    private static void writeStatistics(String outputFile, TextStatistics statistics)
            throws IOException {

        try (BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(outputFile), StandardCharsets.UTF_8))) {

            writer.write(statistics.generateReport());
        }
    }

    /**
     * Основной метод для запуска из командной строки
     */
    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Использование: java TextStatTask <входной-файл> <выходной-файл>");
            System.err.println("Пример: java TextStatTask input.txt output.txt");
            return;
        }

        String inputFile = args[0];
        String outputFile = args[1];

        try {
            processFile(inputFile, outputFile);
            System.out.println("Статистика текста записана в " + outputFile);
        } catch (IOException e) {
            System.err.println("Ошибка обработки файла: " + e.getMessage());
        }
    }
}