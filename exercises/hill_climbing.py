# =============================================================================
# 🧗 Hill Climbing Algorithm - 爬山算法思想说明
# =============================================================================
# 算法目标：
#   在搜索空间中寻找目标函数的最大值（或最小值），通过局部改进逐步逼近最优解。
#
# 核心思想（Core Idea）：
#   - 从一个初始解出发（initial solution）
#   - 在其邻域中生成候选解（neighbors）
#   - 比较邻居的目标函数值（objective value）
#   - 如果找到更优邻居，则移动过去（greedy move）
#   - 重复此过程直到没有更优邻居（local optimum）
#
# 特点（Features）：
#   ✅ 简单易实现，适合教学演示
#   ✅ 局部搜索效率高
#   ❌ 容易陷入局部最优，无法跳出“山谷”
#   ❌ 对初始解敏感
#
# 适用场景：
#   - 连续或离散优化问题
#   - 黑盒函数最大化/最小化
#   - 与模拟退火、遗传算法等对比教学
#
# 示例函数：
#   f(x) = - (x - 3)^2 + 10
#   最大值为 10，出现在 x = 3
# =============================================================================

import random


def objective_function(x):
    return -(x - 3) ** 2 + 10  # 最大值 在 3 的位置


def init():
    return random.uniform(-10, 10)


def nbr(x, step_siz=0.1):
    return [x + step_siz, x - step_siz]


def hill_climbing(f, step_siz=0.01, max_iterations=100000):
    current_x = init()
    current_y = f(current_x)
    for i in range(max_iterations):
        neighbors = nbr(current_x, step_siz)
        next_x = max(neighbors, key=f)
        next_y = f(next_x)

        if next_y > current_y:
            current_x, current_y = next_x, current_y
            print(f"iteration {i}: x = {current_y:.4f},y= {current_y:.4f}")
        else:
            break
    return current_x, current_y


x, y = hill_climbing(objective_function)
print("x = ", x)
print("y = ", y)
