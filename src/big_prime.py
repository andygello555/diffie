from fractions import Fraction
from math import floor
from random import randrange, getrandbits

# From: https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
import numpy


class BigPrime:
    """
    Generates and stores a big prime number
    """

    def __init__(self, length: int = 1024, prime_tests: int = 128, generate: bool = True):
        self.__prime_tests: int = prime_tests
        self.length: int = length
        self.prime: int = 1
        if generate:
            self.jumble()

    def __str__(self):
        return hex(self.prime)

    def __is_prime(self):
        """
        Test if self.prime is prime using a set number of tests (given in self.__prime_tests)
        """

        # Test if n is not even.
        # But care, 2 is prime !
        if self.prime == 2 or self.prime == 3:
            return True
        if self.prime <= 1 or self.prime % 2 == 0:
            return False
        # find r and s
        s = 0
        r = self.prime - 1
        while r & 1 == 0:
            s += 1
            r //= 2
        # do k tests
        for _ in range(self.__prime_tests):
            a = randrange(2, self.prime - 1)
            x = pow(a, r, self.prime)
            if x != 1 and x != self.prime - 1:
                j = 1
                while j < s and x != self.prime - 1:
                    x = pow(x, 2, self.prime)
                    if x == 1:
                        return False
                    j += 1
                if x != self.prime - 1:
                    return False
        return True

    def __generate_prime_candidate(self) -> int:
        """
        Generate an odd integer randomly
        :returns: an odd integer with length self.length
        """

        # generate random bits
        p = getrandbits(self.length)
        # apply a mask to set MSB and LSB to 1
        p |= (1 << self.length - 1) | 1
        return p

    def jumble(self):
        """
        Generates a new prime and stores it in self.prime
        """

        self.prime = 4
        # keep generating while the primality test fails
        while not self.__is_prime():
            self.prime = self.__generate_prime_candidate()

    def gen_prim_root(self):
        # vector < int > fact;
        # int phi = p - 1, n = phi;
        # for (int i=2; i * i <= n; ++i) {
        #     if (n % i == 0) {
        #         fact.push_back (i);
        #         while (n % i == 0) {
        #             n /= i;
        #         }
        #     }
        # }
        # if (n > 1)
        #     fact.push_back (n);
        #
        # for (int res=2; res <= p; ++res) {
        #     bool ok = true;
        #     for (size_t i=0; i < fact.size() & & ok; ++i)
        #         ok &= powmod(res, phi / fact[i], p) != 1;
        #     if (ok)  return res;
        # }
        # return -1;
        fact: list = []
        phi = self.prime - 1
        n: int = phi
        # n: Fraction = Fraction(phi, phi)

        i = 2
        while i * i <= n:
            if n % i == 0:
                fact.append(i)
                # while n.__mod__(i) == 0:
                #     n = n.__div__(i)
                while n % i == 0:
                    n /= i
            i += 1
        print(n)
        if n > 1:
            fact.append(n)

        for res in range(2, self.prime + 1):
            ok = True
            for i in range(len(fact)):
                # print('res', res, 'phi', phi, 'fact[i]', fact[i], 'p', self.prime, 'phi / fact[i]', phi // fact[i])
                ok &= pow(res, int(phi // fact[i]), self.prime) != 1
                if not ok:
                    break
            if ok:
                return res
        return -1


prime = BigPrime(length=1024)
print('Prime', prime.prime, prime.prime.bit_length())
prim_root = prime.gen_prim_root()
print('Primitive root', prim_root, prim_root.bit_length())
