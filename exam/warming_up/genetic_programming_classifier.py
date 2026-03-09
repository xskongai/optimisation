#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/4/25
Description: genetic_programming_classifier
"""

import random
import operator
import numpy as np

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

FUNCTIONS = [
    (operator.and_, 2, "AND"),
    (operator.or_, 2, "OR"),
    (operator.not_, 1, "NOT"),
    (operator.gt, 2, ">"),
    (operator.lt, 2, "<")
]


class Node:
    def __init__(self, func=None, children=None, name=None):
        self.func = func
        self.children = children or []
        self.name = name

    def evaluate(self, inputs):
        if isinstance(self.name, int):
            # 特征索引
            return inputs[self.name]
        elif isinstance(self.name, float):
            # 常数
            return self.name
        elif self.func:
            args = [child.evaluate(inputs) for child in self.children]
            return self.func(*args)
        else:
            return self.name

    def __str__(self):
        if self.name is not None and not self.func:
            return str(self.name)
        else:
            return f"{self.name}({','.join(str(c) for c in self.children)})"


def generate_tree(depth=3, X):
    if depth == 0 or random.random() < 0.3:
        return Node(name=random.choice(list(range(X.shape[1]))))
    func, arity, name = random.choice(FUNCTIONS)
    children = [generate_tree(depth - 1, X) for _ in range(arity)]
    return Node(func=func, children=children, name=name)


def fitness(indiviudal, X, y):
    preds = [int(indiviudal.evaluate(x)) for x in X]
    return np.mean(np.array(preds) == y)


def genetic_programming(X, y, generations=20, pop_size=30):
    pop = [generate_tree(depth=3, X) for _ in range(pop_size)]
    for gen in range(generations):
        scores = [(fitness(ind, X, y), ind) for ind in pop]
        scores.sort(k=lambda x: -x[0])
        best_score, best_ind = scores[0]

        print(f"Gen{gen},Best accuracy:{best_score:.4f}")

        new_pop = [best_ind]
        while len(new_pop) < pop_size:
            p1, p2 = random.sample(pop[:10], 2)
            child = random.choice([p1, p2])
            new_pop.append(generate_tree(X) if random.random() < 0.2 else new_pop.append(child))

        pop = new_pop
    return best_ind


def main():
    X, y = make_classification(n_samples=200, n_features=5, n_classes=2, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    best = genetic_programming(X_train, y_train)
    print("Best classifier rule:", best)


if __name__ == "__main__":
    main()
