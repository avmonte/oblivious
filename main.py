"""
Author: Gevorg Nersesian
CS215 Bonus assignment: Oblivious Transfer implementation
American University of Armenia, Fall 2023

---

Running instructions

The code contains specific components that will only work in a terminal run
(ability to clean the terminal screen after ALICE/BOB finish their input)

Make sure you have python 3.x installed and run the following command in the repo with this file

> python3 main.py

"""

from random import choice
from os import name, system

from tools import *

PRIME_GENERATION_RANGE = (2, 100)  # excluded 0 and 1


def key_setup():
    global N, e, d
    p = generate_random_prime(PRIME_GENERATION_RANGE[0], PRIME_GENERATION_RANGE[1])
    q = generate_random_prime(PRIME_GENERATION_RANGE[0], PRIME_GENERATION_RANGE[1])
    N = p*q
    phi_N = (p-1)*(q-1)

    e = generate_random_prime(2, phi_N)
    while gcd(e, phi_N) != 1:
        e = generate_random_prime(2, phi_N)

    d = mod_inverse(e, phi_N)
    return N, e, d


def encrypt(x):
    return pow(x, e, N)


def decrypt(x):
    return pow(x, d, N)


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def main():
    key_setup()
    separator = '/'

    m = tuple(int(i) for i in input(f"ALICE input messages separated with an '{separator}'\n\tYOUR INPUT | ").split(separator))
    c = tuple(encrypt(i) for i in m)

    clear()

    b = int(input(f"BOB input a number between 0 and {len(m)-1} inclusive\n\tYOUR INPUT | "))
    k = choice(range(1, N))  # it wasn't specified what are the bounds of k, so I assigned it to [1, N)
    v = (c[b] + pow(k, e)) % N

    clear()

    p = tuple(pow(v - i, d) for i in c)
    m_prime = tuple(m[i] + p[i] % N for i in range(len(m)))

    input("BOB press Enter to see the chosen message")
    m_star = m_prime[b] - k
    print(m_star)

    input("BOB press Enter to finish")
    clear()


main()
