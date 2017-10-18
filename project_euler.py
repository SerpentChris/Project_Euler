from functools import reduce
import math
from typing import List, Any
import getopt
import sys
import cProfile


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


def transpose(grid: List[List[Any]]):
    return [list(row) for row in zip(*grid)]


def question_11(grid: List[List[int]]=None, l: int=4) -> int:
    if grid is None:
        temp = '''\
            08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08
            49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00
            81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65
            52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91
            22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80
            24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50
            32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70
            67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21
            24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72
            21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95
            78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92
            16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57
            86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58
            19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40
            04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66
            88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69
            04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36
            20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16
            20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54
            01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48'''
        grid = []
        for row in temp.split('\n'):
            grid.append([int(n) for n in row.strip().split()])

    L = len(grid)

    def max_row(grid):
        max = -1
        range_l = list(range(l))
        range_Lml = list(range(L - l))
        for x in range(L):
            for y in range_Lml:
                prod = 1
                for k in range_l:
                    prod *= grid[x][y+k]
                if prod > max:
                    max = prod

        return max

    def max_col(grid):
        return max_row(transpose(grid))

    def max_left_diag(grid):
        max = -1
        range_l = list(range(l))
        range_Lml = list(range(L - l))
        for x in range_Lml:
            for y in range_Lml:
                prod = 1
                for k in range_l:
                    prod *= grid[x+k][y+k]
                if prod > max:
                    max = prod
        return max

    def max_right_diag(grid):
        return max_left_diag([list(reversed(row)) for row in grid])

    return max(max_row(grid),
               max_col(grid),
               max_left_diag(grid),
               max_right_diag(grid))


def divisor_count(n: int) -> int:
    sqrt = int(n**0.5)
    count = 0
    for i in range(1, sqrt + 1):
        if n % i == 0:
            count += 2
    return count


def question_12(n: int=500) -> int:
    i = 3
    while True:
        a = (i + (i & 1))//2
        b = i + (~i & 1)

        if divisor_count(a)*divisor_count(b) > n:
            return a*b

        i += 1


def question_13(nums: List[int]=None, digits: int=10) -> str:
    if nums is None:
        temp = '''\
        37107287533902102798797998220837590246510135740250
        46376937677490009712648124896970078050417018260538
        74324986199524741059474233309513058123726617309629
        91942213363574161572522430563301811072406154908250
        23067588207539346171171980310421047513778063246676
        89261670696623633820136378418383684178734361726757
        28112879812849979408065481931592621691275889832738
        44274228917432520321923589422876796487670272189318
        47451445736001306439091167216856844588711603153276
        70386486105843025439939619828917593665686757934951
        62176457141856560629502157223196586755079324193331
        64906352462741904929101432445813822663347944758178
        92575867718337217661963751590579239728245598838407
        58203565325359399008402633568948830189458628227828
        80181199384826282014278194139940567587151170094390
        35398664372827112653829987240784473053190104293586
        86515506006295864861532075273371959191420517255829
        71693888707715466499115593487603532921714970056938
        54370070576826684624621495650076471787294438377604
        53282654108756828443191190634694037855217779295145
        36123272525000296071075082563815656710885258350721
        45876576172410976447339110607218265236877223636045
        17423706905851860660448207621209813287860733969412
        81142660418086830619328460811191061556940512689692
        51934325451728388641918047049293215058642563049483
        62467221648435076201727918039944693004732956340691
        15732444386908125794514089057706229429197107928209
        55037687525678773091862540744969844508330393682126
        18336384825330154686196124348767681297534375946515
        80386287592878490201521685554828717201219257766954
        78182833757993103614740356856449095527097864797581
        16726320100436897842553539920931837441497806860984
        48403098129077791799088218795327364475675590848030
        87086987551392711854517078544161852424320693150332
        59959406895756536782107074926966537676326235447210
        69793950679652694742597709739166693763042633987085
        41052684708299085211399427365734116182760315001271
        65378607361501080857009149939512557028198746004375
        35829035317434717326932123578154982629742552737307
        94953759765105305946966067683156574377167401875275
        88902802571733229619176668713819931811048770190271
        25267680276078003013678680992525463401061632866526
        36270218540497705585629946580636237993140746255962
        24074486908231174977792365466257246923322810917141
        91430288197103288597806669760892938638285025333403
        34413065578016127815921815005561868836468420090470
        23053081172816430487623791969842487255036638784583
        11487696932154902810424020138335124462181441773470
        63783299490636259666498587618221225225512486764533
        67720186971698544312419572409913959008952310058822
        95548255300263520781532296796249481641953868218774
        76085327132285723110424803456124867697064507995236
        37774242535411291684276865538926205024910326572967
        23701913275725675285653248258265463092207058596522
        29798860272258331913126375147341994889534765745501
        18495701454879288984856827726077713721403798879715
        38298203783031473527721580348144513491373226651381
        34829543829199918180278916522431027392251122869539
        40957953066405232632538044100059654939159879593635
        29746152185502371307642255121183693803580388584903
        41698116222072977186158236678424689157993532961922
        62467957194401269043877107275048102390895523597457
        23189706772547915061505504953922979530901129967519
        86188088225875314529584099251203829009407770775672
        11306739708304724483816533873502340845647058077308
        82959174767140363198008187129011875491310547126581
        97623331044818386269515456334926366572897563400500
        42846280183517070527831839425882145521227251250327
        55121603546981200581762165212827652751691296897789
        32238195734329339946437501907836945765883352399886
        75506164965184775180738168837861091527357929701337
        62177842752192623401942399639168044983993173312731
        32924185707147349566916674687634660915035914677504
        99518671430235219628894890102423325116913619626622
        73267460800591547471830798392868535206946944540724
        76841822524674417161514036427982273348055556214818
        97142617910342598647204516893989422179826088076852
        87783646182799346313767754307809363333018982642090
        10848802521674670883215120185883543223812876952786
        71329612474782464538636993009049310363619763878039
        62184073572399794223406235393808339651327408011116
        66627891981488087797941876876144230030984490851411
        60661826293682836764744779239180335110989069790714
        85786944089552990653640447425576083659976645795096
        66024396409905389607120198219976047599490197230297
        64913982680032973156037120041377903785566085089252
        16730939319872750275468906903707539413042652315011
        94809377245048795150954100921645863754710598436791
        78639167021187492431995700641917969777599028300699
        15368713711936614952811305876380278410754449733078
        40789923115535562561142322423255033685442488917353
        44889911501440648020369068063960672322193204149535
        41503128880339536053299340368006977710650566631954
        81234880673210146739058568557934581403627822703280
        82616570773948327592232845941706525094512325230608
        22918802058777319719839450180888072429661980811197
        77158542502016545090413245809786882778948721859617
        72107838435069186155435662884062257473692284509516
        20849603980134001723930671666823555245252804609722
        53503534226472524250874054075591789781264330331690'''
        nums = [int(n.strip()) for n in temp.split('\n')]

    return str(sum(nums))[:digits]


