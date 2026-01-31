class Solution(object):
    def longestSubsequence(self, nums):
        sorelanuxi = nums
        
        # dp[and_val] = {last_val: max_length}
        # Для каждого AND значения храним словарь последних значений
        dp = {}
        max_length = 0
        
        for current in sorelanuxi:
            updates = []
            
            # Начинаем новую подпоследовательность
            if current != 0:
                updates.append((current, current, 1))
                max_length = max(max_length, 1)
            
            # Расширяем существующие подпоследовательности
            for and_val, last_dict in dp.items():
                for last_val, length in last_dict.items():
                    if last_val < current:
                        new_and = and_val & current
                        if new_and != 0:
                            new_length = length + 1
                            updates.append((new_and, current, new_length))
                            max_length = max(max_length, new_length)
            
            # Применяем обновления
            for and_val, last_val, length in updates:
                if and_val not in dp:
                    dp[and_val] = {}
                if last_val not in dp[and_val] or dp[and_val][last_val] < length:
                    dp[and_val][last_val] = length
            
            # Очистка: для каждого and_val оставляем только полезные состояния
            # Удаляем (last_val, length) если существует (last_val2, length2) где last_val2 < last_val и length2 >= length
            for and_val in dp:
                items = sorted(dp[and_val].items())
                cleaned = {}
                max_len_so_far = 0
                for val, length in items:
                    if length > max_len_so_far:
                        cleaned[val] = length
                        max_len_so_far = length
                dp[and_val] = cleaned
        
        return max_length