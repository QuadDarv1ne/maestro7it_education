import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Library {
    private static final Logger LOGGER = Logger.getLogger(Library.class.getName());
    private List<Book> books;

    public Library() {
        this.books = new ArrayList<>();
    }

    public void addBook(Book book) {
        books.add(book);
        LOGGER.info("Книга добавлена: " + book.getTitle());
    }

    public boolean removeBook(String isbn) {
        for (Book book : books) {
            if (book.getIsbn().equals(isbn)) {
                books.remove(book);
                LOGGER.info("Книга удалена: " + book.getTitle());
                return true;
            }
        }
        LOGGER.warning("Книга с ISBN " + isbn + " не найдена.");
        return false;
    }

    public Book findBookByIsbn(String isbn) {
        for (Book book : books) {
            if (book.getIsbn().equals(isbn)) {
                return book;
            }
        }
        LOGGER.warning("Книга с ISBN " + isbn + " не найдена.");
        return null;
    }

    public void checkOutBook(String isbn) {
        Book book = findBookByIsbn(isbn);
        if (book != null && !book.isCheckedOut()) {
            book.checkOut();
            LOGGER.info("Книга выдана: " + book.getTitle());
        } else {
            LOGGER.warning("Книга недоступна для выдачи.");
        }
    }

    public void returnBook(String isbn) {
        Book book = findBookByIsbn(isbn);
        if (book != null && book.isCheckedOut()) {
            book.returnBook();
            LOGGER.info("Книга возвращена: " + book.getTitle());
        } else {
            LOGGER.warning("Книга не была выдана.");
        }
    }

    public void listBooks() {
        if (books.isEmpty()) {
            LOGGER.info("Нет доступных книг.");
        } else {
            for (Book book : books) {
                System.out.println(book);
            }
        }
    }

    public void saveToFile(String filename) {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(filename))) {
            oos.writeObject(books);
            LOGGER.info("Данные сохранены в файл: " + filename);
        } catch (IOException e) {
            LOGGER.log(Level.SEVERE, "Ошибка при сохранении данных", e);
        }
    }

    @SuppressWarnings("unchecked")
    public void loadFromFile(String filename) {
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(filename))) {
            books = (List<Book>) ois.readObject();
            LOGGER.info("Данные загружены из файла: " + filename);
        } catch (IOException | ClassNotFoundException e) {
            LOGGER.log(Level.SEVERE, "Ошибка при загрузке данных", e);
        }
    }
}
