class Solution:
    def bestClosingTime(self, customers):
        """
        Находит оптимальный час закрытия магазина для минимизации штрафа.
        
        Args:
            customers: строка из 'Y' и 'N'
            
        Returns:
            Час закрытия с минимальным штрафом (наименьший при равенстве)
            
        Автор: Дуплей Максим Игоревич
        ORCID: https://orcid.org/0009-0007-7605-539X
        GitHub: https://github.com/QuadDarv1ne/
        """
        n = len(customers)
        
        # Считаем общее количество клиентов
        total_y = customers.count('Y')
        
        # Инициализируем
        current_penalty = total_y  # если закроем в час 0
        min_penalty = current_penalty
        best_hour = 0
        
        # Проходим по всем возможным часам закрытия
        for hour in range(1, n + 1):
            # Обновляем штраф для текущего часа закрытия
            if customers[hour - 1] == 'N':
                # Магазин был открыт в этот час без клиентов
                current_penalty += 1
            else:  # customers[hour - 1] == 'Y'
                # Больше не считаем этого клиента в закрытое время
                current_penalty -= 1
            
            # Проверяем, не нашли ли лучший час
            if current_penalty < min_penalty:
                min_penalty = current_penalty
                best_hour = hour
        
        return best_hour
    
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks