import tasks.ReverseTask;
import tasks.WordStatPlusTask;
import java.util.Scanner;

/**
 * Главный класс приложения TextAnalyzerPro
 */
public class Main {
    
    public static void main(String[] args) {
        System.out.println("TextAnalyzerPro v" + AppConfig.VERSION);
        System.out.println();
        
        if (args.length == 0) {
            runInteractiveMode();
            return;
        }
        
        String command = args[0].toLowerCase();
        
        try {
            switch (command) {
                case "reverse":
                    if (args.length == 3) {
                        if (!new java.io.File(args[1]).exists()) {
                            System.err.println("Ошибка: Входной файл не найден: " + args[1]);
                            return;
                        }
                        if (new java.io.File(args[1]).length() > AppConfig.MAX_FILE_SIZE) {
                            System.err.println("Ошибка: Файл слишком большой (макс. " + AppConfig.MAX_FILE_SIZE / (1024 * 1024) + "MB)");
                            return;
                        }
                        ReverseTask.main(new String[]{args[1], args[2]});
                    } else {
                        printUsage();
                    }
                    break;
                    
                case "wordstat":
                case "wordstatplus":
                    if (args.length == 3) {
                        if (!new java.io.File(args[1]).exists()) {
                            System.err.println("Ошибка: Входной файл не найден: " + args[1]);
                            return;
                        }
                        if (new java.io.File(args[1]).length() > AppConfig.MAX_FILE_SIZE) {
                            System.err.println("Ошибка: Файл слишком большой (макс. " + AppConfig.MAX_FILE_SIZE / (1024 * 1024) + "MB)");
                            return;
                        }
                        WordStatPlusTask.main(new String[]{args[1], args[2]});
                    } else {
                        printUsage();
                    }
                    break;
                    
                case "config":
                    AppConfig.printConfig();
                    break;
                    
                case "help":
                    printHelp();
                    break;
                    
                default:
                    System.err.println("Неизвестная команда: " + command);
                    printUsage();
                    break;
            }
        } catch (Exception e) {
            System.err.println("Ошибка: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private static void runInteractiveMode() {
        Scanner consoleScanner = new Scanner(System.in, "UTF-8");
        
        System.out.println("╔════════════════════════════════════╗");
        System.out.println("║      TextAnalyzerPro v1.0          ║");
        System.out.println("╚════════════════════════════════════╝");
        System.out.println();
        System.out.println("Доступные задачи:");
        System.out.println("1. Реверс (обратный порядок чисел)");
        System.out.println("2. Статистика слов++ (частоты и позиции)");
        System.out.println("3. Выход");
        System.out.println();
        
        while (true) {
            System.out.print("Выберите задачу (1-3): ");
            String choice = consoleScanner.nextLine().trim();
            
            switch (choice) {
                case "1":
                    runReverseTask(consoleScanner);
                    break;
                    
                case "2":
                    runWordStatTask(consoleScanner);
                    break;
                    
                case "3":
                    System.out.println("Выход из программы...");
                    consoleScanner.close();
                    return;
                    
                default:
                    System.out.println("Неверный выбор. Попробуйте снова.");
                    break;
            }
            
            System.out.println();
        }
    }
    
    private static void runReverseTask(Scanner consoleScanner) {
        System.out.println("\n=== Задача 'Реверс' ===");
        System.out.print("Входной файл: ");
        String inputFile = consoleScanner.nextLine().trim();
        
        java.io.File file = new java.io.File(inputFile);
        if (!file.exists()) {
            System.err.println("✗ Ошибка: Входной файл не найден: " + inputFile);
            return;
        }
        if (file.length() > AppConfig.MAX_FILE_SIZE) {
            System.err.println("✗ Ошибка: Файл слишком большой (макс. " + AppConfig.MAX_FILE_SIZE / (1024 * 1024) + "MB)");
            return;
        }
        
        System.out.print("Выходной файл: ");
        String outputFile = consoleScanner.nextLine().trim();
        
        try {
            ReverseTask.processFile(inputFile, outputFile);
            System.out.println("✓ Задача успешно выполнена!");
            System.out.println("Результат сохранен в: " + outputFile);
        } catch (Exception e) {
            System.err.println("✗ Ошибка: " + e.getMessage());
        }
    }
    
    private static void runWordStatTask(Scanner consoleScanner) {
        System.out.println("\n=== Задача 'Статистика слов++' ===");
        System.out.print("Входной файл: ");
        String inputFile = consoleScanner.nextLine().trim();
        
        java.io.File file = new java.io.File(inputFile);
        if (!file.exists()) {
            System.err.println("✗ Ошибка: Входной файл не найден: " + inputFile);
            return;
        }
        if (file.length() > AppConfig.MAX_FILE_SIZE) {
            System.err.println("✗ Ошибка: Файл слишком большой (макс. " + AppConfig.MAX_FILE_SIZE / (1024 * 1024) + "MB)");
            return;
        }
        
        System.out.print("Выходной файл: ");
        String outputFile = consoleScanner.nextLine().trim();
        
        try {
            WordStatPlusTask.processFile(inputFile, outputFile);
            System.out.println("✓ Задача успешно выполнена!");
            System.out.println("Статистика сохранена в: " + outputFile);
        } catch (Exception e) {
            System.err.println("✗ Ошибка: " + e.getMessage());
        }
    }
    
    private static void printUsage() {
        System.err.println("Использование:");
        System.err.println("  java Main <команда> <входной-файл> <выходной-файл>");
        System.err.println();
        System.err.println("Команды:");
        System.err.println("  reverse     - задача 'Реверс'");
        System.err.println("  wordstat    - задача 'Статистика слов++'");
        System.err.println("  config      - показать конфигурацию");
        System.err.println("  help        - показать эту справку");
        System.err.println();
        System.err.println("Примеры:");
        System.err.println("  java Main reverse input.txt output.txt");
        System.err.println("  java Main wordstat text.txt stats.txt");
        System.err.println("  java Main config");
    }
    
    private static void printHelp() {
        System.out.println("TextAnalyzerPro - Анализатор текста на Java");
        System.out.println();
        System.out.println("Задачи:");
        System.out.println("1. Реверс:");
        System.out.println("   Читает матрицу чисел из файла и выводит её");
        System.out.println("   в обратном порядке (строки и числа в строках)");
        System.out.println();
        System.out.println("2. Статистика слов++:");
        System.out.println("   Подсчитывает частоту каждого слова в тексте");
        System.out.println("   и выводит слова в порядке их первого появления");
        System.out.println("   с указанием количества и позиций каждого слова");
        System.out.println();
        System.out.println("Формат вывода для Статистики слов++:");
        System.out.println("   слово количество позиция1 позиция2 ...");
        System.out.println();
        System.out.println("Поддерживаемые кодировки: UTF-8");
        System.out.println("Поддержка Unicode: полная (кириллица, эмодзи и др.)");
    }
}