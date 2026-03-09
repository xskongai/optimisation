#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/4/25
Description: genetic_programming_symbolic_regression
"""
import random
import operator
import math
import numpy as np

import copy

# 定义函数集和终端集
FUNCTIONS = [
    (operator.add, 2, "+"),
    (operator.sub, 2, "-"),
    (operator.mul, 2, "*"),
    (lambda x, y: x / y if abs(y) > 1e-6 else 1, 2, "/"),
    (math.sin, 1, "sin"),
    (math.cos, 1, "cos")
]
TERMINALS = ["x", 1.0, 2.0]


class Node:
    def __init__(self, func=None, children=None, name=None):
        self.func = func
        self.children = children
        self.name = name

    def evaluate(self, x):
        # variable node
        if self.name == "x":
            return x
        # constant node
        elif isinstance(self.name, float):
            return self.name
        #  function node
        else:
            args = [child.evaluate(x) for child in self.children]
            return self.func(*args)

    def __str__(self):
        if self.func is None:
            return str(self.name)
        elif len(self.children) == 2:
            return f"{self.children[0]}{self.name}{self.children[1]}"
        else:
            return f"{self.name}({self.children[0]})"


def generate_tree(depth=3):
    if depth == 0 or (depth > 1 and random.random() < 0.3):
        term = random.choice(TERMINALS)
        return Node(name=term)

    func, arity, name = random.choice(FUNCTIONS)
    children = [generate_tree(depth - 1) for _ in range(arity)]
    return Node(func=func, children=children, name=name)


def fitness(individual, X, Y):
    preds = [individual.evaluate(x) for x in X]
    return np.mean((np.array(preds) - Y) ** 2)


def crossover(p1, p2):
    return random.choice([p1, p2])


def mutate(individual, depth=3):
    node = copy.deepcopy(individual)
    if depth == 0 or random.random() < 0.2:
        return generate_tree(depth)
    if node.children:
        idx = random.randrange(len(node.children))
        node.children[idx] = mutate(node.children[idx], depth - 1)
    return node


def select_tournament(pop, scores, tournament_k=10):
    candidates = random.sample(list(zip(pop, scores)), tournament_k)
    return min(candidates, key=lambda pair: pair[1])[0]


def genetic_programming(X, Y, generations=30, pop_size=50):
    pop = [generate_tree() for _ in range(pop_size)]
    scores = [fitness(ind, X, Y) for ind in pop]

    for gen in range(generations):
        elite = sorted(list(zip(pop, scores)), key=lambda pair: pair[1])[:2]

        next_pop = [copy.deepcopy(e[0]) for e in elite]

        while len(next_pop) != pop_size:
            p1 = select_tournament(pop, scores, 10)
            p2 = select_tournament(pop, scores, 10)

            c1 = crossover(p1, p2)
            c1 = mutate(c1)
            next_pop.append(c1)

        pop = next_pop[:]
        scores = [fitness(ind, X, Y) for ind in pop]

    best = min(list(zip(pop, scores)), key=lambda pair: pair[1])

    return best[0], best[1]


def main():
    X = np.linspace(-5, 5, 50)
    Y = X ** 2 + X + 1

    print("---------------------------genetic programming---------------------------------------")
    sol, val = genetic_programming(X, Y, generations=30, pop_size=50)
    print(f"best individual: sol:{sol},score:{val}")


if __name__ == "__main__":
    main()
