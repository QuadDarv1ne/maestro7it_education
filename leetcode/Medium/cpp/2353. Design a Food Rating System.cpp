/**
 * https://leetcode.com/problems/design-a-food-rating-system/description/?envType=daily-question&envId=2025-09-17
 */

#include <string>
#include <unordered_map>
#include <map>
#include <set>
using namespace std;

class FoodRatings {
    // карта: кухня -> множество пар (-рейтинг, название блюда)
    unordered_map<string, set<pair<int, string>>> cuisineMap;
    // food -> кухня
    unordered_map<string, string> foodToCuisine;
    // food -> рейтинг
    unordered_map<string, int> foodToRating;

public:
    FoodRatings(vector<string>& foods, vector<string>& cuisines, vector<int>& ratings) {
        int n = foods.size();
        for (int i = 0; i < n; i++) {
            string food = foods[i];
            string cuisine = cuisines[i];
            int rating = ratings[i];
            foodToCuisine[food] = cuisine;
            foodToRating[food] = rating;
            // вставляем пару: отрицательный рейтинг, чтобы наименьшая пара соответствовала наивысшему рейтингу
            cuisineMap[cuisine].insert({ -rating, food });
        }
    }

    void changeRating(string food, int newRating) {
        string cuisine = foodToCuisine[food];
        int oldRating = foodToRating[food];
        // удаляем старую пару
        cuisineMap[cuisine].erase({ -oldRating, food });
        // вставляем новую
        cuisineMap[cuisine].insert({ -newRating, food });
        // обновляем рейтинг
        foodToRating[food] = newRating;
    }

    string highestRated(string cuisine) {
        // самое "маленькое" в множестве — это пара с наивысшим rating
        auto it = cuisineMap[cuisine].begin();
        return it->second;
    }
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