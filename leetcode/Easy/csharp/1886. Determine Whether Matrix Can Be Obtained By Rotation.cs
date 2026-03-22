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

public class Solution {
    public bool FindRotation(int[][] mat, int[][] target) {
        int n = mat.Length;
        
        // Проверяем 4 возможных поворота
        for (int rot = 0; rot < 4; ++rot) {
            if (AreMatricesEqual(mat, target)) {
                return true;
            }
            // Поворачиваем матрицу на 90° по часовой стрелке
            Rotate90(mat);
        }
        
        return false;
    }
    
    private void Rotate90(int[][] matrix) {
        int n = matrix.Length;
        // Транспонируем матрицу
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                int temp = matrix[i][j];
                matrix[i][j] = matrix[j][i];
                matrix[j][i] = temp;
            }
        }
        // Отражаем каждую строку
        for (int i = 0; i < n; ++i) {
            Array.Reverse(matrix[i]);
        }
    }
    
    private bool AreMatricesEqual(int[][] mat, int[][] target) {
        int n = mat.Length;
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (mat[i][j] != target[i][j]) {
                    return false;
                }
            }
        }
        return true;
    }
}