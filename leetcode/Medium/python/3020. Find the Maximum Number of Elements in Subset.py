from collections import Counter

class Solution(object):
    def maximumLength(self, nums):
        """
        Finds the maximum length of a subset that can be arranged into a chain
        where each element's square is also present (except possibly the last).
        Chain: a, a², a⁴, a⁸, ...
        
        Находит максимальную длину подмножества, которое можно упорядочить
        в цепочку, где квадрат каждого элемента (кроме последнего) также
        присутствует в подмножестве.
        Цепочка: a, a², a⁴, a⁸, ...
        
        Args:
            nums: List[int] - input array of integers
            
        Returns:
            int: maximum possible length of such subset
        """
        freq = Counter(nums)
        max_len = 0
        
        # Special case for 1: 1² = 1
        if 1 in freq:
            count = freq[1]
            # Use all ones if count is odd, otherwise all but one
            max_len = count if count % 2 == 1 else count - 1
        
        visited = set()
        
        for num in sorted(freq.keys()):
            if num == 1 or num in visited:
                continue
            
            # Skip if this number is a square of another number in freq
            root = int(num ** 0.5)
            if root * root == num and root in freq:
                continue
            
            # Build chain starting from this number
            current = num
            chain_len = 0
            
            while current in freq and current <= 10**9:
                visited.add(current)
                
                next_square = current * current
                
                if next_square in freq and next_square <= 10**9:
                    # Can continue chain - use all occurrences
                    chain_len += freq[current]
                    current = next_square
                else:
                    # End of chain - use just one element
                    chain_len += 1
                    break
            
            max_len = max(max_len, chain_len)
        
        return max_len