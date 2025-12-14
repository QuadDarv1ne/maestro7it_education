/*
https://leetcode.com/problems/number-of-ways-to-divide-a-long-corridor/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

var numberOfWays = function(corridor) {
    const MOD = 1000000007;
    const seats = [];

    for (let i = 0; i < corridor.length; i++) {
        if (corridor[i] === 'S')
            seats.push(i);
    }

    if (seats.length < 2 || seats.length % 2 !== 0)
        return 0;

    let ways = 1;
    for (let i = 1; i < seats.length - 1; i += 2) {
        const gap = seats[i + 1] - seats[i];
        ways = (ways * gap) % MOD;
    }

    return ways;
};
