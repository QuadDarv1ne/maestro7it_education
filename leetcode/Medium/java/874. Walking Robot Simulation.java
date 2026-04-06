/**
 * https://leetcode.com/problems/walking-robot-simulation/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Walking Robot Simulation" на Java
 * 
 * Задача: Робот начинает в (0,0) и выполняет команды: 
 *        -2 – поворот налево, -1 – поворот направо, 1..9 – шаги вперёд.
 *        На поле есть препятствия. Нужно найти максимальное квадратичное расстояние
 *        от начала, которое робот достиг во время движения.
 * 
 * Алгоритм:
 * 1. Задаём направления: север (0,1), восток (1,0), юг (0,-1), запад (-1,0).
 * 2. Препятствия храним в HashSet с кодированием координат в long.
 * 3. Для каждой команды:
 *    - Если поворот, меняем направление.
 *    - Если шаги: пытаемся сделать каждый шаг, проверяя следующую клетку.
 *      Если клетка не препятствие – перемещаемся и обновляем максимальное расстояние.
 *      Иначе – прерываем шаги для этой команды.
 * 4. Возвращаем максимальное расстояние (x*x + y*y).
 * 
 * Сложность: O(commands + obstacles) времени и памяти.
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

import java.util.HashSet;
import java.util.Set;

class Solution {
    public int robotSim(int[] commands, int[][] obstacles) {
        // Направления: 0=север, 1=восток, 2=юг, 3=запад
        int[] dx = {0, 1, 0, -1};
        int[] dy = {1, 0, -1, 0};
        int dir = 0;
        
        // Храним препятствия в HashSet, кодируя координаты в long
        Set<Long> obsSet = new HashSet<>();
        for (int[] o : obstacles) {
            long key = ((long)o[0] << 32) | (o[1] & 0xffffffffL);
            obsSet.add(key);
        }
        
        int x = 0, y = 0;
        int maxDist = 0;
        
        for (int cmd : commands) {
            if (cmd == -1) {
                dir = (dir + 1) % 4;
            } else if (cmd == -2) {
                dir = (dir + 3) % 4;
            } else {
                for (int step = 0; step < cmd; step++) {
                    int nx = x + dx[dir];
                    int ny = y + dy[dir];
                    long nkey = ((long)nx << 32) | (ny & 0xffffffffL);
                    if (!obsSet.contains(nkey)) {
                        x = nx;
                        y = ny;
                        maxDist = Math.max(maxDist, x*x + y*y);
                    } else {
                        break;
                    }
                }
            }
        }
        return maxDist;
    }
}