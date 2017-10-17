from functools import reduce
import math
from typing import List


def triangle(a):
    return a * (a + 1) // 2


def question_1(n: int=1000):
    n -= 1
    return 3*triangle(n//3) + 5*triangle(n//5) - 15*triangle(n//15)


def question_2(limit: int=4000000):
    a, b = 0, 1
    result = 0
    while a < limit:
        a, b = b, a+b
        a, b = b, a+b
        a, b = b, a+b
        result += a
    if a >= limit:
        return result - a
    else:
        return result


def question_3(n: int=600851475143, verbose: bool=False):
    original_n = n
    # handle the special case of 2 first.
    primes_found = [2]
    exponents = [0]
    while not n&1:
        n >>= 1
        exponents[0] += 1

    if n == 1:
        return 2

    prime_candidate = 3
    while prime_candidate <= n:
        sqrt = int(prime_candidate**0.5)
        composite = False
        for p in primes_found:
            if p > sqrt:
                break
            if prime_candidate%p == 0:
                composite = True
                break

        if not composite:
            primes_found.append(prime_candidate)
            exponents.append(0)
            while n%prime_candidate == 0:
                n /= prime_candidate
                exponents[-1] += 1

        prime_candidate += 2

    assert reduce(lambda a, b: a*b, map(lambda p, e: p**e, primes_found, exponents), 1) == original_n

    if verbose:
        print('Prime factors of {}:'.format(original_n))
        print('  ' + '\n  '.join('{}**{}'.format(p, e) for p, e in zip(primes_found, exponents) if e))

    return primes_found[-1]


def is_palindrome(n):
    if len(n) <= 1:
        return True
    if n[0] == n[-1]:
        return is_palindrome(n[1:-1])
    else:
        return False


def question_4():

    max = -1
    for i in range(999, 899, -1):
        for j in range(i, 899, -1):
            prod = i*j
            if is_palindrome(str(prod)) and prod > max:
                max = prod
    assert max != -1
    return max


def sieve(n):
    primes = [True]*(n-1)
    for i in range(n-1):
        if primes[i]:
            p = i + 2
            for j in range(p*p-2, n - 1, p):
                primes[j] = False
    return [i+2 for i, p in enumerate(primes) if p]


def question_5(n: int=20):
    # the product of the largest prime powers less than or equal to n
    result = 1

    for prime in sieve(n):
        result *= prime**int(math.log(n, prime))

    for i in range(1, n+1):
        assert result % i == 0, 'result: {}, i: {}, remainder: {}'.format(result, i, result%i)
    return result


def question_6(n: int=100):
    return (n*(n+1)//2)**2 - n*(n+1)*(2*n+1)//6


def fast_sieve(n):
    d = n//2 - 1
    primes = [1]*d
    limit = (int(n**0.5) - 3)//2 + 1
    for i in range(limit):
        if primes[i]:
            step = 2*i + 3
            start = (step*step - 3)//2
            for j in range(start, d, step):
                primes[j] = 0
    result = [2]
    result.extend(2*i+3 for i, p in enumerate(primes) if p)
    return result


def question_7(n: int=10001):

    upper_bound = int(n*math.log(n) + n*math.log(math.log(n)))

    result = fast_sieve(upper_bound)[n-1]

    assert result & 1
    for i in range(3, int(result**0.5)+1):
        assert result % i != 0

    return result


def question_8(digits: List[int] = None, n: int = 13):
    if digits is None:
        temp = ''.join([
            '73167176531330624919225119674426574742355349194934',
            '96983520312774506326239578318016984801869478851843',
            '85861560789112949495459501737958331952853208805511',
            '12540698747158523863050715693290963295227443043557',
            '66896648950445244523161731856403098711121722383113',
            '62229893423380308135336276614282806444486645238749',
            '30358907296290491560440772390713810515859307960866',
            '70172427121883998797908792274921901699720888093776',
            '65727333001053367881220235421809751254540594752243',
            '52584907711670556013604839586446706324415722155397',
            '53697817977846174064955149290862569321978468622482',
            '83972241375657056057490261407972968652414535100474',
            '82166370484403199890008895243450658541227588666881',
            '16427171479924442928230863465674813919123162824586',
            '17866458359124566529476545682848912883142607690042',
            '24219022671055626321111109370544217506941658960408',
            '07198403850962455444362981230987879927244284909188',
            '84580156166097919133875499200524063689912560717606',
            '05886116467109405077541002256983155200055935729725',
            '71636269561882670428252483600823257530420752963450'
        ])
        digits = [int(_) for _ in temp]

    max = -1
    for i in range(len(digits) - n):
        prod = reduce(lambda a, b: a*b, digits[i:i+n], 1)
        if prod > max:
            max = prod

    return max


def question_9(n: int=1000):

    for a in range(1, n):
        a2 = a**2
        for b in range(a+1, n):
            b2 = b**2
            c = int((a2 + b2)**0.5)
            sum = a+b+c
            if sum > n:
                break
            if c**2 == a2+b2 and sum == n:
                return a*b*c


def question_10(n: int=2000000):
    return sum(fast_sieve(n))

if __name__ == '__main__':
    print(question_1())
    print(question_2())
    print(question_3())
    print(question_4())
    print(question_5())
    print(question_6())
    print(question_7())
    print(question_8(n=4), question_8())
    print(question_9())
    print(question_10())
