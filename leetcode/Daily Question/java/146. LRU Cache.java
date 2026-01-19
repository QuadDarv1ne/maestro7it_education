/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

/**
 * @brief Класс LRU (Least Recently Used) кэша
 * 
 * Реализация с использованием:
 * 1. HashMap для быстрого доступа
 * 2. Двусвязного списка для отслеживания порядка
 */
class LRUCache {
    /**
     * @brief Узел двусвязного списка
     */
    class Node {
        int key;
        int value;
        Node prev;
        Node next;
        
        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }
    
    private final int capacity;
    private final Map<Integer, Node> cache;
    private final Node head;  // фиктивный узел
    private final Node tail;  // фиктивный узел
    
    /**
     * @brief Конструктор LRU кэша
     */
    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new HashMap<>();
        
        // Инициализация фиктивных узлов
        this.head = new Node(-1, -1);
        this.tail = new Node(-1, -1);
        head.next = tail;
        tail.prev = head;
    }
    
    /**
     * @brief Удаляет узел из списка
     */
    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    /**
     * @brief Добавляет узел в начало списка
     */
    private void addToFront(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
    
    /**
     * @brief Перемещает узел в начало списка
     */
    private void moveToFront(Node node) {
        removeNode(node);
        addToFront(node);
    }
    
    /**
     * @brief Удаляет самый старый узел
     */
    private void removeLRU() {
        Node lru = tail.prev;
        removeNode(lru);
        cache.remove(lru.key);
    }
    
    /**
     * @brief Получает значение по ключу
     */
    public int get(int key) {
        if (!cache.containsKey(key)) {
            return -1;
        }
        
        Node node = cache.get(key);
        moveToFront(node);  // Обновляем порядок использования
        return node.value;
    }
    
    /**
     * @brief Добавляет или обновляет пару ключ-значение
     */
    public void put(int key, int value) {
        if (cache.containsKey(key)) {
            // Обновляем существующий
            Node node = cache.get(key);
            node.value = value;
            moveToFront(node);
        } else {
            // Добавляем новый
            if (cache.size() >= capacity) {
                removeLRU();
            }
            
            Node newNode = new Node(key, value);
            addToFront(newNode);
            cache.put(key, newNode);
        }
    }
}