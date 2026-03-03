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

public class LRUCache
{
    private class DLinkedNode
    {
        public int key;
        public int value;
        public DLinkedNode prev;
        public DLinkedNode next;
        
        public DLinkedNode(int key = 0, int value = 0)
        {
            this.key = key;
            this.value = value;
        }
    }
    
    private int capacity;
    private Dictionary<int, DLinkedNode> cache;
    private DLinkedNode head;
    private DLinkedNode tail;
    
    public LRUCache(int capacity)
    {
        this.capacity = capacity;
        cache = new Dictionary<int, DLinkedNode>();
        head = new DLinkedNode();
        tail = new DLinkedNode();
        head.next = tail;
        tail.prev = head;
    }
    
    private void AddToHead(DLinkedNode node)
    {
        node.prev = head;
        node.next = head.next;
        head.next.prev = node;
        head.next = node;
    }
    
    private void RemoveNode(DLinkedNode node)
    {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    private void MoveToHead(DLinkedNode node)
    {
        RemoveNode(node);
        AddToHead(node);
    }
    
    private DLinkedNode RemoveTail()
    {
        DLinkedNode node = tail.prev;
        RemoveNode(node);
        return node;
    }
    
    public int Get(int key)
    {
        if (cache.TryGetValue(key, out DLinkedNode node))
        {
            MoveToHead(node);
            return node.value;
        }
        return -1;
    }
    
    public void Put(int key, int value)
    {
        if (cache.TryGetValue(key, out DLinkedNode node))
        {
            node.value = value;
            MoveToHead(node);
        }
        else
        {
            DLinkedNode newNode = new DLinkedNode(key, value);
            cache.Add(key, newNode);
            AddToHead(newNode);
            if (cache.Count > capacity)
            {
                DLinkedNode toRemove = RemoveTail();
                cache.Remove(toRemove.key);
            }
        }
    }
}