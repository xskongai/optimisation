#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/3/25
Description: simulated_annealing_vector
"""
import random

from exercises.genetic_algorithm import fitness


# objective function:Minimum
def f_real(vec):
    return sum(x ** 2 for x in vec)


def init(d=10, low=-5, high=5):
    return [random.uniform(low, high) for _ in range(d)]


def crossover_uniform_real(a, b):
    return [ai if random.random() > 0.5 else bi for ai, bi in zip(a, b)]


def mutate_gaussian(vec, sigma=0.1, p_mut=0.2):
    out = vec[:]
    for i in range(len(out)):
        if random.random() < p_mut:
            out[i] += random.gauss(0, sigma)
    return out


def select_tournament(pop, fitness, tournament_k=10):
    candidates = random.sample(list(zip(pop, fitness)), tournament_k)
    return min(candidates, key=lambda pair: pair[1])[0]


def ga_real(d=10, pop_size=80, generation=200, p_crossover=0.9, p_mut=0.2, sigma=0.1, elitism=2):
    pop = [init(d) for _ in range(pop_size)]
    fitness = [f_real(ind) for ind in pop]

    for _ in range(generation):
        elite = sorted(list(zip(pop, fitness)), key=lambda pair: pair[1])[:elitism]
        next_pop = [e[0][:] for e in elite]

        while len(next_pop) != pop_size:
            p1 = select_tournament(pop, fitness)
            p2 = select_tournament(pop, fitness)

            if random.random() < p_crossover:
                c1 = crossover_uniform_real(p1, p2)
                c2 = crossover_uniform_real(p1, p2)
            else:
                c1 = p1[:]
                c2 = p2[:]

            c1 = mutate_gaussian(c1, sigma, p_mut)
            c2 = mutate_gaussian(c2, sigma, p_mut)
            next_pop.extend([c1, c2])

        pop = next_pop[:pop_size]
        fitness = [f_real(ind) for ind in pop]

    best = min(list(zip(pop, fitness)), key=lambda pair: pair[1])
    return best[0], best[1]


def main():
    print("-------------------------test ga real vector----------------------------------")
    sol, val = ga_real()
    print("sol:", sol, "val", val)


if __name__ == "__main__":
    main()
