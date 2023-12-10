import hashlib
from sys import byteorder
from math import ceil
from random import randint


def sha(n: int):
    return int.from_bytes(hashlib.sha3_256(n.to_bytes(ceil(n.bit_length() / 8), byteorder=byteorder)).digest(),
                          byteorder=byteorder)


def gcd(a, b):
    u = [a, 1, 0]
    v = [b, 0, 1]
    while v[0] != 0:
        q = u[0] // v[0]
        t = [u[0] % v[0], u[1] - q * v[1], u[2] - q * v[2]]
        u = v
        v = t
    return u


def gcd_light(a, b):
    if b == 0:
        return a
    return gcd_light(b, a % b)


def ferma(x):
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    for i in range(0, 100):
        a = randint(2, x - 2)
        if gcd_light(a, x) != 1:
            return False
        if pow(a, x - 1, x) != 1:
            return False
    return True


def generate_simple_number(left, right):
    result = randint(left, right)

    while not ferma(result):
        result = randint(left, right)

    return result


def inverse(n: int, p: int):
    inv = gcd(n, p)[1]
    if inv < 0:
        inv += p
    return inv


def generate_friend_simple_numper(p):
    result = generate_simple_number(2, p)

    while gcd_light(p, result) != 1:
        result = generate_simple_number(2, p)

    return result


def to_bin(x):
    s = ""
    while x != 0 and x != -1:
        s += str(x % 2)
        x //= 2
        print(x)

    return s


def mega_pow(x, n, y):
    bin_n = to_bin(n)
    result = 1
    list = []
    for i in range(0, len(bin_n)):
        if bin_n[i] == '1':
            result *= x
        x = (x * x) % y

    return result % y