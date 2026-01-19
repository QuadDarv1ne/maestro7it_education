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
 * Реализация LRU-кэша с использованием:
 * 1. Двусвязного списка для отслеживания порядка использования
 * 2. Хэш-таблицы для быстрого доступа по ключу
 * 
 * Сложность операций:
 * - get: O(1)
 * - put: O(1)
 * 
 * Принцип работы:
 * 1. При обращении к элементу он перемещается в начало списка (как самый "свежий")
 * 2. При добавлении нового элемента:
 *    - Если элемент уже есть, обновляем значение и перемещаем в начало
 *    - Если места нет, удаляем последний элемент (самый "старый")
 */
class LRUCache {
private:
    /**
     * @brief Узел двусвязного списка
     */
    struct Node {
        int key;
        int value;
        Node* prev;
        Node* next;
        
        Node(int k, int v) : key(k), value(v), prev(nullptr), next(nullptr) {}
    };
    
    int capacity;
    unordered_map<int, Node*> cache;
    Node* head;  // фиктивный узел для начала списка
    Node* tail;  // фиктивный узел для конца списка
    
    /**
     * @brief Удаляет узел из списка
     */
    void removeNode(Node* node) {
        node->prev->next = node->next;
        node->next->prev = node->prev;
    }
    
    /**
     * @brief Добавляет узел в начало списка
     */
    void addToFront(Node* node) {
        node->next = head->next;
        node->prev = head;
        head->next->prev = node;
        head->next = node;
    }
    
    /**
     * @brief Перемещает узел в начало списка
     */
    void moveToFront(Node* node) {
        removeNode(node);
        addToFront(node);
    }
    
    /**
     * @brief Удаляет самый старый узел (с конца списка)
     * @return Ключ удаленного узла
     */
    int removeLRU() {
        Node* lru = tail->prev;
        removeNode(lru);
        int key = lru->key;
        delete lru;
        return key;
    }

public:
    /**
     * @brief Конструктор LRU кэша
     * @param capacity Максимальная емкость кэша
     */
    LRUCache(int capacity) {
        this->capacity = capacity;
        head = new Node(-1, -1);  // фиктивная голова
        tail = new Node(-1, -1);  // фиктивный хвост
        head->next = tail;
        tail->prev = head;
    }
    
    /**
     * @brief Получает значение по ключу
     * @param key Ключ для поиска
     * @return Значение ключа или -1, если ключ не найден
     */
    int get(int key) {
        if (cache.find(key) == cache.end()) {
            return -1;
        }
        
        Node* node = cache[key];
        moveToFront(node);  // Обновляем как недавно использованный
        return node->value;
    }
    
    /**
     * @brief Добавляет или обновляет пару ключ-значение
     * @param key Ключ
     * @param value Значение
     */
    void put(int key, int value) {
        if (cache.find(key) != cache.end()) {
            // Ключ уже существует, обновляем значение и перемещаем в начало
            Node* node = cache[key];
            node->value = value;
            moveToFront(node);
        } else {
            // Новый ключ
            if (cache.size() >= capacity) {
                // Удаляем самый старый элемент
                int removedKey = removeLRU();
                cache.erase(removedKey);
            }
            
            // Добавляем новый узел
            Node* newNode = new Node(key, value);
            addToFront(newNode);
            cache[key] = newNode;
        }
    }
    
    /**
     * @brief Деструктор для очистки памяти
     */
    ~LRUCache() {
        Node* current = head;
        while (current) {
            Node* next = current->next;
            delete current;
            current = next;
        }
    }
};