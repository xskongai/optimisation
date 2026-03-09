#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/3/25
Description: simulated_annealing_2d
"""
import random, math


def f(bits):
    return sum(bits)


def init(n=50):
    bits = [random.choice([0, 1]) for _ in range(n)]
    return bits


def nbr(bits, step=1):
    n = len(bits)
    for i in range(step):
        i = random.randrange(n)
        new_val = 1 - bits[i]
        bits[i] = new_val
    return bits


def accept(delta, T):
    if delta < 0:
        return True
    return random.random() < math.exp(-delta / T)


def cool(T, alpha=0.95):
    return T * alpha


def simulated_annealing(T0=100, n_iter=100, L=50):
    x = init(n=50)
    best_x = x
    best_val = f(x)

    T = T0
    for i in range(n_iter):
        for _ in range(L):
            x_new = nbr(x, step=1)
            delta = f(x_new) - f(x)

            if accept(delta, T):
                x = x_new
                if f(x_new) < best_val:
                    best_x, best_val = x_new, f(x_new)
        T = cool(T, alpha=0.95)

    return best_x, best_val


def main():
    print("-----------------test sa bits----------------------------")
    print("sa():", simulated_annealing())
    pass


if __name__ == "__main__":
    main()
