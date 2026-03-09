#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/11/25
Description: 04_ga_real
"""
import random


def f_real(vec):
    return sum((x - 2) * (x - 2) for x in vec)


def init(d=10, lower=-5.0, higher=5.0):
    return [random.uniform(lower, higher) for _ in range(d)]


def crossover(a, b):
    return [ai if random.random() < 0.5 else bi for ai, bi in zip(a, b)]


def nbr(vec, sigma=0.1, p_mut=0.2):
    new_vec = vec[:]
    n = len(vec)

    for i in range(n):
        if random.random() < p_mut:
            new_vec[i] += random.gauss(0, sigma)

    return new_vec


def select_tournament(pop, fitness, tournament_k=5):
    candidates = random.sample(list(zip(pop, fitness)), k=tournament_k)
    return min(candidates, key=lambda pair: pair[1])[0]


def ga_real(pop_size=100, generation=200, tournament_k=5, p_crosssover=0.9, p_mutate=0.01, elitism=2):
    pop = [init(d=5) for _ in range(pop_size)]
    fitness = [f_real(vec) for vec in pop]

    for _ in range(generation):
        elite = sorted(list(zip(pop, fitness)), key=lambda pair: pair[1])[:elitism]
        next_pop = [vec for vec, fitness in elite]

        while len(next_pop) < pop_size:
            p1, p2 = select_tournament(pop, fitness, tournament_k), select_tournament(pop, fitness, tournament_k)
            c1 = crossover(p1, p2)
            c1 = nbr(c1)
            next_pop.append(c1)

        pop = next_pop
        fitness = [f_real(vec) for vec in pop]

    best = min(list(zip(pop, fitness)), key=lambda pair: pair[1])
    return best[0], best[1]


def main():
    print("--ga,real value --")
    best_sol, best_fitness = ga_real()
    print(f"best_sol:{best_sol}, best_fitness:{best_fitness}")


if __name__ == "__main__":
    main()
