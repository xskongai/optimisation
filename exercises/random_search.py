# =============================================================================
# 🎲 Random Search Algorithm - 随机搜索算法思想说明
# =============================================================================
# 算法目标：
#   在搜索空间中随机采样多个候选解，通过评估目标函数值来寻找最优解或近似最优解。
#
# 核心思想（Core Idea）：
#   - 不依赖梯度信息或邻域结构（gradient-free, neighbor-free）
#   - 每次在整个搜索空间中随机生成一个新解（global sampling）
#   - 评估该解的目标函数值（evaluate objective function）
#   - 如果该解优于当前最优解，则更新最优解（greedy update）
#   - 重复此过程直到达到迭代次数或满足停止条件（termination condition）
#
# 特点（Features）：
#   ✅ 实现简单，适用于黑盒优化问题
#   ✅ 不易陷入局部最优，具有全局探索能力
#   ❌ 收敛速度慢，效率低
#   ❌ 无法保证找到全局最优解
#
# 适用场景：
#   - 超参数优化（如机器学习模型调参）
#   - 黑盒函数最大化/最小化
#   - 与局部搜索算法（如爬山、模拟退火）对比教学
#
# 示例函数：
#   f(x, y) = x^2 + y^2
#   最小值为 0，出现在 x = 0, y = 0
# =============================================================================

import random


def objective_function(x, y):
    return x ** 2 + y ** 2


def random_search(n_iter=10000, bounds=[(-10, 10), (-10, 10)]):
    best_x, best_y = None, None
    best_score = float('inf')

    for i in range(n_iter):

        x = random.uniform(bounds[0][0], bounds[0][1])
        y = random.uniform(bounds[1][0], bounds[1][1])
        score = objective_function(x, y)
        print(f"iteration{i}:the optimal solution is:x= {x:.4f},y = {y:.4f},score = {score:.4f}")

        if score < best_score:
            best_x, best_y = x, y
            best_score = score
            print(f"iteration{i}:the optimal solution is:x= {best_x:.4f},y = {best_y:.4f},score = {best_score:.4f}")
    return best_x, best_y, best_score


best_x, best_y, best_score = random_search()

