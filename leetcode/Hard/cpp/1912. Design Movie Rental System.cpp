/**
 * https://leetcode.com/problems/design-movie-rental-system/
 */

#include <bits/stdc++.h>
using namespace std;

struct Entry {
    int price, shop, movie;
    bool operator<(const Entry& other) const {
        if (price != other.price) return price < other.price;
        if (shop != other.shop) return shop < other.shop;
        return movie < other.movie;
    }
};

class MovieRentingSystem {
    unordered_map<long long, int> priceMap; // (shop * 1e5 + movie) -> price
    unordered_map<int, set<Entry>> availableByMovie; // movie -> set of entries
    set<Entry> rented;

public:
    MovieRentingSystem(int n, vector<vector<int>>& entries) {
        for (auto &e : entries) {
            int shop = e[0], movie = e[1], price = e[2];
            long long key = 1LL * shop * 100000 + movie;
            priceMap[key] = price;
            availableByMovie[movie].insert({price, shop, movie});
        }
    }

    vector<int> search(int movie) {
        vector<int> res;
        if (!availableByMovie.count(movie)) return res;
        auto &s = availableByMovie[movie];
        for (auto it = s.begin(); it != s.end() && res.size() < 5; ++it) {
            res.push_back(it->shop);
        }
        return res;
    }

    void rent(int shop, int movie) {
        long long key = 1LL * shop * 100000 + movie;
        int price = priceMap[key];
        Entry e = {price, shop, movie};
        availableByMovie[movie].erase(e);
        rented.insert(e);
    }

    void drop(int shop, int movie) {
        long long key = 1LL * shop * 100000 + movie;
        int price = priceMap[key];
        Entry e = {price, shop, movie};
        rented.erase(e);
        availableByMovie[movie].insert(e);
    }

    vector<vector<int>> report() {
        vector<vector<int>> res;
        for (auto it = rented.begin(); it != rented.end() && res.size() < 5; ++it) {
            res.push_back({it->shop, it->movie});
        }
        return res;
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