#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/4/25
Description: greedy_randomised_constructive_heuristic_grch
"""
import math
import random

import numpy as np
from scipy.signal import correlate


# Euclidean distance
def compute_distance_matrix(coords):
    n = len(coords)
    dist = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i, n):
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            dist[i, j] = math.hypot(dx, dy)
            dist[j, i] = dist[i, j]
    return dist


def start_selector(n, deterministic=False):
    return 0 if deterministic else random.randint(0, n - 1)


def candidate_generator(visited, n):
    return [c for c in range(n) if c not in visited]


def evaluation_function(current_city, candidates, dist_matrix):
    return [(c, dist_matrix[current_city][c]) for c in candidates]


def randomised_selector(evaluated_candidates, k=3):
    if not evaluated_candidates:
        return None
    sorted_cands = sorted(evaluated_candidates, key=lambda x: x[1])
    rcl = sorted_cands[:min(k, len(sorted_cands))]
    return random.choice(rcl)[0]


def termination_check(visited, n):
    return len(visited) == n


def grch_tsp(distance_matrix, k=3, deterministic_start=False):
    n = len(distance_matrix)
    tour = []
    current = start_selector(n, deterministic_start)
    tour.append(current)

    while not termination_check(tour, n):
        candidates = candidate_generator(tour, n)
        evaluated = evaluation_function(current, candidates, distance_matrix)
        next_city = randomised_selector(evaluated, k=3)
        if next_city is None and evaluated:
            next_city = min(evaluated, key=lambda x: x[1])[0]
        tour.append(next_city)
        current = next_city

    tour.append(tour[0])
    total_dist = sum(distance_matrix[tour[i]][tour[i + 1]] for i in range(n))
    return tour, total_dist


def main():
    random.seed(123)
    np.random.seed(123)

    coords = np.array([
        [10, 30],
        [20, 80],
        [25, 35],
        [60, 20],
        [55, 75],
        [85, 55],
        [40, 50],
        [15, 10]
    ], dtype=float)

    dist_matrix = compute_distance_matrix(coords)

    tour, length = grch_tsp(dist_matrix, k=3, deterministic_start=False)

    print("Constructed tour(with return):", tour)
    print("total distance:", round(length, 2))


if __name__ == "__main__":
    main()
