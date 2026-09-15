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
 * Использует быстрое возведение матрицы в степень с параллельным трекингом вектора.
 * Время: O(m^3 * log n), где m = r - l + 1
 * Память: O(m^2)
 * 
 * @param n Длина массива
 * @param l Левая граница диапазона
 * @param r Правая граница диапазона
 * @return int Количество зигзагообразных массивов по модулю 10^9+7
 */
class Solution {
    const int MOD = 1e9 + 7;
    
    // Умножение матрицы на матрицу
    vector<vector<long long>> matMul(const vector<vector<long long>>& A, const vector<vector<long long>>& B) {
        int n = A.size();
        vector<vector<long long>> C(n, vector<long long>(n, 0));
        for (int i = 0; i < n; i++) {
            for (int k = 0; k < n; k++) {
                if (A[i][k]) { // Оптимизация: пропуск нулей
                    for (int j = 0; j < n; j++) {
                        C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD;
                    }
                }
            }
        }
        return C;
    }

    // Умножение матрицы на вектор
    vector<long long> matVecMul(const vector<vector<long long>>& M, const vector<long long>& V) {
        int n = M.size();
        vector<long long> res(n, 0);
        for (int i = 0; i < n; i++) {
            long long sum = 0;
            for (int j = 0; j < n; j++) {
                sum = (sum + M[i][j] * V[j]) % MOD;
            }
            res[i] = sum;
        }
        return res;
    }

public:
    int zigZagArrays(int n, int l, int r) {
        int m = r - l + 1;
        if (n == 1) return m;
        
        int size = 2 * m;
        vector<vector<long long>> M(size, vector<long long>(size, 0));
        
        // Заполнение матрицы переходов
        for (int i = 0; i < m; i++) {
            for (int j = i + 1; j < m; j++) M[i][m + j] = 1; // up_i -> down_j
            for (int j = 0; j < i; j++) M[m + i][j] = 1;     // down_i -> up_j
        }
        
        vector<long long> V(size, 1); // Начальный вектор
        int power = n - 1;
        
        // Быстрое возведение в степень с трекингом вектора
        while (power > 0) {
            if (power % 2 == 1) {
                V = matVecMul(M, V);
            }
            M = matMul(M, M);
            power /= 2;
        }
        
        long long ans = 0;
        for (long long x : V) ans = (ans + x) % MOD;
        return ans;
    }
};