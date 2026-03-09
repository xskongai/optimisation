#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/10/25
Description: 01_random_search
"""

import random


# maximum
def f(x):
    return -x * x


def init():
    random.seed(42)
    # return random.randrange(-10, 10)
    return  random.uniform(-10,10)


def random_search(iteration):
    best_x = init()
    best_y = f(best_x)
    for _ in range(iteration):
        current_x = init()
        current_y = f(current_x)

        if current_y > best_y:
            best_x = current_x
            best_y = current_y

    return best_x, best_y


def main():
    print("--------------------test random search ---------------------------")
    print("best x,value :", random_search(1000))


if __name__ == "__main__":
    main()
