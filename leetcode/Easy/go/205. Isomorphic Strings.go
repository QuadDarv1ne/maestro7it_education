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

func isIsomorphic(s string, t string) bool {
    if len(s) != len(t) {
        return false
    }
    
    sToT := make(map[byte]byte)
    tToS := make(map[byte]byte)
    
    for i := 0; i < len(s); i++ {
        sChar := s[i]
        tChar := t[i]
        
        // Проверяем s -> t
        if val, exists := sToT[sChar]; exists {
            if val != tChar {
                return false
            }
        } else {
            sToT[sChar] = tChar
        }
        
        // Проверяем t -> s
        if val, exists := tToS[tChar]; exists {
            if val != sChar {
                return false
            }
        } else {
            tToS[tChar] = sChar
        }
    }
    
    return true
}