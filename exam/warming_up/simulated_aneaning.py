#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/3/25
Description: simulated_aneaning
"""
import random, math


def f(x):
    return (x - 3) ** 2


def init():
    return random.uniform(-10, 10)


def nbr(x, step=0.5):
    return x + random.uniform(-step, step)


def accept(delta, T):
    if delta < 0:
        return True
    return random.random() < math.exp(-delta / T)


def cool(T, alpha=0.95):
    return T * 0.95


def sa(T0=10, n_iter=200, alpha=0.95, L=50):
    x = init()
    best_x = x
    best_y = f(x)

    for i in range(n_iter):
        for _ in range(L):
            x_new = nbr(x)

            delta = f(x_new) - f(x)
            if accept(delta, T0):
                x = x_new
                if f(x_new) < best_y:
                    best_x, best_y = x_new, f(x_new)
        T0 = cool(T0, alpha)
    return best_x, best_y


def main():
    print("-----------------------test sa-------------------------------")
    print(sa())


if __name__ == "__main__":
    main()
