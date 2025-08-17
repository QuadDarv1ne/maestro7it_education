/**
 * https://leetcode.com/problems/kth-largest-element-in-an-array/description/
 */

class MinHeap {
    constructor() { this.heap = []; }
    size() { return this.heap.length; }
    peek() { return this.heap[0]; }
    push(val) {
        this.heap.push(val);
        let i = this.heap.length - 1;
        while (i > 0) {
            let p = Math.floor((i - 1) / 2);
            if (this.heap[p] <= this.heap[i]) break;
            [this.heap[p], this.heap[i]] = [this.heap[i], this.heap[p]];
            i = p;
        }
    }
    pop() {
        const top = this.heap[0];
        const end = this.heap.pop();
        if (this.heap.length === 0) return top;
        this.heap[0] = end;
        let i = 0;
        while (true) {
            let left = 2*i + 1, right = 2*i + 2, smallest = i;
            if (left < this.heap.length && this.heap[left] < this.heap[smallest]) smallest = left;
            if (right < this.heap.length && this.heap[right] < this.heap[smallest]) smallest = right;
            if (smallest === i) break;
            [this.heap[i], this.heap[smallest]] = [this.heap[smallest], this.heap[i]];
            i = smallest;
        }
        return top;
    }
}

var findKthLargest = function(nums, k) {
    let heap = new MinHeap();
    for (let num of nums) {
        heap.push(num);
        if (heap.size() > k) heap.pop();
    }
    return heap.peek();
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/