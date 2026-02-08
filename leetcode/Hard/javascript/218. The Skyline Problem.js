/**
 * https://leetcode.com/problems/the-skyline-problem/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "218. The Skyline Problem"
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
 * Возвращает контур неба (skyline) для заданных зданий.
 * @param {number[][]} buildings - Массив зданий в формате [[left, right, height], ...]
 * @return {number[][]} Контур неба в формате [[x1, y1], [x2, y2], ...]
 */
var getSkyline = function(buildings) {
    const result = [];
    if (!buildings || buildings.length === 0) return result;
    
    // Создаем массив событий
    const events = [];
    for (const [left, right, height] of buildings) {
        // Начало здания - отрицательная высота
        events.push([left, -height]);
        // Конец здания - положительная высота
        events.push([right, height]);
    }
    
    // Сортируем события
    events.sort((a, b) => {
        if (a[0] !== b[0]) return a[0] - b[0];
        // При одинаковом X: начала перед концами
        return a[1] - b[1];
    });
    
    // Максимальная куча для хранения текущих высот
    // В JavaScript нет встроенной max-heap, используем массив с сортировкой
    const maxHeap = [0];  // Начинаем с уровня земли
    const heightCount = {0: 1};  // Счетчик для каждой высоты
    
    // Функция для добавления в кучу
    function addToHeap(height) {
        maxHeap.push(height);
        // Поднимаем элемент вверх для поддержания свойства max-heap
        let i = maxHeap.length - 1;
        while (i > 0 && maxHeap[Math.floor((i - 1) / 2)] < maxHeap[i]) {
            [maxHeap[Math.floor((i - 1) / 2)], maxHeap[i]] = 
            [maxHeap[i], maxHeap[Math.floor((i - 1) / 2)]];
            i = Math.floor((i - 1) / 2);
        }
    }
    
    // Функция для удаления максимального элемента
    function removeMaxFromHeap() {
        if (maxHeap.length === 1) return;
        
        // Заменяем корень последним элементом
        maxHeap[0] = maxHeap.pop();
        
        // Просеиваем вниз
        let i = 0;
        while (true) {
            let left = 2 * i + 1;
            let right = 2 * i + 2;
            let largest = i;
            
            if (left < maxHeap.length && maxHeap[left] > maxHeap[largest]) {
                largest = left;
            }
            if (right < maxHeap.length && maxHeap[right] > maxHeap[largest]) {
                largest = right;
            }
            
            if (largest === i) break;
            
            [maxHeap[i], maxHeap[largest]] = [maxHeap[largest], maxHeap[i]];
            i = largest;
        }
    }
    
    // Предыдущая максимальная высота
    let prevMax = 0;
    
    // Обрабатываем события
    for (const [x, height] of events) {
        if (height < 0) {
            // Начало здания
            const h = -height;
            addToHeap(h);
            heightCount[h] = (heightCount[h] || 0) + 1;
        } else {
            // Конец здания
            heightCount[height]--;
        }
        
        // Удаляем неактивные высоты из кучи
        while (heightCount[maxHeap[0]] === 0) {
            removeMaxFromHeap();
        }
        
        // Текущая максимальная высота
        const currentMax = maxHeap[0];
        
        // Если высота изменилась
        if (currentMax !== prevMax) {
            result.push([x, currentMax]);
            prevMax = currentMax;
        }
    }
    
    return result;
};