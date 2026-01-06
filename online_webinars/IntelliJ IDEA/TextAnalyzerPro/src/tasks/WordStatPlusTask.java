package tasks;

import analyzer.AppConfig;
import analyzer.scanner.TextScanner;
import analyzer.statistics.WordStatistics;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.*;
import analyzer.AppConfig.*;

/**
 * Решение задачи "Статистика слов++"
 * Выводит слова в порядке их появления с количеством и позициями
 * Поддерживает параллельную обработку для больших файлов
 */
public class WordStatPlusTask {

    /**
     * Обрабатывает входной файл и записывает статистику в выходной
     */
    public static void processFile(String inputFile, String outputFile) throws IOException {
        File file = new File(inputFile);
        long fileSize = file.length();

        WordStatistics statistics;

        // Используем параллельную обработку для файлов > 1MB
        if (fileSize > 1024 * 1024 && AppConfig.USE_PARALLEL_PROCESSING) {
            statistics = processFileParallel(inputFile);
        } else {
            statistics = processFileSequential(inputFile);
        }

        writeStatistics(outputFile, statistics);
    }

    /**
     * Последовательная обработка файла
     */
    private static WordStatistics processFileSequential(String inputFile) throws IOException {
        WordStatistics statistics = new WordStatistics();

        try (TextScanner scanner = new TextScanner(new InputStreamReader(new FileInputStream(inputFile), StandardCharsets.UTF_8))) {
            String word;
            while ((word = scanner.nextWord()) != null) {
                statistics.addWord(word);
            }
        }

        return statistics;
    }

    /**
     * Параллельная обработка файла
     */
    private static WordStatistics processFileParallel(String inputFile) throws IOException {
        // Определяем количество потоков
        int numThreads = Math.min(AppConfig.MAX_THREADS, Runtime.getRuntime().availableProcessors());

        // Создаем ExecutorService
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);

        try {
            // Разделяем файл на части
            List<Future<WordStatistics>> futures = new ArrayList<>();

            long fileSize = new File(inputFile).length();
            long chunkSize = fileSize / numThreads;

            for (int i = 0; i < numThreads; i++) {
                long start = i * chunkSize;
                long end = (i == numThreads - 1) ? fileSize : (i + 1) * chunkSize;

                futures.add(executor.submit(new WordProcessor(inputFile, start, end)));
            }

            // Собираем результаты
            WordStatistics combinedStats = new WordStatistics();
            for (Future<WordStatistics> future : futures) {
                try {
                    WordStatistics partialStats = future.get();
                    // Объединяем статистику
                    for (String word : partialStats.getUniqueWords()) {
                        int freq = partialStats.getFrequency(word);
                        for (int j = 0; j < freq; j++) {
                            combinedStats.addWord(word);
                        }
                    }
                } catch (InterruptedException | ExecutionException e) {
                    throw new IOException("Ошибка при параллельной обработке", e);
                }
            }

            return combinedStats;

        } finally {
            executor.shutdown();
            try {
                if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                    executor.shutdownNow();
                }
            } catch (InterruptedException e) {
                executor.shutdownNow();
            }
        }
    }

    /**
     * Класс для обработки части файла в отдельном потоке
     */
    private static class WordProcessor implements Callable<WordStatistics> {
        private final String filePath;
        private final long startOffset;
        private final long endOffset;

        public WordProcessor(String filePath, long startOffset, long endOffset) {
            this.filePath = filePath;
            this.startOffset = startOffset;
            this.endOffset = endOffset;
        }

        @Override
        public WordStatistics call() throws Exception {
            WordStatistics statistics = new WordStatistics();

            try (RandomAccessFile raf = new RandomAccessFile(filePath, "r")) {
                raf.seek(startOffset);

                // Если не начало файла, пропускаем до границы слова
                if (startOffset > 0) {
                    skipToWordBoundary(raf);
                }

                // Читаем данные порциями
                byte[] buffer = new byte[8192];
                StringBuilder chunk = new StringBuilder();
                long currentPos = startOffset;

                while (currentPos < endOffset) {
                    int bytesRead = raf.read(buffer);
                    if (bytesRead == -1) break;

                    chunk.append(new String(buffer, 0, bytesRead, StandardCharsets.UTF_8));
                    currentPos += bytesRead;

                    // Если конец файла или буфер полон, обрабатываем
                    if (currentPos >= endOffset || chunk.length() > 65536) {
                        processChunk(chunk.toString(), statistics);
                        chunk.setLength(0);
                    }
                }

                // Обрабатываем оставшийся chunk
                if (chunk.length() > 0) {
                    processChunk(chunk.toString(), statistics);
                }
            }

            return statistics;
        }

        private void skipToWordBoundary(RandomAccessFile raf) throws IOException {
            int ch;
            while ((ch = raf.read()) != -1) {
                if (Character.isWhitespace(ch)) {
                    break;
                }
            }
        }

        private void processChunk(String chunk, WordStatistics statistics) {
            // Простая обработка - разделяем по пробелам
            // В реальности лучше использовать TextScanner
            String[] words = chunk.split("\\s+");
            for (String word : words) {
                word = word.replaceAll("[^\\p{L}]+", "").toLowerCase();
                if (!word.isEmpty()) {
                    statistics.addWord(word);
                }
            }
        }
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