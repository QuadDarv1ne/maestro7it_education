package analyzer;

import analyzer.scanner.TextScanner;
import analyzer.statistics.WordStatistics;
import java.io.IOException;
import java.io.StringReader;
import java.util.List;

/**
 * Класс для benchmarking производительности сканера и статистики
 */
public class Benchmark {

    public static void main(String[] args) throws IOException {
        String testText = generateTestText(100000); // 100k слов

        long startTime = System.nanoTime();
        try (TextScanner scanner = new TextScanner(new StringReader(testText))) {
            WordStatistics stats = new WordStatistics();
            String word;
            while ((word = scanner.nextWord()) != null) {
                stats.addWord(word);
            }
            List<String> words = stats.getWordsInOrder();
            System.out.println("Обработано слов: " + stats.getTotalWords());
            System.out.println("Уникальных слов: " + stats.getUniqueWordsCount());
        }
        long endTime = System.nanoTime();
        System.out.println("Время выполнения: " + (endTime - startTime) / 1_000_000 + " ms");
    }

    private static String generateTestText(int wordCount) {
        StringBuilder sb = new StringBuilder();
        String[] words = {"hello", "world", "java", "text", "analyzer", "performance", "test"};
        for (int i = 0; i < wordCount; i++) {
            sb.append(words[i % words.length]).append(" ");
        }
        return sb.toString();
    }
}