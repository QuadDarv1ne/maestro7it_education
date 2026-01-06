package analyzer.statistics;

import analyzer.scanner.TextScanner;
import analyzer.utils.IntList;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

/**
 * Комплексная статистика текста: символы, слова, строки, распределение
 */
public class TextStatistics {
    private int charCount;
    private int wordCount;
    private int lineCount;
    private int sentenceCount;
    private int whitespaceCount;
    private int punctuationCount;
    private int digitCount;
    private int letterCount;
    private int uniqueWords;

    private final Map<Character, Integer> charFrequency;
    private final Map<String, Integer> wordFrequency;
    private final Map<Integer, Integer> wordLengthDistribution;
    private final IntList lineLengths;
    private final List<String> longestWords;
    private final List<String> mostFrequentWords;
    private final List<String> shortestWords;

    public TextStatistics() {
        this.charCount = 0;
        this.wordCount = 0;
        this.lineCount = 0;
        this.sentenceCount = 0;
        this.whitespaceCount = 0;
        this.punctuationCount = 0;
        this.digitCount = 0;
        this.letterCount = 0;
        this.uniqueWords = 0;

        this.charFrequency = new HashMap<>();
        this.wordFrequency = new LinkedHashMap<>();
        this.wordLengthDistribution = new HashMap<>();
        this.lineLengths = new IntList();
        this.longestWords = new ArrayList<>();
        this.mostFrequentWords = new ArrayList<>();
        this.shortestWords = new ArrayList<>();
    }

    /**
     * Анализирует текст из файла
     */
    public void analyzeFile(String filePath) throws IOException {
        reset();

        try (TextScanner scanner = new TextScanner(new InputStreamReader(new FileInputStream(filePath), StandardCharsets.UTF_8))) {
            analyzeScanner(scanner);
        }

        calculateDerivedStatistics();
    }

    /**
     * Анализирует текст из строки
     */
    public void analyzeText(String text) throws IOException {
        reset();

        try (TextScanner scanner = new TextScanner(new StringReader(text))) {
            analyzeScanner(scanner);
        }

        calculateDerivedStatistics();
    }

    /**
     * Анализирует текст из TextScanner
     */
    private void analyzeScanner(TextScanner scanner) throws IOException {
        String line;
        StringBuilder currentLine = new StringBuilder();

        while ((line = scanner.nextLine()) != null) {
            lineCount++;
            currentLine.setLength(0);
            currentLine.append(line);

            // Анализ строки
            analyzeLine(line);

            // Сохраняем длину строки (в символах)
            lineLengths.add(line.length());

            // Подсчет предложений (упрощенно)
            if (line.matches(".*[.!?].*")) {
                sentenceCount += countSentencesInLine(line);
            }
        }

        // Если последняя строка не заканчивается точкой, считаем ее предложением
        if (lineCount > 0 && currentLine.length() > 0 &&
                !currentLine.toString().matches(".*[.!?]$")) {
            sentenceCount++;
        }
    }

    /**
     * Анализирует одну строку
     */
    private void analyzeLine(String line) {
        charCount += line.length();

        for (int i = 0; i < line.length(); i++) {
            char ch = line.charAt(i);
            updateCharStatistics(ch);
        }

        // Подсчет слов в строке (упрощенно, для демонстрации)
        String[] words = line.split("[\\p{Punct}\\s]+");
        for (String word : words) {
            if (!word.isEmpty()) {
                analyzeWord(word);
            }
        }
    }

    /**
     * Обновляет статистику по символу
     */
    private void updateCharStatistics(char ch) {
        // Частота символов
        charFrequency.put(ch, charFrequency.getOrDefault(ch, 0) + 1);

        // Классификация символов
        if (Character.isWhitespace(ch)) {
            whitespaceCount++;
        } else if (Character.isLetter(ch)) {
            letterCount++;
        } else if (Character.isDigit(ch)) {
            digitCount++;
        } else if (isPunctuation(ch)) {
            punctuationCount++;
        }
    }

    /**
     * Анализирует слово
     */
    private void analyzeWord(String word) {
        if (word.isEmpty()) {
            return;
        }

        String normalizedWord = word.toLowerCase();

        // Частота слов
        int frequency = wordFrequency.getOrDefault(normalizedWord, 0);
        wordFrequency.put(normalizedWord, frequency + 1);

        wordCount++;

        // Распределение по длине слов
        int length = word.length();
        wordLengthDistribution.put(length,
                wordLengthDistribution.getOrDefault(length, 0) + 1);
    }

