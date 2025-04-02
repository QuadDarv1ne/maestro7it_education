import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

public class LibraryManagementSystem {
    private static final Logger LOGGER = Logger.getLogger(LibraryManagementSystem.class.getName());

    public static void main(String[] args) {
        Library library = new Library();
        Scanner scanner = new Scanner(System.in);

        library.loadFromFile("library.dat");

        while (true) {
            System.out.println("\nСистема управления библиотекой");
            System.out.println("1. Добавить книгу");
            System.out.println("2. Удалить книгу");
            System.out.println("3. Выдать книгу");
            System.out.println("4. Вернуть книгу");
            System.out.println("5. Список книг");
            System.out.println("6. Сохранить и выйти");
            System.out.print("Выберите опцию: ");
            int choice = scanner.nextInt();
            scanner.nextLine(); // Чтение символа новой строки

            switch (choice) {
                case 1:
                    addBook(scanner, library);
                    break;
                case 2:
                    removeBook(scanner, library);
                    break;
                case 3:
                    checkOutBook(scanner, library);
                    break;
                case 4:
                    returnBook(scanner, library);
                    break;
                case 5:
                    library.listBooks();
                    break;
                case 6:
                    library.saveToFile("library.dat");
                    LOGGER.info("Данные сохранены. Выход...");
                    scanner.close();
                    return;
                default:
                    LOGGER.warning("Неверная опция. Пожалуйста, попробуйте снова.");
            }
        }
    }

    private static void addBook(Scanner scanner, Library library) {
        System.out.print("Введите название: ");
        String title = scanner.nextLine();
        System.out.print("Введите автора: ");
        String author = scanner.nextLine();
        System.out.print("Введите ISBN: ");
        String isbn = scanner.nextLine();
        library.addBook(new Book(title, author, isbn));
    }

    private static void removeBook(Scanner scanner, Library library) {
        System.out.print("Введите ISBN для удаления: ");
        String isbn = scanner.nextLine();
        if (library.removeBook(isbn)) {
            LOGGER.info("Книга удалена.");
        } else {
            LOGGER.warning("Книга не найдена.");
        }
    }

    private static void checkOutBook(Scanner scanner, Library library) {
        System.out.print("Введите ISBN для выдачи: ");
        String isbn = scanner.nextLine();
        library.checkOutBook(isbn);
    }

    private static void returnBook(Scanner scanner, Library library) {
        System.out.print("Введите ISBN для возврата: ");
        String isbn = scanner.nextLine();
        library.returnBook(isbn);
    }
}
