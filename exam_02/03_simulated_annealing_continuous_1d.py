#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/10/25
Description: 03_simulated_annealing
"""
import random
import math


# minimize
def f(x):
    return (x - 3) ** 2


def init(lower, higher):
    return random.uniform(lower, higher)


def nbr(x, step=0.5):
    return x + random.uniform(-step, step)


def accept(delta, T):
    if delta < 0:
        return True
    return random.random() < math.exp(-delta / T)


def cool(T, alpha):
    return T * alpha


def simulated_annealing_continuous_1d(max_iteration=100, T0=10.0, alpha=0.95, L=50):
    x = init(-10, 10)
    best_x = x
    best_val = f(best_x)

    T = T0
    for _ in range(max_iteration):
        for _ in range(L):
            x_new = nbr(x)
            delta = f(x_new) - f(x)

            if accept(delta, T):
                x = x_new
                if f(x_new) < best_val:
                    best_x = x_new
                    best_val = f(x_new)
        T = cool(T, alpha)
    return best_x, best_val


def main():
    print("--test simulated annealing continuous 1 dimension value--")
    best_x, best_val = simulated_annealing_continuous_1d()
    print(f"best_x:{best_x}, best_val:{best_val}")


if __name__ == "__main__":
    main()
