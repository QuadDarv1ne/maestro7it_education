/**
 * https://leetcode.com/problems/design-a-food-rating-system/description/?envType=daily-question&envId=2025-09-17
 */

using System;
using System.Collections.Generic;

public class FoodRatings {
    /// <summary>
    /// Храним:
    /// - foodToCuisine: Dictionary<string, string>
    /// - foodToRating: Dictionary<string, int>
    /// - cuisineToSet: Dictionary<string, SortedSet<Food>>, где Food — класс с полями Name, Rating, с компаратором
    /// </summary>

    private class Food : IComparable<Food> {
        public string Name;
        public int Rating;
        public Food(string name, int rating) {
            Name = name;
            Rating = rating;
        }
        public int CompareTo(Food other) {
            if (this.Rating != other.Rating) {
                // убывающий порядок по рейтингу
                return other.Rating.CompareTo(this.Rating);
            }
            // при равных — по имени
            return this.Name.CompareTo(other.Name);
        }
        public override bool Equals(object obj) {
            if (obj == null || !(obj is Food)) return false;
            Food f = (Food)obj;
            return this.Name == f.Name && this.Rating == f.Rating;
        }
        public override int GetHashCode() {
            return (Name, Rating).GetHashCode();
        }
    }

    private Dictionary<string, string> foodToCuisine;
    private Dictionary<string, int> foodToRating;
    private Dictionary<string, SortedSet<Food>> cuisineToSet;

    public FoodRatings(string[] foods, string[] cuisines, int[] ratings) {
        foodToCuisine = new Dictionary<string, string>();
        foodToRating = new Dictionary<string, int>();
        cuisineToSet = new Dictionary<string, SortedSet<Food>>();
        for (int i = 0; i < foods.Length; i++) {
            string food = foods[i];
            string cuisine = cuisines[i];
            int rating = ratings[i];
            foodToCuisine[food] = cuisine;
            foodToRating[food] = rating;
            if (!cuisineToSet.ContainsKey(cuisine)) {
                cuisineToSet[cuisine] = new SortedSet<Food>();
            }
            cuisineToSet[cuisine].Add(new Food(food, rating));
        }
    }

    public void ChangeRating(string food, int newRating) {
        string cuisine = foodToCuisine[food];
        int oldRating = foodToRating[food];
        SortedSet<Food> set = cuisineToSet[cuisine];
        set.Remove(new Food(food, oldRating));
        set.Add(new Food(food, newRating));
        foodToRating[food] = newRating;
    }

    public string HighestRated(string cuisine) {
        SortedSet<Food> set = cuisineToSet[cuisine];
        // SortedSet в C# не гарантирует, что .Min/.Max будет тот, кого мы хотим?
        // Но если сортировка сделана так, что первый элемент — нужный, то можно взять: через enumerator
        foreach (var f in set) {
            return f.Name;  // первый по итератору
        }
        return ""; // если нет блюд
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