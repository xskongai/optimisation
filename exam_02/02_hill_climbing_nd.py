#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/10/25
Description: 02_hill_climbing_nd
"""
import random


# minimum
def f(vec):
    return sum(x * x for x in vec)


def init(d=5, lower=-10, higher=10):
    return [random.uniform(lower, higher) for _ in range(d)]


def nbr(vec, step=0.5):
    neighbor = vec[:]
    d = len(vec)
    idx = random.randrange(d)
    neighbor[idx] += random.uniform(-step, step)
    return neighbor


def hill_climbing_nd(iteration=1000, d=3):
    best_sol = init(d)
    best_val = f(best_sol)

    step = 0.5
    alpha = 0.99
    for _ in range(iteration):

        neighbor = nbr(best_sol)
        if f(neighbor) < best_val:
            best_sol = nbr(best_sol, step=step)
            best_val = f(best_sol)

            step *= alpha

    return best_sol, best_val


def main():
    print("--------------------test hill climbing n dimension-------------------------")
    best_sol, best_val = hill_climbing_nd()
    print(f" best_sol:{best_sol},best_val:{best_val} ")


if __name__ == "__main__":
    main()
