package analyzer.utils;

import java.text.Normalizer;
import java.util.regex.Pattern;

/**
 * Утилиты для работы со строками
 */
public class StringUtils {
    
    private StringUtils() {
        // Утилитарный класс
    }
    
    /**
     * Проверяет, является ли строка null или пустой
     */
    public static boolean isNullOrEmpty(String str) {
        return str == null || str.isEmpty();
    }
    
    /**
     * Проверяет, является ли строка null, пустой или состоит только из пробелов
     */
    public static boolean isNullOrBlank(String str) {
        return str == null || str.trim().isEmpty();
    }
    
    /**
     * Приводит строку к нижнему регистру, защищаясь от null
     */
    public static String toLowerCase(String str) {
        return str != null ? str.toLowerCase() : null;
    }
    
    /**
     * Приводит строку к верхнему регистру, защищаясь от null
     */
    public static String toUpperCase(String str) {
        return str != null ? str.toUpperCase() : null;
    }
    
    /**
     * Обрезает строку, защищаясь от null
     */
    public static String trim(String str) {
        return str != null ? str.trim() : null;
    }
    
    /**
     * Удаляет все пробельные символы из строки
     */
    public static String removeWhitespace(String str) {
        if (str == null) {
            return null;
        }
        return str.replaceAll("\\s+", "");
    }
    
    /**
     * Удаляет все небуквенные символы из строки (оставляет только буквы)
     */
    public static String removeNonLetters(String str) {
        if (str == null) {
            return null;
        }
        return str.replaceAll("[^\\p{L}]", "");
    }
    
    /**
     * Удаляет все нецифровые символы из строки
     */
    public static String removeNonDigits(String str) {
        if (str == null) {
            return null;
        }
        return str.replaceAll("[^0-9]", "");
    }
    
    /**
     * Нормализует строку: удаляет диакритические знаки (акценты)
     */
    public static String normalize(String str) {
        if (str == null) {
            return null;
        }
        
        String normalized = Normalizer.normalize(str, Normalizer.Form.NFD);
        Pattern pattern = Pattern.compile("\\p{InCombiningDiacriticalMarks}+");
        return pattern.matcher(normalized).replaceAll("");
    }
    
    /**
     * Проверяет, содержит ли строка только буквы
     */
    public static boolean isAlphabetic(String str) {
        if (str == null || str.isEmpty()) {
            return false;
        }
        
        for (int i = 0; i < str.length(); i++) {
            if (!Character.isLetter(str.charAt(i))) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * Проверяет, содержит ли строка только цифры
     */
    public static boolean isNumeric(String str) {
        if (str == null || str.isEmpty()) {
            return false;
        }
        
        for (int i = 0; i < str.length(); i++) {
            if (!Character.isDigit(str.charAt(i))) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * Проверяет, содержит ли строка только буквы и/или цифры
     */
    public static boolean isAlphanumeric(String str) {
        if (str == null || str.isEmpty()) {
            return false;
        }
        
        for (int i = 0; i < str.length(); i++) {
            char ch = str.charAt(i);
            if (!Character.isLetterOrDigit(ch)) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * Подсчитывает количество вхождений подстроки в строку
     */
    public static int countOccurrences(String str, String substring) {
        if (str == null || substring == null || substring.isEmpty()) {
            return 0;
        }
        
        int count = 0;
        int index = 0;
        
        while ((index = str.indexOf(substring, index)) != -1) {
            count++;
            index += substring.length();
        }
        
        return count;
    }
    
    /**
     * Обращает строку
     */
    public static String reverse(String str) {
        if (str == null) {
            return null;
        }
        
        return new StringBuilder(str).reverse().toString();
    }
    
    /**
     * Проверяет, является ли строка палиндромом
     */
    public static boolean isPalindrome(String str) {
        if (str == null) {
            return false;
        }
        
        String cleaned = str.replaceAll("[^\\p{L}\\p{N}]", "").toLowerCase();
        String reversed = reverse(cleaned);
        
        return cleaned.equals(reversed);
    }
    
    /**
     * Сокращает строку до указанной длины, добавляя многоточие при необходимости
     */
    public static String truncate(String str, int maxLength) {
        if (str == null || maxLength < 0) {
            return str;
        }
        
        if (str.length() <= maxLength) {
            return str;
        }
        
        if (maxLength <= 3) {
            return str.substring(0, maxLength);
        }
        
        return str.substring(0, maxLength - 3) + "...";
    }
    
    /**
     * Объединяет массив строк с указанным разделителем
     */
    public static String join(String[] parts, String delimiter) {
        if (parts == null || parts.length == 0) {
            return "";
        }
        
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < parts.length; i++) {
            if (i > 0) {
                sb.append(delimiter);
            }
            sb.append(parts[i]);
        }
        
        return sb.toString();
    }
    
    /**
     * Разбивает строку на слова (последовательности букв)
     */
    public static String[] splitWords(String text) {
        if (text == null) {
            return new String[0];
        }
        
        return text.split("[^\\p{L}']+");
    }
    
    /**
     * Приводит первую букву строки к верхнему регистру
     */
    public static String capitalize(String str) {
        if (str == null || str.isEmpty()) {
            return str;
        }
        
        return str.substring(0, 1).toUpperCase() + str.substring(1);
    }
    
    /**
     * Приводит первую букву каждого слова к верхнему регистру
     */
    public static String capitalizeWords(String str) {
        if (str == null || str.isEmpty()) {
            return str;
        }
        
        String[] words = str.split("\\s+");
        StringBuilder result = new StringBuilder();
        
        for (int i = 0; i < words.length; i++) {
            if (i > 0) {
                result.append(" ");
            }
            result.append(capitalize(words[i]));
        }
        
        return result.toString();
    }
}