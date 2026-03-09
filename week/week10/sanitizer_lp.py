#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 11/14/25
Description: sanitizer_lp
"""

from ortools.linear_solver import pywraplp

def build_model():
    """
    构建消毒液线性规划模型：
    - 定义变量
    - 添加约束
    - 设置目标函数
    返回 solver, x1, x2, objective
    """
    solver = pywraplp.Solver('Sanitizer',
                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # 决策变量
    x1 = solver.NumVar(0, 18, 'x1')  # 产品1
    x2 = solver.NumVar(0, 30, 'x2')  # 产品2

    # 约束条件
    solver.Add(0.1*x1 + 0.1*x2 <= 2.2, name="原料约束")
    solver.Add(1.5*x1 + 2.5*x2 <= 45, name="劳动力约束")

    # 目标函数：最大化利润
    objective = solver.Objective()
    objective.SetCoefficient(x1, 15)
    objective.SetCoefficient(x2, 10)
    objective.SetMaximization()

    return solver, x1, x2, objective


def analyze_solution(solver, x1, x2, objective):
    """
    求解并输出结果，包括：
    - 最优解
    - 活动量与松弛量
    - 影子价格
    """
    result_status = solver.Solve()

    if result_status != pywraplp.Solver.OPTIMAL:
        print("未找到最优解，状态码:", result_status)
        return

    # 最优解
    print("✅ 最优解:")
    print(f"x1 = {x1.solution_value()}")
    print(f"x2 = {x2.solution_value()}")
    print(f"最大利润 = {objective.Value()}")

    # 活动量与松弛量
    print("\n📊 约束活动量与松弛量:")
    activities = solver.ComputeConstraintActivities()
    for i, c in enumerate(solver.constraints()):
        activity = activities[i]
        slack = c.ub() - activity
        print(f"{c.name()}: 活动量={activity}, 松弛量={slack}")

    # 影子价格
    print("\n💡 影子价格 (Shadow Prices):")
    for c in solver.constraints():
        print(f"{c.name()} 的影子价格 = {c.DualValue()}")


def main():
    solver, x1, x2, objective = build_model()
    analyze_solution(solver, x1, x2, objective)


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
