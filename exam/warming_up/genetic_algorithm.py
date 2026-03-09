#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/3/25
Description: genetic_algorithm
"""

# objective function:Minimum
import random

from exercises.genetic_algorithm import fitness


def f(bits):
    return sum(bits)


def init(n=50):
    return [random.choice([0, 1]) for _ in range(n)]


def nbr_flip(bits, p_mut=0.01):
    out = bits[:]
    for i in range(len(bits)):
        if random.random() < p_mut:
            out[i] = 1 - out[i]
    return out


def crossover_1point(a, b):
    n = len(a)
    if n < 2:
        return a[:], b[:]
    cut = random.randrange(1, n)
    child1 = a[:cut] + b[cut:]
    child2 = b[:cut] + a[cut:]
    return child1, child2


def select_tournament(pop, fitness, k=10):
    # 从随机采样的k个个体 中先出适应度更优者（最小化）
    candidates = random.sample(list(zip(pop, fitness)), k)
    return min(candidates, key=lambda pair: pair[1])[0]


def ga_bits(n=50, pop_size=100, generations=200, p_crossover=0.9, p_mut=0.01, tournament_k=10, elitism=1):
    pop = [init(n) for _ in range(pop_size)]
    fitness = [f(bits) for bits in pop]

    for g in range(generations):
        elite_pairs = sorted(zip(pop, fitness), key=lambda pair: pair[1])[:elitism]
        next_pop = [pair[0][:] for pair in elite_pairs]

        while len(next_pop) < pop_size:
            parent1 = select_tournament(pop, fitness, k=tournament_k)
            parent2 = select_tournament(pop, fitness, k=tournament_k)

            if random.random() < p_crossover:
                child1, child2 = crossover_1point(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:]

            child1 = nbr_flip(child1, p_mut=p_mut)
            child2 = nbr_flip(child2, p_mut=p_mut)
            next_pop.extend([child1, child2])
        pop = next_pop[:pop_size]
        fitness = [f(bits) for bits in pop]

    best = min(list(zip(pop, fitness)), key=lambda pair: pair[1])

    return best[0], best[1]


def main():
    print("-----------------------------ga test: bits---------------------------------------")
    sol, val = ga_bits()
    print("sol:", sol, "val", val)


if __name__ == "__main__":
    main()
