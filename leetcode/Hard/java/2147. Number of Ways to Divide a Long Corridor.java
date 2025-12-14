/*
https://leetcode.com/problems/number-of-ways-to-divide-a-long-corridor/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
    public int numberOfWays(String corridor) {
        final long MOD = 1_000_000_007L;
        List<Integer> seats = new ArrayList<>();

        for (int i = 0; i < corridor.length(); i++) {
            if (corridor.charAt(i) == 'S')
                seats.add(i);
        }

        if (seats.size() < 2 || seats.size() % 2 != 0)
            return 0;

        long ways = 1;
        for (int i = 1; i < seats.size() - 1; i += 2) {
            long gap = seats.get(i + 1) - seats.get(i);
            ways = (ways * gap) % MOD;
        }

        return (int) ways;
    }
}
