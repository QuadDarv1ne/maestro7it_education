/**
 * https://leetcode.com/problems/design-movie-rental-system/description/?envType=daily-question&envId=2025-09-21
 */

import java.util.*;

class MovieRentingSystem {
    private Map<String,Integer> priceMap;
    private Map<Integer, TreeSet<int[]>> available;
    private TreeSet<int[]> rented;

    public MovieRentingSystem(int n, int[][] entries) {
        priceMap = new HashMap<>();
        available = new HashMap<>();
        rented = new TreeSet<>((a,b)-> 
            a[0]!=b[0]?a[0]-b[0]:
            a[1]!=b[1]?a[1]-b[1]:
            a[2]-b[2]
        );

        for (int[] e: entries) {
            int s=e[0], m=e[1], p=e[2];
            priceMap.put(s+"#"+m, p);
            available.computeIfAbsent(m,k-> new TreeSet<>(
                (x,y)-> x[0]!=y[0]?x[0]-y[0]:x[1]-y[1]
            ));
            available.get(m).add(new int[]{p,s});
        }
    }

    public List<Integer> search(int movie) {
        List<Integer> res=new ArrayList<>();
        if (!available.containsKey(movie)) return res;
        int cnt=0;
        for (int[] arr: available.get(movie)) {
            res.add(arr[1]);
            if (++cnt==5) break;
        }
        return res;
    }

    public void rent(int shop, int movie) {
        int p = priceMap.get(shop+"#"+movie);
        available.get(movie).remove(new int[]{p,shop}); // tricky: need wrapper
        // В Java нельзя удалить по new int[]{}, поэтому лучше хранить Pair класс
        rented.add(new int[]{p,shop,movie});
    }

    public void drop(int shop, int movie) {
        int p = priceMap.get(shop+"#"+movie);
        rented.remove(new int[]{p,shop,movie});
        available.get(movie).add(new int[]{p,shop});
    }

    public List<List<Integer>> report() {
        List<List<Integer>> res=new ArrayList<>();
        int cnt=0;
        for (int[] arr: rented) {
            res.add(Arrays.asList(arr[1], arr[2]));
            if (++cnt==5) break;
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