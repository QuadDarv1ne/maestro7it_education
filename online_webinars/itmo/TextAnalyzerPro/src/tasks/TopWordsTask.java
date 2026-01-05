package tasks;

import analyzer.scanner.TextScanner;
import analyzer.statistics.WordStatistics;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

/**
 * Решение задачи "Топ слов"
 * Выводит топ N наиболее частых слов с их частотами
 */
public class TopWordsTask {

    /**
     * Обрабатывает входной файл и записывает топ слов в выходной
     */
    public static void processFile(String inputFile, String outputFile, int topN) throws IOException {
        WordStatistics statistics = new WordStatistics();

        try (TextScanner scanner = new TextScanner(new InputStreamReader(new FileInputStream(inputFile), StandardCharsets.UTF_8))) {
            String word;
            while ((word = scanner.nextWord()) != null) {
                statistics.addWord(word);
            }
        }

        writeTopWords(outputFile, statistics, topN);
    }

    /**
     * Записывает топ слов в файл
     */
    private static void writeTopWords(String outputFile, WordStatistics statistics, int topN)
            throws IOException {

        try (BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(outputFile), StandardCharsets.UTF_8))) {

            // Получаем все слова с их частотами
            List<Map.Entry<String, Integer>> wordFreqList = new ArrayList<>();
            for (String word : statistics.getUniqueWords()) {
                wordFreqList.add(new AbstractMap.SimpleEntry<>(word, statistics.getFrequency(word)));
            }

            // Сортируем по частоте убыванию, затем по алфавиту
            wordFreqList.sort((a, b) -> {
                int freqCompare = Integer.compare(b.getValue(), a.getValue());
                if (freqCompare != 0) return freqCompare;
                return a.getKey().compareTo(b.getKey());
            });

            // Выводим топ N
            int count = 0;
            for (Map.Entry<String, Integer> entry : wordFreqList) {
                if (count >= topN) break;
                writer.write(entry.getKey() + " " + entry.getValue() + "\n");
                count++;
            }
        }
    }

    /**
     * Основной метод для запуска из командной строки
     */
    public static void main(String[] args) {
        if (args.length != 3) {
            System.err.println("Использование: java TopWordsTask <входной-файл> <выходной-файл> <топ-N>");
            System.err.println("Пример: java TopWordsTask input.txt output.txt 10");
            return;
        }

        String inputFile = args[0];
        String outputFile = args[1];
        int topN;

        try {
            topN = Integer.parseInt(args[2]);
            if (topN <= 0) {
                System.err.println("Ошибка: Топ N должно быть положительным числом");
                return;
            }
        } catch (NumberFormatException e) {
            System.err.println("Ошибка: Неверный формат числа для топ N: " + args[2]);
            return;
        }

        try {
            processFile(inputFile, outputFile, topN);
            System.out.println("Топ " + topN + " слов успешно записан в " + outputFile);
        } catch (IOException e) {
            System.err.println("Ошибка при обработке файлов: " + e.getMessage());
        }
    }
}