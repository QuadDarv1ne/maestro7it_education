package tasks;

import analyzer.statistics.TextStatistics;
import java.io.*;
import java.util.Scanner;

/**
 * Исполнитель задач с единым интерфейсом
 */
public class TaskExecutor {
    
    /**
     * Выполняет задачу в зависимости от команды
     */
    public static void execute(String command, String[] args) throws IOException {
        switch (command.toLowerCase()) {
            case "reverse":
                if (args.length != 2) {
                    throw new IllegalArgumentException(
                        "Для команды 'reverse' требуется 2 аргумента: входной и выходной файлы");
                }
                ReverseTask.processFile(args[0], args[1]);
                System.out.println("Задача 'Реверс' выполнена. Результат в: " + args[1]);
                break;
                
            case "wordstat":
                if (args.length != 2) {
                    throw new IllegalArgumentException(
                        "Для команды 'wordstat' требуется 2 аргумента: входной и выходной файлы");
                }
                WordStatTask.processFile(args[0], args[1]);
                System.out.println("Задача 'Статистика слов' выполнена. Результат в: " + args[1]);
                break;
                
            case "wordstatplus":
                if (args.length != 2) {
                    throw new IllegalArgumentException(
                        "Для команды 'wordstatplus' требуется 2 аргумента: входной и выходной файлы");
                }
                WordStatPlusTask.processFile(args[0], args[1]);
                System.out.println("Задача 'Статистика слов++' выполнена. Результат в: " + args[1]);
                break;
                
            case "textstats":
                if (args.length != 2) {
                    throw new IllegalArgumentException(
                        "Для команды 'textstats' требуется 2 аргумента: входной и выходной файлы");
                }
                TextStatistics stats = new TextStatistics();
                stats.analyzeFile(args[0]);
                stats.exportToFile(args[1]);
                System.out.println("Полная текстовая статистика сохранена в: " + args[1]);
                break;
                
            default:
                throw new IllegalArgumentException("Неизвестная команда: " + command);
        }
    }
    
    /**
     * Запускает интерактивный режим
     */
    public static void runInteractive() {
        Scanner console = new Scanner(System.in, "UTF-8");
        
        System.out.println("=== ТЕКСТОВЫЙ АНАЛИЗАТОР ===");
        System.out.println("Доступные команды:");
        System.out.println("  1. reverse     - перевернуть матрицу чисел");
        System.out.println("  2. wordstat    - базовая статистика слов");
        System.out.println("  3. wordstatplus - расширенная статистика слов (с позициями)");
        System.out.println("  4. textstats   - полная текстовая статистика");
        System.out.println("  5. help        - справка");
        System.out.println("  6. exit        - выход");
        
        while (true) {
            System.out.print("\nВведите команду: ");
            String command = console.nextLine().trim();
            
            if (command.equalsIgnoreCase("exit")) {
                System.out.println("Выход...");
                break;
            }
            
            if (command.equalsIgnoreCase("help")) {
                printHelp();
                continue;
            }
            
            try {
                System.out.print("Входной файл: ");
                String input = console.nextLine().trim();
                
                System.out.print("Выходной файл: ");
                String output = console.nextLine().trim();
                
                execute(command, new String[]{input, output});
                
            } catch (IllegalArgumentException e) {
                System.err.println("Ошибка: " + e.getMessage());
                System.out.println("Используйте 'help' для справки");
            } catch (IOException e) {
                System.err.println("Ошибка ввода-вывода: " + e.getMessage());
            } catch (Exception e) {
                System.err.println("Неожиданная ошибка: " + e.getMessage());
            }
        }
        
        console.close();
    }
    
    /**
     * Печатает справку
     */
    private static void printHelp() {
        System.out.println("\n=== СПРАВКА ПО КОМАНДАМ ===\n");
        
        System.out.println("reverse <input> <output>");
        System.out.println("  Читает матрицу чисел из input и записывает перевернутую матрицу в output");
        System.out.println("  Пример: reverse numbers.txt reversed.txt\n");
        
        System.out.println("wordstat <input> <output>");
        System.out.println("  Подсчитывает частоту слов в файле input");
        System.out.println("  Формат вывода: слово частота");
        System.out.println("  Пример: wordstat text.txt stats.txt\n");
        
        System.out.println("wordstatplus <input> <output>");
        System.out.println("  Подсчитывает частоту и позиции слов в файле input");
        System.out.println("  Формат вывода: слово частота позиция1 позиция2 ...");
        System.out.println("  Пример: wordstatplus text.txt stats_plus.txt\n");
        
        System.out.println("textstats <input> <output>");
        System.out.println("  Выполняет полный анализ текста (символы, слова, предложения)");
        System.out.println("  Пример: textstats article.txt analysis.txt\n");
    }
    
    /**
     * Основной метод для запуска из командной строки
     */
    public static void main(String[] args) {
        if (args.length == 0) {
            runInteractive();
            return;
        }
        
        String command = args[0];
        
        try {
            String[] taskArgs = new String[args.length - 1];
            System.arraycopy(args, 1, taskArgs, 0, taskArgs.length);
            
            execute(command, taskArgs);
        } catch (IllegalArgumentException e) {
            System.err.println("Ошибка аргументов: " + e.getMessage());
            System.out.println("\nИспользование: java TaskExecutor <команда> <аргументы>");
            System.out.println("Используйте: java TaskExecutor help - для справки");
        } catch (IOException e) {
            System.err.println("Ошибка ввода-вывода: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("Ошибка: " + e.getMessage());
        }
    }
}