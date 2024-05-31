def primes(n: int):
    """Return a list of the first n primes"""

    sieve = [True] * n

    res = []

    for p in range(2, n):
        if sieve[p]:
            res.append(p)
            for i in range(p * p, n, p):
                sieve[i] = False

    return res


xs = primes(100)
print(xs)
