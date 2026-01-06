package analyzer.statistics;

import analyzer.utils.IntList;
import java.util.*;

/**
 * Класс для сбора и анализа статистики слов в тексте
 */
public class WordStatistics {
    private final Map<String, IntList> wordPositions;
    private final Map<String, Integer> wordCount = new HashMap<>();
    private final List<String> wordsInOrder;
    private int totalWords;

    public WordStatistics() {
        this.wordPositions = new LinkedHashMap<>();
        this.wordsInOrder = new ArrayList<>();
        this.totalWords = 0;
    }

    /**
     * Добавляет слово в статистику
     */
    public void addWord(String word) {
        if (word == null || word.isEmpty()) {
            return;
        }

        String normalizedWord = normalizeWord(word);
        totalWords++;

        if (!wordPositions.containsKey(normalizedWord)) {
            wordPositions.put(normalizedWord, new IntList());
            wordsInOrder.add(normalizedWord);
        }

        wordPositions.get(normalizedWord).add(totalWords);
    }

    /**
     * Добавляет несколько слов
     */
    public void addWords(List<String> words) {
        for (String word : words) {
            addWord(word);
        }
    }

    /**
     * Добавляет все слова из массива
     */
    public void addWords(String[] words) {
        for (String word : words) {
            addWord(word);
        }
    }

    /**
     * Нормализует слово: приводит к нижнему регистру и обрезает
     */
    private String normalizeWord(String word) {
        return word.toLowerCase().trim();
    }

    /**
     * Возвращает общее количество слов
     */
    public int getTotalWords() {
        return totalWords;
    }

    /**
     * Возвращает количество уникальных слов
     */
    public int getUniqueWordsCount() {
        return wordPositions.size();
    }

    /**
     * Возвращает частоту встречаемости слова
     */
    public int getFrequency(String word) {
        String normalized = normalizeWord(word);
        IntList positions = wordPositions.get(normalized);
        return positions != null ? positions.size() : 0;
    }

    /**
     * Возвращает позиции слова в тексте
     */
    public IntList getPositions(String word) {
        String normalized = normalizeWord(word);
        IntList positions = wordPositions.get(normalized);
        return positions != null ? new IntList() : positions; // Возвращаем копию или пустой список
    }

    /**
     * Возвращает все слова в порядке их первого появления
     */
    public List<String> getWordsInOrder() {
        return new ArrayList<>(wordsInOrder);
    }

    /**
     * Возвращает словарь слово -> позиции
     */
    public Map<String, IntList> getWordPositions() {
        Map<String, IntList> copy = new LinkedHashMap<>();
        for (Map.Entry<String, IntList> entry : wordPositions.entrySet()) {
            copy.put(entry.getKey(), entry.getValue());
        }
        return copy;
    }

    /**
     * Возвращает список слов, отсортированный по частоте (по убыванию)
     */
    public List<Map.Entry<String, Integer>> getWordsByFrequency() {
        List<Map.Entry<String, Integer>> entries = new ArrayList<>();

        for (Map.Entry<String, IntList> entry : wordPositions.entrySet()) {
            entries.add(new AbstractMap.SimpleEntry<>(entry.getKey(), entry.getValue().size()));
        }

        entries.sort((e1, e2) -> {
            int freqCompare = e2.getValue().compareTo(e1.getValue());
            if (freqCompare != 0) {
                return freqCompare;
            }
            return e1.getKey().compareTo(e2.getKey());
        });

        return entries;
    }

    /**
     * Возвращает топ-N самых частых слов
     */
    public List<Map.Entry<String, Integer>> getTopWords(int n) {
        List<Map.Entry<String, Integer>> sorted = getWordsByFrequency();
        return sorted.subList(0, Math.min(n, sorted.size()));
    }

    /**
     * Возвращает самые редкие слова (с частотой 1)
     */
    public List<String> getHapaxLegomena() {
        List<String> hapax = new ArrayList<>();

        for (Map.Entry<String, IntList> entry : wordPositions.entrySet()) {
            if (entry.getValue().size() == 1) {
                hapax.add(entry.getKey());
            }
        }

        return hapax;
    }

    /**
     * Очищает статистику
     */
    public void clear() {
        wordPositions.clear();
        wordsInOrder.clear();
        totalWords = 0;
    }

    /**
     * Объединяет статистику с другой статистикой
     */
    public void merge(WordStatistics other) {
        for (Map.Entry<String, IntList> entry : other.wordPositions.entrySet()) {
            String word = entry.getKey();
            IntList otherPositions = entry.getValue();

            if (!wordPositions.containsKey(word)) {
                wordPositions.put(word, new IntList());
                wordsInOrder.add(word);
            }

            // Сдвигаем позиции из other на текущий totalWords
            IntList positions = wordPositions.get(word);
            for (int i = 0; i < otherPositions.size(); i++) {
                positions.add(otherPositions.get(i) + totalWords);
            }
        }

        totalWords += other.totalWords;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("Статистика слов:\n");
        sb.append("Всего слов: ").append(totalWords).append("\n");
        sb.append("Уникальных слов: ").append(getUniqueWordsCount()).append("\n");

        List<Map.Entry<String, Integer>> topWords = getTopWords(10);
        if (!topWords.isEmpty()) {
            sb.append("Топ-10 слов:\n");
            for (Map.Entry<String, Integer> entry : topWords) {
                sb.append("  ").append(entry.getKey()).append(": ").append(entry.getValue()).append("\n");
            }
        }

        return sb.toString();
    }

    /**
     * Экспортирует статистику в форматированную строку
     */
    public String exportStatistics() {
        StringBuilder sb = new StringBuilder();

        for (String word : wordsInOrder) {
            IntList positions = wordPositions.get(word);
            sb.append(word).append(" ").append(positions.size());

            for (int i = 0; i < positions.size(); i++) {
                sb.append(" ").append(positions.get(i));
            }

            sb.append("\n");
        }

        return sb.toString();
    }

    /**
     * Экспортирует статистику в CSV формат
     */
    public String exportToCSV() {
        StringBuilder sb = new StringBuilder();
        sb.append("Слово,Частота,Позиции\n");

        for (String word : wordsInOrder) {
            IntList positions = wordPositions.get(word);
            sb.append(word).append(",").append(positions.size()).append(",\"");

            for (int i = 0; i < positions.size(); i++) {
                if (i > 0) {
                    sb.append(" ");
                }
                sb.append(positions.get(i));
            }

            sb.append("\"\n");
        }

        return sb.toString();
    }

    public String[] getUniqueWords() {
        // Возвращаем массив уникальных слов
        return wordCount.keySet().toArray(new String[0]);
    }
}