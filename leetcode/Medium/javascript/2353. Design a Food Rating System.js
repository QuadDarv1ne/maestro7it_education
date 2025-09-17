/**
 * https://leetcode.com/problems/design-a-food-rating-system/description/?envType=daily-question&envId=2025-09-17
 */

// В JS нет встроенного сбалансированного дерева, поэтому можно сделать:
 // - использовать библиотеку (если разрешено)
 // - или использовать heap + lazy removals + хэш для текущего рейтинга

class FoodRatings {
    /**
     * Храним:
     * - foodToCuisine: Map food -> cuisine
     * - foodToRating: Map food -> rating
     * - cuisineToHeap: Map cuisine -> max-heap (с lazy удалением)
     */
    constructor(foods, cuisines, ratings) {
        this.foodToCuisine = new Map();
        this.foodToRating = new Map();
        this.cuisineToHeap = new Map();

        for (let i = 0; i < foods.length; i++) {
            const food = foods[i];
            const cuisine = cuisines[i];
            const rating = ratings[i];
            this.foodToCuisine.set(food, cuisine);
            this.foodToRating.set(food, rating);
            if (!this.cuisineToHeap.has(cuisine)) {
                this.cuisineToHeap.set(cuisine, []);
            }
            this._heapPush(this.cuisineToHeap.get(cuisine), { food, rating });
        }
    }

    // правильный компаратор: max-heap по рейтингу, при равенстве — по food лексикографически
    _compare(a, b) {
        if (a.rating !== b.rating) return b.rating - a.rating; // выше больший рейтинг
        return a.food.localeCompare(b.food); // выше меньший food (по алфавиту)
    }

    _heapPush(heap, val) {
        heap.push(val);
        this._siftUp(heap, heap.length - 1);
    }

    _heapPop(heap) {
        const last = heap.pop();
        if (heap.length > 0) {
            heap[0] = last;
            this._siftDown(heap, 0);
        }
    }

    _siftUp(heap, idx) {
        while (idx > 0) {
            const parent = Math.floor((idx - 1) / 2);
            if (this._compare(heap[idx], heap[parent]) < 0) {
                [heap[idx], heap[parent]] = [heap[parent], heap[idx]];
                idx = parent;
            } else break;
        }
    }

    _siftDown(heap, idx) {
        const n = heap.length;
        while (true) {
            let best = idx;
            const left = 2 * idx + 1;
            const right = 2 * idx + 2;
            if (left < n && this._compare(heap[left], heap[best]) < 0) best = left;
            if (right < n && this._compare(heap[right], heap[best]) < 0) best = right;
            if (best !== idx) {
                [heap[idx], heap[best]] = [heap[best], heap[idx]];
                idx = best;
            } else break;
        }
    }

    changeRating(food, newRating) {
        const cuisine = this.foodToCuisine.get(food);
        this.foodToRating.set(food, newRating);
        this._heapPush(this.cuisineToHeap.get(cuisine), { food, rating: newRating });
    }

    highestRated(cuisine) {
        const heap = this.cuisineToHeap.get(cuisine);
        while (heap.length > 0) {
            const top = heap[0];
            const currRating = this.foodToRating.get(top.food);
            if (top.rating === currRating) return top.food; // актуальная запись
            this._heapPop(heap); // иначе устаревшее — удаляем
        }
        return "";
    }
}


/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/