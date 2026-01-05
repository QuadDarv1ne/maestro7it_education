package tasks;

import analyzer.utils.Logger;

/**
 * Решение задачи "Топ слов"
 * Выводит топ N наиболее частых слов с их частотами
 * Поддерживает параллельную обработку для больших файлов
 */
public class TopWordsTask {

    /**
     * Обрабатывает входной файл и записывает топ слов в выходной
     */
    public static void processFile(String inputFile, String outputFile, int topN) throws IOException {
        Logger.logTaskStart("Топ слов", inputFile);
        long startTime = System.currentTimeMillis();
        
        File file = new File(inputFile);
        long fileSize = file.length();
        
        WordStatistics statistics;
        
        // Используем параллельную обработку для файлов > 1MB
        if (fileSize > 1024 * 1024 && AppConfig.USE_PARALLEL_PROCESSING) {
            Logger.info("Используется параллельная обработка для файла размером " + fileSize + " байт");
            statistics = processFileParallel(inputFile);
        } else {
            Logger.info("Используется последовательная обработка");
            statistics = processFileSequential(inputFile);
        }
        
        writeTopWords(outputFile, statistics, topN);
        
        long endTime = System.currentTimeMillis();
        Logger.logTaskEnd("Топ слов", outputFile, endTime - startTime);
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