    /**
     * Подсчет предложений в строке
     */
    private int countSentencesInLine(String line) {
        int count = 0;
        for (int i = 0; i < line.length(); i++) {
            char ch = line.charAt(i);
            if (ch == '.' || ch == '!' || ch == '?') {
                count++;
            }
        }
        return count;
    }

    /**
     * Проверка, является ли символ знаком препинания
     */
    private boolean isPunctuation(char ch) {
        return ch == '.' || ch == ',' || ch == ';' || ch == ':' ||
                ch == '!' || ch == '?' || ch == '-' || ch == '\'' ||
                ch == '"' || ch == '(' || ch == ')' || ch == '[' ||
                ch == ']' || ch == '{' || ch == '}';
    }

    /**
     * Вычисление производной статистики
     */
    private void calculateDerivedStatistics() {
        uniqueWords = wordFrequency.size();

        // Находим самое длинное слово
        int maxLength = 0;
        for (String word : wordFrequency.keySet()) {
            if (word.length() > maxLength) {
                maxLength = word.length();
                longestWords.clear();
                longestWords.add(word);
            } else if (word.length() == maxLength) {
                longestWords.add(word);
            }
        }

        // Находим самое короткое слово (не менее 1 символа)
        int minLength = Integer.MAX_VALUE;
        for (String word : wordFrequency.keySet()) {
            if (word.length() < minLength && word.length() > 0) {
                minLength = word.length();
                shortestWords.clear();
                shortestWords.add(word);
            } else if (word.length() == minLength) {
                shortestWords.add(word);
            }
        }

        // Находим самые частые слова
        int maxFrequency = 0;
        for (Map.Entry<String, Integer> entry : wordFrequency.entrySet()) {
            if (entry.getValue() > maxFrequency) {
                maxFrequency = entry.getValue();
                mostFrequentWords.clear();
                mostFrequentWords.add(entry.getKey());
            } else if (entry.getValue() == maxFrequency) {
                mostFrequentWords.add(entry.getKey());
            }
        }

        // Корректировка количества предложений, если оно нулевое
        if (sentenceCount == 0 && wordCount > 0) {
            sentenceCount = 1;
        }
    }

    /**
     * Сброс статистики
     */
    private void reset() {
        charCount = 0;
        wordCount = 0;
        lineCount = 0;
        sentenceCount = 0;
        whitespaceCount = 0;
        punctuationCount = 0;
        digitCount = 0;
        letterCount = 0;
        uniqueWords = 0;

        charFrequency.clear();
        wordFrequency.clear();
        wordLengthDistribution.clear();
        lineLengths.clear();
        longestWords.clear();
        mostFrequentWords.clear();
        shortestWords.clear();
    }

    // Геттеры для статистики
    public int getCharCount() { return charCount; }
    public int getWordCount() { return wordCount; }
    public int getLineCount() { return lineCount; }
    public int getSentenceCount() { return sentenceCount; }
    public int getWhitespaceCount() { return whitespaceCount; }
    public int getPunctuationCount() { return punctuationCount; }
    public int getDigitCount() { return digitCount; }
    public int getLetterCount() { return letterCount; }
    public int getUniqueWords() { return uniqueWords; }

    /**
     * Средняя длина слова
     */
    public double getAverageWordLength() {
        if (wordCount == 0) return 0.0;
        return (double) letterCount / wordCount;
    }

    /**
     * Средняя длина предложения (в словах)
     */
    public double getAverageSentenceLength() {
        if (sentenceCount == 0) return 0.0;
        return (double) wordCount / sentenceCount;
    }

    /**
     * Средняя длина строки (в символах)
     */
    public double getAverageLineLength() {
        if (lineCount == 0) return 0.0;
        return lineLengths.sum() / (double) lineCount;
    }

    /**
     * Частота символов
     */
    public Map<Character, Integer> getCharFrequency() {
        return Collections.unmodifiableMap(charFrequency);
    }

    /**
     * Частота слов
     */
    public Map<String, Integer> getWordFrequency() {
        return Collections.unmodifiableMap(wordFrequency);
    }

    /**
     * Распределение длин слов
     */
    public Map<Integer, Integer> getWordLengthDistribution() {
        return Collections.unmodifiableMap(wordLengthDistribution);
    }

    /**
     * Самые длинные слова
     */
    public List<String> getLongestWords() {
        return Collections.unmodifiableList(longestWords);
    }

