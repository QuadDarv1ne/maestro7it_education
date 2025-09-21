/**
 * https://leetcode.com/problems/design-movie-rental-system/description/?envType=daily-question&envId=2025-09-21
 */

using System;
using System.Collections.Generic;

/// <summary>
/// Класс MovieRentingSystem — имитация системы аренды фильмов.
/// Особенности:
/// - Поддержка поиска доступных фильмов с сортировкой по цене и магазину.
/// - Аренда (Rent), возврат (Drop), отчёт о 5 самых дешёвых арендованных фильмах.
/// </summary>
public class MovieRentingSystem
{
    // priceMap: ключ = (shop, movie), значение = цена
    private Dictionary<(int shop, int movie), int> priceMap;

    // available: для каждого фильма хранит SortedSet (price, shop)
    private Dictionary<int, SortedSet<(int price, int shop)>> available;

    // rented: все арендованные фильмы, сортировка по цене, затем shop, затем movie
    private SortedSet<(int price, int shop, int movie)> rented;

    /// <summary>
    /// Конструктор системы
    /// </summary>
    /// <param name="n">Количество магазинов</param>
    /// <param name="entries">Список [shop, movie, price]</param>
    public MovieRentingSystem(int n, IList<IList<int>> entries)
    {
        priceMap = new Dictionary<(int, int), int>();
        available = new Dictionary<int, SortedSet<(int, int)>>();
        rented = new SortedSet<(int, int, int)>(
            Comparer<(int price, int shop, int movie)>.Create((a, b) =>
                a.price != b.price ? a.price - b.price :
                a.shop != b.shop ? a.shop - b.shop :
                a.movie - b.movie
            )
        );

        foreach (var e in entries)
        {
            int shop = e[0], movie = e[1], price = e[2];
            priceMap[(shop, movie)] = price;

            if (!available.ContainsKey(movie))
            {
                available[movie] = new SortedSet<(int, int)>(
                    Comparer<(int price, int shop)>.Create((x, y) =>
                        x.price != y.price ? x.price - y.price : x.shop - y.shop
                    )
                );
            }
            available[movie].Add((price, shop));
        }
    }

    /// <summary>
    /// Поиск до 5 магазинов, где доступен фильм, отсортированных по цене и id магазина
    /// </summary>
    /// <param name="movie">ID фильма</param>
    /// <returns>Список ID магазинов</returns>
    public IList<int> Search(int movie)
    {
        var res = new List<int>();
        if (!available.ContainsKey(movie)) return res;

        foreach (var (price, shop) in available[movie])
        {
            res.Add(shop);
            if (res.Count == 5) break;
        }
        return res;
    }

    /// <summary>
    /// Аренда фильма в конкретном магазине
    /// </summary>
    /// <param name="shop">ID магазина</param>
    /// <param name="movie">ID фильма</param>
    public void Rent(int shop, int movie)
    {
        int price = priceMap[(shop, movie)];
        available[movie].Remove((price, shop));
        rented.Add((price, shop, movie));
    }

    /// <summary>
    /// Возврат арендованного фильма
    /// </summary>
    /// <param name="shop">ID магазина</param>
    /// <param name="movie">ID фильма</param>
    public void Drop(int shop, int movie)
    {
        int price = priceMap[(shop, movie)];
        rented.Remove((price, shop, movie));
        available[movie].Add((price, shop));
    }

    /// <summary>
    /// Получение отчёта: до 5 самых дешёвых арендованных фильмов
    /// </summary>
    /// <returns>Список [shop, movie]</returns>
    public IList<IList<int>> Report()
    {
        var res = new List<IList<int>>();
        foreach (var (price, shop, movie) in rented)
        {
            res.Add(new List<int> { shop, movie });
            if (res.Count == 5) break;
        }
        return res;
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