#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 11/12/25
Description: linear_programming
"""

# pip install ortools
'''
- OR= Operations Research（运筹学）  运筹学是一门研究如何在有限资源下做出最优决策的学科，常用于物流、排程、分配、路径优化等领域。
- Tools = 工具表示这是一个工具集，提供多种算法和求解器，方便开发者在不同场景下应用。
因此，OR-Tools 就是“运筹学工具集”，直观地说明了它的定位和用途。

ortools这个库 主要功能有哪些
简要回答：  OR-Tools 是 Google 开发的一个开源运筹优化库，主要功能包括 线性规划、整数规划、约束规划、车辆路径问题、排程与分配、打包问题 等，支持多种编程语言接口（Python、C++、Java、C#），并内置了强大的求解器如 CP-SAT、GLOP 等。
🧩 OR-Tools 的主要功能模块
- 线性规划 (Linear Programming, LP)
  用于解决目标函数和约束条件均为线性表达式的问题，例如资源分配、生产计划。
- 整数规划 (Integer Programming, IP)
  在 LP 基础上增加整数约束，适合处理离散决策问题，如工厂调度、选址问题。
- 约束规划 (Constraint Programming, CP)
  使用 CP-SAT 求解器，解决复杂的组合优化问题，如排班、时间表、八皇后问题等。
- 车辆路径问题 (Vehicle Routing Problem, VRP)
  专门的模块用于优化配送路线，常见于物流、快递、运输行业。
- 分配问题 (Assignment Problem)
  例如任务分配、人员调度，帮助找到最优匹配方案。
- 打包问题 (Packing Problem)
  解决如何在有限空间或容量下合理放置物品的问题。
- 图算法 (Graph Algorithms)
  包含最短路径、最大流等经典图论算法。
  
  
⚙️ 支持的求解器
- 开源求解器
：Google GLOP（线性规划）、CP-SAT（约束规划）、SCIP、GLPK
- 商业求解器接口
：可调用 Gurobi、CPLEX 等
- 多语言支持
：Python、C++、Java、C#
📌 应用场景举例
- 物流配送
：优化卡车或快递员的路线，降低运输成本
- 生产制造
：排产、资源分配，提升效率
- 人力资源
：排班、任务分配，满足约束条件
- 科研与教育
：解决经典优化问题（如八皇后、背包问题）

 总结来说，OR-Tools 是一个面向组合优化的全能工具箱，涵盖了从线性规划到复杂约束问题的多种算法，既能解决学术问题，也能直接应用于工业场景。
'''
from ortools.linear_solver import pywraplp

def dairy_girls_demon():
    solver = pywraplp.Solver.CreateSolver("SCIP")

    if not solver:
        raise Exception("SCIP solver not available")


    # variables:
    #  lower bound 0,uppder bound :infinity,
    x1 = solver.NumVar(0,solver.infinity(),'x1')
    x2 = solver.NumVar(0,solver.infinity(),'x2')
    x3 = solver.NumVar(0,solver.infinity(),'x3')


    # constraints
    solver.Add(10*x1<=20)
    solver.Add(2*x1+4*x2+3*x3 <=24)

    # objective function:Maximize
    solver.Maximize(3*x1+5*x2+5.5*x3)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution Found:")
        print("Litres of Vanilla ice-cream(x1):",x1.solution_value())
        print("Litres of Vanilla ice-cream(x2):",x2.solution_value())
        print("Maximum profit:",solver.Objective().Value())
    else:
        print("No optimal solution found.")




def giapetto_problem_demo():

def main():
    dairy_girls_demon()


if __name__ == "__main__":
    main()
