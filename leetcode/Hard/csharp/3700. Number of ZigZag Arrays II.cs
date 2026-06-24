/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

/**
 * @brief Подсчёт количества зигзагообразных массивов.
 * 
 * Реализация на C# с использованием быстрого возведения матрицы в степень.
 * Используются двумерные массивы для лучшей локальности кэша.
 * 
 * @param n Длина массива
 * @param l Левая граница диапазона
 * @param r Правая граница диапазона
 * @return int Количество зигзагообразных массивов по модулю 10^9+7
 */
public class Solution {
    private const int MOD = 1000000007;
    
    public int ZigZagArrays(int n, int l, int r) {
        int m = r - l + 1;
        if (n == 1) return m;
        
        int size = 2 * m;
        long[,] M = new long[size, size];
        
        // Заполнение матрицы переходов
        for (int i = 0; i < m; i++) {
            for (int j = i + 1; j < m; j++) M[i, m + j] = 1;
            for (int j = 0; j < i; j++) M[m + i, j] = 1;
        }
        
        long[] V = new long[size];
        for (int i = 0; i < size; i++) V[i] = 1;
        
        int power = n - 1;
        while (power > 0) {
            if ((power & 1) == 1) {
                V = MatVecMul(M, V);
            }
            M = MatMul(M, M);
            power >>= 1;
        }
        
        long ans = 0;
        foreach (long x in V) ans = (ans + x) % MOD;
        return (int)ans;
    }
    
    private long[,] MatMul(long[,] A, long[,] B) {
        int n = A.GetLength(0);
        long[,] C = new long[n, n];
        for (int i = 0; i < n; i++) {
            for (int k = 0; k < n; k++) {
                if (A[i, k] != 0) {
                    for (int j = 0; j < n; j++) {
                        C[i, j] = (C[i, j] + A[i, k] * B[k, j]) % MOD;
                    }
                }
            }
        }
        return C;
    }
    
    private long[] MatVecMul(long[,] M, long[] V) {
        int n = M.GetLength(0);
        long[] res = new long[n];
        for (int i = 0; i < n; i++) {
            long sum = 0;
            for (int j = 0; j < n; j++) {
                sum = (sum + M[i, j] * V[j]) % MOD;
            }
            res[i] = sum;
        }
        return res;
    }
}