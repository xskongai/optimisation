#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/10/25
Description: 02_hill_climbing_bits
"""
import random


# minimum
def f(bits):
    return sum(bits)


def init(n=30):
    return [random.choice([0, 1]) for _ in range(n)]


def nbr(bits, flip=1):
    new_bits = bits[:]
    n = len(bits)
    for _ in range(flip):
        idx = random.randrange(0, n)
        new_bits[idx] = 1 - bits[idx]

    return new_bits


def hill_climbing_discrete_value(iteration=100):
    best_sol = init(n=20)
    best_val = f(best_sol)
    for _ in range(iteration):
        neighbor = nbr(best_sol, flip=2)

        if f(neighbor) < best_val:
            best_sol = neighbor
            best_val = f(neighbor)

    return best_sol, best_val


def main():
    print("-----------------------------hill climbing: test discrete value,bits---------------------------")
    best_sol, best_val = hill_climbing_discrete_value()
    print(f"best_sol:{best_sol}, best_val:{best_val}")


if __name__ == "__main__":
    main()
