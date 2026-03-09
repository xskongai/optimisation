#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/11/25
Description: 03_simulated_annealing_discrete
"""
import random
import math


# minimize
def f(bits):
    return sum(bits)


def init(n=50):
    return [random.choice([0, 1]) for _ in range(n)]


def nbr(bits, flip):
    n = len(bits)
    new_bits = bits[:]
    for _ in range(flip):
        idx = random.randrange(n)
        new_bits[idx] = 1 - bits[idx]
    return new_bits


def accept(delta, T):
    if delta < 0:
        return True
    return random.random() < math.exp(-delta / T)


def cool(T, alpha):
    return T * alpha


def sa_discrete(iteraiton=100, L=50, T0=10, aplha=0.95):
    x = init(n=20)

    best_x = x
    best_val = f(x)
    T = T0
    for _ in range(iteraiton):
        for _ in range(L):
            new_x = nbr(x, flip=2)

            delta = f(new_x) - f(x)
            if accept(delta, T):
                x = new_x

                if f(new_x) < best_val:
                    best_x = new_x
                    best_val = f(new_x)
        T = cool(T, aplha)
    return best_x, best_val


def main():
    print("--test simulated annealing discrete,bits--")
    best_x, best_val = sa_discrete()
    print(f"best_x:{best_x},best_val: {best_val}")


if __name__ == "__main__":
    main()