    /**
     * Самые частые слова
     */
    public List<String> getMostFrequentWords() {
        return Collections.unmodifiableList(mostFrequentWords);
    }

    /**
     * Самые короткие слова
     */
    public List<String> getShortestWords() {
        return Collections.unmodifiableList(shortestWords);
    }

    /**
     * Длины строк
     */
    public IntList getLineLengths() {
        return lineLengths;
    }

    /**
     * Возвращает отчет в виде строки
     */
    public String generateReport() {
        StringBuilder report = new StringBuilder();
        report.append("=== ТЕКСТОВАЯ СТАТИСТИКА ===\n\n");

        report.append("ОБЩАЯ СТАТИСТИКА:\n");
        report.append(String.format("  Символы: %d\n", charCount));
        report.append(String.format("  Буквы: %d\n", letterCount));
        report.append(String.format("  Цифры: %d\n", digitCount));
        report.append(String.format("  Пробелы: %d\n", whitespaceCount));
        report.append(String.format("  Знаки препинания: %d\n", punctuationCount));
        report.append(String.format("  Строки: %d\n", lineCount));
        report.append(String.format("  Слова: %d\n", wordCount));
        report.append(String.format("  Уникальные слова: %d\n", uniqueWords));
        report.append(String.format("  Предложения: %d\n", sentenceCount));
        report.append("\n");

        report.append("СРЕДНИЕ ЗНАЧЕНИЯ:\n");
        report.append(String.format("  Средняя длина слова: %.2f символов\n",
                getAverageWordLength()));
        report.append(String.format("  Средняя длина предложения: %.2f слов\n",
                getAverageSentenceLength()));
        report.append(String.format("  Средняя длина строки: %.2f символов\n",
                getAverageLineLength()));
        report.append("\n");

        if (!longestWords.isEmpty()) {
            report.append("САМЫЕ ДЛИННЫЕ СЛОВА:\n");
            for (String word : longestWords) {
                report.append(String.format("  \"%s\" (%d символов)\n",
                        word, word.length()));
            }
            report.append("\n");
        }

        if (!shortestWords.isEmpty()) {
            report.append("САМЫЕ КОРОТКИЕ СЛОВА:\n");
            for (String word : shortestWords) {
                report.append(String.format("  \"%s\" (%d символов)\n",
                        word, word.length()));
            }
            report.append("\n");
        }

        if (!mostFrequentWords.isEmpty() && wordCount > 0) {
            int maxFreq = wordFrequency.get(mostFrequentWords.get(0));
            report.append("САМЫЕ ЧАСТЫЕ СЛОВА:\n");
            for (String word : mostFrequentWords) {
                double percentage = (maxFreq * 100.0) / wordCount;
                report.append(String.format("  \"%s\": %d раз (%.1f%%)\n",
                        word, maxFreq, percentage));
            }
            report.append("\n");
        }

        report.append("РАСПРЕДЕЛЕНИЕ ДЛИН СЛОВ:\n");
        List<Integer> lengths = new ArrayList<>(wordLengthDistribution.keySet());
        Collections.sort(lengths);
        for (int length : lengths) {
            int count = wordLengthDistribution.get(length);
            report.append(String.format("  %d символов: %d слов\n", length, count));
        }

        return report.toString();
    }

    /**
     * Возвращает краткий отчет
     */
    public String generateSummary() {
        return String.format(
                "Текст: %d символов, %d слов, %d строк, %d уникальных слов",
                charCount, wordCount, lineCount, uniqueWords
        );
    }

    /**
     * Экспорт статистики в файл
     */
    public void exportToFile(String filePath) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(filePath), StandardCharsets.UTF_8))) {

            writer.write(generateReport());

            // Дополнительно: экспорт частоты слов
            writer.write("\nЧАСТОТА СЛОВ:\n");
            List<Map.Entry<String, Integer>> sortedWords = new ArrayList<>(wordFrequency.entrySet());
            sortedWords.sort((a, b) -> {
                int freqCompare = b.getValue().compareTo(a.getValue());
                if (freqCompare != 0) return freqCompare;
                return a.getKey().compareTo(b.getKey());
            });

            for (Map.Entry<String, Integer> entry : sortedWords) {
                writer.write(String.format("%s: %d\n", entry.getKey(), entry.getValue()));
            }
        }
    }

    @Override
    public String toString() {
        return generateSummary();
    }
}