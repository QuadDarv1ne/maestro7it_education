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
 * 1. Dictionary для быстрого доступа
 * 2. LinkedList для отслеживания порядка использования
 */
public class LRUCache {
    private class Node {
        public int Key;
        public int Value;
        public Node Prev;
        public Node Next;
        
        public Node(int key, int value) {
            Key = key;
            Value = value;
        }
    }
    
    private readonly int capacity;
    private readonly Dictionary<int, Node> cache;
    private Node head;  // фиктивный узел для начала
    private Node tail;  // фиктивный узел для конца
    
    /**
     * @brief Конструктор LRU кэша
     */
    public LRUCache(int capacity) {
        this.capacity = capacity;
        cache = new Dictionary<int, Node>();
        
        // Инициализация фиктивных узлов
        head = new Node(-1, -1);
        tail = new Node(-1, -1);
        head.Next = tail;
        tail.Prev = head;
    }
    
    /**
     * @brief Удаляет узел из списка
     */
    private void RemoveNode(Node node) {
        node.Prev.Next = node.Next;
        node.Next.Prev = node.Prev;
    }
    
    /**
     * @brief Добавляет узел в начало списка
     */
    private void AddToFront(Node node) {
        node.Next = head.Next;
        node.Prev = head;
        head.Next.Prev = node;
        head.Next = node;
    }
    
    /**
     * @brief Перемещает узел в начало списка
     */
    private void MoveToFront(Node node) {
        RemoveNode(node);
        AddToFront(node);
    }
    
    /**
     * @brief Удаляет самый старый узел
     */
    private void RemoveLRU() {
        Node lru = tail.Prev;
        RemoveNode(lru);
        cache.Remove(lru.Key);
    }
    
    /**
     * @brief Получает значение по ключу
     */
    public int Get(int key) {
        if (!cache.ContainsKey(key)) {
            return -1;
        }
        
        Node node = cache[key];
        MoveToFront(node);  // Обновляем порядок использования
        return node.Value;
    }
    
    /**
     * @brief Добавляет или обновляет пару ключ-значение
     */
    public void Put(int key, int value) {
        if (cache.ContainsKey(key)) {
            // Обновляем существующий
            Node node = cache[key];
            node.Value = value;
            MoveToFront(node);
        } else {
            // Добавляем новый
            if (cache.Count >= capacity) {
                RemoveLRU();
            }
            
            Node newNode = new Node(key, value);
            AddToFront(newNode);
            cache[key] = newNode;
        }
    }
}