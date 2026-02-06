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

func reverseBits(n int) int {
    // Конвертируем int в uint32 для работы с 32-битными беззнаковыми числами
    var num uint32 = uint32(n)
    var result uint32 = 0
    
    for i := 0; i < 32; i++ {
        // Сдвигаем результат влево для освобождения места под следующий бит
        result <<= 1
        
        // Получаем младший бит числа num
        bit := num & 1
        
        // Добавляем бит к результату
        result |= bit
        
        // Сдвигаем num вправо для обработки следующего бита
        num >>= 1
    }
    
    // Конвертируем обратно в int для возврата
    return int(result)
}