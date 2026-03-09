#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 10/31/25
Description: grch
"""

import random
import numpy as np

# ========== 通用 GRCH 框架 ==========
def GRCH(instance, init, complete, allowed_parts, cost, add_part, p=0.2):
    """Greedy Randomised Constructive Heuristic (general form)"""
    sol = init(instance)
    while not complete(sol, instance):
        parts = allowed_parts(sol, instance)
        if not parts:
            break
        costs = [cost(sol, part, instance) for part in parts]
        RCL_limit = np.percentile(costs, p * 100)
        RCL = [part for part, c in zip(parts, costs) if c <= RCL_limit]
        sol = add_part(sol, random.choice(RCL), instance)
    return sol


# ========== 背包问题特定函数定义 ==========
def knapsack_init(instance):
    return {"items": [], "total_weight": 0, "total_value": 0}

def knapsack_complete(sol, instance):
    return sol["total_weight"] >= instance["capacity"]

def knapsack_allowed_parts(sol, instance):
    allowed = []
    for item in instance["items"]:
        if item["id"] not in sol["items"] and sol["total_weight"] + item["weight"] <= instance["capacity"]:
            allowed.append(item)
    return allowed

def knapsack_cost(sol, item, instance):
    # 使用负值作为“代价”，使得高价值的 item 代价更小
    return -item["value"]

def knapsack_add_part(sol, item, instance):
    sol["items"].append(item["id"])
    sol["total_weight"] += item["weight"]
    sol["total_value"] += item["value"]
    return sol


# ========== 示例数据：背包问题 ==========
instance = {
    "capacity": 269,
    "items": [
        {"id": 1, "value": 55, "weight": 95},
        {"id": 2, "value": 10, "weight": 4},
        {"id": 3, "value": 47, "weight": 60},
        {"id": 4, "value": 5, "weight": 32},
        {"id": 5, "value": 4, "weight": 23},
        {"id": 6, "value": 50, "weight": 72},
        {"id": 7, "value": 8, "weight": 80},
        {"id": 8, "value": 61, "weight": 62},
        {"id": 9, "value": 85, "weight": 65},
        {"id": 10, "value": 87, "weight": 46},
    ]
}

# ========== 运行 GRCH 多次，比较结果 ==========
random.seed(42)
for run in range(5):
    sol = GRCH(instance,
               init=knapsack_init,
               complete=knapsack_complete,
               allowed_parts=knapsack_allowed_parts,
               cost=knapsack_cost,
               add_part=knapsack_add_part,
               p=0.3)   # RCL 参数 p=0.3 表示前30%最好候选
    print(f"Run {run+1}: items={sol['items']}, total value={sol['total_value']}, total weight={sol['total_weight']}")
