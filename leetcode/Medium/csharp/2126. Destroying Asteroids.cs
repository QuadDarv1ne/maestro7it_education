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

using System;

public class Solution {
    /// <summary>
    /// Определяет, сможет ли планета уничтожить все астероиды.
    /// 
    /// Планета может уничтожить астероид, если её текущая масса больше или равна
    /// массе астероида. После уничтожения масса планеты увеличивается на массу
    /// астероида. Астероиды можно уничтожать в любом порядке.
    /// </summary>
    /// <param name="mass">Начальная масса планеты</param>
    /// <param name="asteroids">Массив масс астероидов</param>
    /// <returns>True, если все астероиды могут быть уничтожены, иначе False</returns>
    /// 
    /// <example>
    /// AsteroidsDestroyed(10, [3, 9, 19, 5, 21]) -> True
    /// AsteroidsDestroyed(5, [4, 9, 23, 4]) -> False
    /// </example>
    /// 
    /// <remarks>
    /// Алгоритм:
    ///   1. Сортируем астероиды по возрастанию массы
    ///   2. Жадно уничтожаем самые маленькие доступные
    ///   3. Если текущая масса меньше массы астероида — невозможно уничтожить все
    /// 
    /// Сложность:
    ///   Время: O(n log n) — сортировка массива
    ///   Память: O(1)
    /// </remarks>
    public bool AsteroidsDestroyed(int mass, int[] asteroids) {
        Array.Sort(asteroids);
        long currentMass = mass;  // long для избежания переполнения
        
        foreach (int asteroid in asteroids) {
            if (currentMass >= asteroid) {
                currentMass += asteroid;
            } else {
                return false;
            }
        }
        
        return true;
    }
}