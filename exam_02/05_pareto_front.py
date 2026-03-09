#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/11/25
Description: 05_pareto_front
"""

import matplotlib.pyplot as plt


def dominate(x, y):
    # x dominates y if x is no worse in all objectives and better in at least one
    return (x[0] <= y[0] and x[1] <= y[1]) and (x[0] < y[0] or x[1] < y[1])


def pareto_front_min(points):
    front = []
    for i, x in enumerate(points):
        dominated = False
        for j, y in enumerate(points):
            if i != j and dominate(y, x):  # y dominates x
                dominated = True
                break
        if not dominated:
            front.append(x)
    return front


def main():
    solutions = [
        (1700, 2200),
        (1600, 2300),
        (1750, 2100),
        (1650, 2250),
        (1550, 2350),
        (1700, 2500),
        (1600, 2400)
    ]
    front = pareto_front_min(solutions)
    points = solutions

    plt.scatter([p[0] for p in points], [p[1] for p in points],
                c='green', label="all solutions")
    plt.scatter([p[0] for p in front], [p[1] for p in front],
                c='red', label="Pareto front")

    plt.xlabel('Cost (min)')
    plt.ylabel('Emissions (min)')
    plt.legend()
    plt.title('Pareto front (2-objective minimisation)')
    plt.show()


if __name__ == "__main__":
    main()
