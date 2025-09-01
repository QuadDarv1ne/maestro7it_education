/**
 * https://leetcode.com/problems/maximum-average-pass-ratio/description/?envType=daily-question&envId=2025-09-01
 */

// JavaScript — LeetCode
// Реализуем max-heap вручную; храним объекты {p,t} и сравниваем по gain.
function gain(p, t) {
  return (p + 1) / (t + 1) - p / t;
}

class MaxHeap {
  constructor() { this.a = []; }
  size() { return this.a.length; }
  push(node) {
    this.a.push(node); this._siftUp(this.a.length - 1);
  }
  pop() {
    if (this.a.length === 0) return null;
    const top = this.a[0];
    const last = this.a.pop();
    if (this.a.length) { this.a[0] = last; this._siftDown(0); }
    return top;
  }
  _siftUp(i) {
    while (i > 0) {
      const p = Math.floor((i - 1) / 2);
      if (gain(this.a[i].p, this.a[i].t) <= gain(this.a[p].p, this.a[p].t)) break;
      [this.a[i], this.a[p]] = [this.a[p], this.a[i]];
      i = p;
    }
  }
  _siftDown(i) {
    const n = this.a.length;
    while (true) {
      let largest = i;
      const l = 2*i + 1, r = 2*i + 2;
      if (l < n && gain(this.a[l].p, this.a[l].t) > gain(this.a[largest].p, this.a[largest].t)) largest = l;
      if (r < n && gain(this.a[r].p, this.a[r].t) > gain(this.a[largest].p, this.a[largest].t)) largest = r;
      if (largest === i) break;
      [this.a[i], this.a[largest]] = [this.a[largest], this.a[i]];
      i = largest;
    }
  }
}

var maxAverageRatio = function(classes, extraStudents) {
  const heap = new MaxHeap();
  for (const c of classes) heap.push({p: c[0], t: c[1]});
  while (extraStudents-- > 0) {
    const cur = heap.pop();
    cur.p += 1; cur.t += 1;
    heap.push(cur);
  }
  let sum = 0.0;
  for (const node of heap.a) sum += node.p / node.t;
  return sum / classes.length;
};

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