def collatz_length(n, known_lengths):
    length = 0
    new_chain_member_starts = {}
    while n != 1:
        if n in known_lengths:
            break
        new_chain_member_starts[n] = length
        if n&1:
            n = 3*n + 1
        else:
            n >>= 1
        length += 1
    else:
        for k, v in new_chain_member_starts.items():
            known_lengths[k] = length - v
        return

    assert n != 1
    remaining_length = known_lengths[n]
    for k, v in new_chain_member_starts.items():
        known_lengths[k] = length - v + remaining_length


def question_14(n: int=1000000):
    known_lengths = {1: 0}
    max = -1
    max_i = None
    for i in range(2, n):
        if i in known_lengths:
            continue
        collatz_length(i, known_lengths)
        if known_lengths[i] > max:
            max = known_lengths[i]
            max_i = i

    return max_i


def choose(n, k):
    i = 1
    d = n - k
    if d < k:
        k, d = d, k

    k_fact = 1
    for i in range(1, k + 1):
        k_fact *= i

    d_fact = k_fact
    for i in range(k + 1, d + 1):
        d_fact *= i

    n_fact = d_fact
    for i in range(d + 1, n + 1):
        n_fact *= i

    return n_fact//k_fact//d_fact


def question_15(n: int = 20):
    return choose(2*n, n)


def question_16(n: int = 1000):
    return sum(int(c) for c in str(1 << n))


def main():
    opts, args = getopt.getopt(sys.argv[1:], 'q:p')

    opt, val = None, None
    funcs = []
    profile = False
    for opt, val in opts:
        if opt == '-q':
            try:
                val = int(val)
            except:
                print('Invalid value for option: -q %d' % val)
                sys.exit(2)

            func_name = 'question_%d' % int(val)
            if func_name not in globals():
                print('Solution not implemented')
                sys.exit(1)
            else:
                funcs.append(func_name)
        if opt == '-p':
            profile = True

    if len(funcs) == 0:
        i = 1
        name = 'question_%d'
        while (name % i) in globals():
            funcs.append(name % i)
            i += 1

    for name in funcs:
        if profile:
            print('Profiling %s:' % name)
            cProfile.run('print(%s())' % name)
        else:
            print(globals()[name]())

    sys.exit(0)

if __name__ == '__main__':
    main()
