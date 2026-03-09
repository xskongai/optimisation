#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/10/25
Description: 02_hill_climbing
"""
import random


# Minimum
def f(x):
    return (x - 3) ** 2 + 3


def init():
    return random.uniform(-10, 10)


def nbr(x, step):
    return [x - step, x + step]


def hill_climbing(iteration):
    best_x = init()
    best_y = f(best_x)

    for _ in range(iteration):
        neighbors = nbr(best_x, step=0.1)
        next_x = min(neighbors, key=f)

        if f(next_x) < best_y:
            best_x = next_x
            best_y = f(next_x)

        else:
            break
    return best_x, best_y


def main():
    print("----------------run hill climbing --------------------")
    print("best x,y:", hill_climbing(1000))


if __name__ == "__main__":
    main()
