--- Возвращает список простых чисел до n (алгоритм "Решето Эратосфена").
-- @param n integer Верхняя граница поиска.
-- @return table Массив простых чисел.
-- @example
--   find_primes(20) --> {2, 3, 5, 7, 11, 13, 17, 19}
function find_primes(n)
    local sieve = {}
    local primes = {}
    for i = 2, n do
        if not sieve[i] then
            table.insert(primes, i)
            for j = i * i, n, i do
                sieve[j] = true
            end
        end
    end
    return primes
end