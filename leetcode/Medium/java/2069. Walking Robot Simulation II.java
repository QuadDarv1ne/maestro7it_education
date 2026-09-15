/**
 * https://leetcode.com/problems/walking-robot-simulation-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Walking Robot Simulation II" на Java
 * 
 * Алгоритм аналогичен C++ версии.
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

import java.util.ArrayList;
import java.util.List;

class Robot {
    private int perimeter;
    private long steps;
    private List<int[]> positions;
    private List<String> directions;
    
    public Robot(int width, int height) {
        perimeter = 2 * (width + height) - 4;
        steps = 0;
        positions = new ArrayList<>();
        directions = new ArrayList<>();
        
        // East
        for (int x = 0; x < width; x++) {
            positions.add(new int[]{x, 0});
            directions.add("East");
        }
        // North
        for (int y = 1; y < height; y++) {
            positions.add(new int[]{width - 1, y});
            directions.add("North");
        }
        // West
        for (int x = width - 2; x >= 0; x--) {
            positions.add(new int[]{x, height - 1});
            directions.add("West");
        }
        // South
        for (int y = height - 2; y > 0; y--) {
            positions.add(new int[]{0, y});
            directions.add("South");
        }
    }
    
    public void step(int num) {
        steps += num;
    }
    
    public int[] getPos() {
        if (perimeter == 0) return new int[]{0, 0};
        int idx = (int)(steps % perimeter);
        return positions.get(idx);
    }
    
    public String getDir() {
        if (perimeter == 0) return "East";
        int idx = (int)(steps % perimeter);
        if (steps > 0 && idx == 0) return "South";
        return directions.get(idx);
    }
}