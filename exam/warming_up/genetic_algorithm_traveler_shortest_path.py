#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/3/25
Description: genetic_algorithm_traveler_shortest_path
"""

import random


def make_dist(n=20, seed=0):
    random.seed(seed)

    coords = [(random.random(), random.random()) for _ in range(n)]

    def dist(i, j):
        (xi, yi), (xj, yj) = coords[i], coords[j]
        return ((xi - xj) ** 2 + (yi - yj) ** 2) ** 0.5

    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            D[i][j] = D[j][i] = dist(i, j)
    return D


def init_perm(n):
    tour = list(range(n))
    random.shuffle(tour)
    return tour


def tour_length(tour, D):
    return sum([D[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour))])


def crossover_OX(p1, p2):
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[a: b + 1] = p1[a: b + 1]
    fill = [x for x in p1 if x not in child]
    j = 0
    for i in range(n):
        if child[i] is None:
            child[i] = fill[j]
            j += 1
    return child


def mutate_swap(tour, p_mut=0.2):
    out = tour[:]
    if random.random() < p_mut:
        i, j = random.sample(range(len(out), ), 2)
        out[i], out[j] = out[j], out[i]
    return out


def select_tournament(pop, fitness, tournament_k):
    candidates = random.sample(list(zip(pop, fitness)), tournament_k)
    return min(candidates, key=lambda pair: pair[1])[0]


def ga_traveler_shortest_path(n=30, pop_size=80, generations=200, p_crossover=0.9, p_mut=0.2, tournament_k=10,
                              elitism=2):
    D = make_dist(n, seed=42)
    pop = [init_perm(n) for _ in range(pop_size)]
    fitness = [tour_length(ind, D) for ind in pop]

    for _ in range(generations):
        elite = sorted(list(zip(pop, fitness)), key=lambda pair: pair[1])[:elitism]
        next_pop = [e[0][:] for e in elite]

        while len(next_pop) != pop_size:

            p1 = select_tournament(pop, fitness, tournament_k)
            p2 = select_tournament(pop, fitness, tournament_k)

            if random.random() < p_crossover:
                c1, c2 = crossover_OX(p1, p2), crossover_OX(p1, p2)
            else:
                c1, c2 = p1[:], p2[:]

            c1 = mutate_swap(c1, p_mut)
            c2 = mutate_swap(c2, p_mut)

            next_pop.extend([c1, c2])

        pop = next_pop[:pop_size]
        fitness = [tour_length(idx, D) for idx in pop]

    best = min(list(zip(pop, fitness)), key=lambda pair: pair[1])
    return best[0], best[1]


def main():
    print("-----------------------------ga_traveler_shortest_path-------------------------------------")
    sol, val = ga_traveler_shortest_path()
    print("sol:", sol, "val:", val)


if __name__ == "__main__":
    main()
