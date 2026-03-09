#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 10/31/25
Description: grch_demo
"""
import numpy as np
import random


# 初始化空路径
# Initialize an empty path
def init(instance):
    return []

# 判断是否访问了所有颜色
# Check if all colors have been visited
def complete(sol, instance):
    return len(sol) == len(instance)

# 返回未访问的颜色
# Return list of unvisited colors
def allowed_parts(sol, instance):
    return [c for c in instance if c not in sol]

# 计算添加某颜色后的清洗成本
# Compute cleaning cost of adding a color to current path
def cost(sol, part, instance):
    if not sol:
        return 0  # 起点无成本
    last = sol[-1]
    return cleaning_time[last][part]

# 将颜色加入路径
# Add selected color to current path
def add_part(sol, part, instance):
    return sol + [part]


# 通用 GRCH 构造式启发式框架
# Generalised Restricted Candidate Heuristic (GRCH) framework
def GRCH(instance, init, complete, allowed_parts, cost, add_part, p):
    # 初始化一个空解
    # Initialize an empty solution
    sol = init(instance)

    # 当解未完成时，继续构造
    # While the solution is incomplete, keep building
    while not complete(sol, instance):
        # 获取当前允许添加的元素
        # Get the list of allowed parts to add next
        parts = allowed_parts(sol, instance)

        # 如果没有可选元素，说明已完成
        # If no parts left, we must be done
        if len(parts) == 0:
            break

        # 计算每个候选元素的成本
        # Compute cost of adding each candidate part
        costs = [cost(sol, part, instance) for part in parts]

        # 根据百分位数构造受限候选列表（RCL）
        # Build Restricted Candidate List (RCL) based on cost percentile
        RCL_limit = np.percentile(costs, p * 100)
        RCL = [part for part, c in zip(parts, costs) if c <= RCL_limit]

        # 确保 RCL 非空
        # Ensure RCL is not empty
        assert len(RCL)

        # 从 RCL 中随机选择一个元素加入解中
        # Randomly select one part from RCL and add to solution
        sol = add_part(sol, random.choice(RCL), instance)

    # 返回最终构造的解
    # Return the final constructed solution
    return sol



# 定义颜色之间的清洗时间（非对称）
# Define asymmetric cleaning time between colors
cleaning_time = {
    'Black': {'Yellow': 12, 'Red': 8, 'White': 10, 'Blue': 15},
    'Yellow': {'Black': 6, 'Red': 7, 'White': 9, 'Blue': 11},
    'Red': {'Black': 5, 'Yellow': 11, 'White': 6, 'Blue': 10},
    'White': {'Black': 7, 'Yellow': 10, 'Red': 9, 'Blue': 8},
    'Blue': {'Black': 9, 'Yellow': 13, 'Red': 6, 'White': 7}
}

# 所有颜色列表
# List of all colors
colors = ['Black', 'Yellow', 'Red', 'White', 'Blue']


if __name__ == "__main__":
    instance = colors
    p = 0.3  # 只考虑成本最低的 30% 候选项
    best_path = GRCH(instance, init, complete, allowed_parts, cost, add_part, p)

    # 计算总清洗时间
    # Calculate total cleaning time for the final path
    total_cost = sum(
        cleaning_time[best_path[i]][best_path[i+1]]
        for i in range(len(best_path) - 1)
    )

    # 输出结果
    # Print the result
    print("颜色切换顺序（Color sequence）：", " → ".join(best_path))
    print("总清洗时间（Total cleaning time）：", total_cost, "分钟")

