/**
 * https://leetcode.com/problems/insert-delete-getrandom-o1/description/?envType=study-plan-v2&envId=top-interview-150
 */

#include <vector>
#include <unordered_map>
#include <cstdlib>
using namespace std;

class RandomizedSet {
private:
    vector<int> nums;
    unordered_map<int, int> pos;  // value -> index

public:
    RandomizedSet() {}

    bool insert(int val) {
        if (pos.count(val)) return false;
        nums.push_back(val);
        pos[val] = nums.size() - 1;
        return true;
    }

    bool remove(int val) {
        if (!pos.count(val)) return false;
        int idx = pos[val];
        int last = nums.back();
        nums[idx] = last;
        pos[last] = idx;
        nums.pop_back();
        pos.erase(val);
        return true;
    }

    int getRandom() {
        int idx = rand() % nums.size();
        return nums[idx];
    }
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