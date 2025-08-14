/**
 * https://leetcode.com/problems/soup-servings/description/?envType=daily-question&envId=2025-08-08
 */

/// <summary>
/// Вычисляет вероятность того, что суп A закончится раньше супа B
/// плюс половина вероятности, что они закончатся одновременно.
/// 
/// Условие:
/// - Изначально есть n мл супа A и n мл супа B.
/// - На каждом шаге выбирается одна из 4 операций с равной вероятностью (0.25):
///   1) A -= 100, B -= 0
///   2) A -= 75,  B -= 25
///   3) A -= 50,  B -= 50
///   4) A -= 25,  B -= 75
/// - Если требуемого объёма нет, подаётся оставшееся количество.
/// - Процесс останавливается, когда хотя бы один вид супа закончился.
/// 
/// Оптимизация:
/// - Порции кратны 25 мл, поэтому n можно уменьшить до m = ceil(n / 25).
/// - Для больших n (> 4800) вероятность ≈ 1, возвращаем 1.0.
/// 
/// Алгоритм:
/// - Рекурсия с мемоизацией (DFS) для всех возможных состояний (a, b).
/// - Случаи:
///   * a <= 0 && b <= 0 → вернуть 0.5
///   * a <= 0 → вернуть 1.0
///   * b <= 0 → вернуть 0.0
/// 
/// </summary>
/// <param name="n">Начальное количество миллилитров каждого вида супа (0 ≤ n ≤ 1e9)</param>
/// <returns>Вероятность с точностью до 1e-5</returns>
public class Solution
{
    private double[,] memo;
    public double SoupServings(int n)
    {
        if (n > 4800) return 1.0;
        int m = (n + 24) / 25;
        memo = new double[m + 1, m + 1];
        return Dfs(m, m);
    }
    private double Dfs(int a, int b)
    {
        if (a <= 0 && b <= 0) return 0.5;
        if (a <= 0) return 1.0;
        if (b <= 0) return 0.0;
        if (memo[a, b] > 0) return memo[a, b];
        double res = 0.25 * (Dfs(a - 4, b) + Dfs(a - 3, b - 1) + Dfs(a - 2, b - 2) + Dfs(a - 1, b - 3));
        memo[a, b] = res;
        return res;
    }
}

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