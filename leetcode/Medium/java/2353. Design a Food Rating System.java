/**
 * https://leetcode.com/problems/design-a-food-rating-system/description/?envType=daily-question&envId=2025-09-17
 */

import java.util.*;

public class FoodRatings {
    /**
     * Идея та же: для каждой кухни — TreeSet, где пары (rating, foodName), сортировка:
     * по рейтингу убывающему, при равенстве — по названию лексикографически
     * также словари: food -> cuisine, food -> rating
     */

    private Map<String, TreeSet<Food>> cuisineMap;
    private Map<String, String> foodToCuisine;
    private Map<String, Integer> foodToRating;

    private static class Food implements Comparable<Food> {
        String name;
        int rating;
        Food(String n, int r) {
            name = n;
            rating = r;
        }
        public int compareTo(Food other) {
            // сначала по рейтингу убывающему
            if (this.rating != other.rating) {
                return other.rating - this.rating;
            }
            // при равенстве рейтингов — по имени
            return this.name.compareTo(other.name);
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof Food)) return false;
            Food f = (Food) o;
            return rating == f.rating && name.equals(f.name);
        }

        @Override
        public int hashCode() {
            return Objects.hash(name, rating);
        }
    }

    public FoodRatings(String[] foods, String[] cuisines, int[] ratings) {
        cuisineMap = new HashMap<>();
        foodToCuisine = new HashMap<>();
        foodToRating = new HashMap<>();

        for (int i = 0; i < foods.length; i++) {
            String food = foods[i];
            String cuisine = cuisines[i];
            int rating = ratings[i];
            foodToCuisine.put(food, cuisine);
            foodToRating.put(food, rating);
            cuisineMap.computeIfAbsent(cuisine, k -> new TreeSet<>()).add(new Food(food, rating));
        }
    }

    public void changeRating(String food, int newRating) {
        String cuisine = foodToCuisine.get(food);
        int oldRating = foodToRating.get(food);
        TreeSet<Food> set = cuisineMap.get(cuisine);
        // удаляем старый объект
        set.remove(new Food(food, oldRating));
        // добавляем новый
        set.add(new Food(food, newRating));
        foodToRating.put(food, newRating);
    }

    public String highestRated(String cuisine) {
        TreeSet<Food> set = cuisineMap.get(cuisine);
        return set.first().name;
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