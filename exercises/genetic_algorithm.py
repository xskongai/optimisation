
# 遗传算法（Genetic Algorithm, GA）是一种模拟自然选择和遗传机制的优化算法，其核心思想是“优胜劣汰 + 基因重组 + 随机变异”。下面是它的基本思想步骤，适合教学和组内讲解：
#
# 🧬 遗传算法的核心思想步骤 | Core Steps of Genetic Algorithm
# 1️⃣ 初始化种群（Population Initialization）
# 随机生成一组候选解（个体），每个个体由一组基因表示。
#
# 这些个体构成初始种群。
#
# 🎓 示例：在搜索整数最小化
# 𝑓( 𝑥)=𝑥^2 时，种群可能是 [34, -12, 87, -45, 3]
#
# 2️⃣ 适应度评估（Fitness Evaluation）
# 使用目标函数评估每个个体的“适应度”，即它的优劣程度。
#
# 适应度越高，个体越可能被选中。
#
# 🎓 示例：适应度函数为
# −
# 𝑥
# 2
# ，越接近0越好。
#
# 3️⃣ 选择操作（Selection）
# 根据适应度选择部分个体作为“父代”。
#
# 常用方法：轮盘赌选择、锦标赛选择、排名选择等。
#
# 🎓 示例：适应度高的个体如 -12 和 3 被多次选中。
#
# 4️⃣ 交叉操作（Crossover）
# 将两个父代的基因组合，生成新个体（子代）。
#
# 模拟生物遗传中的基因重组。
#
# 🎓 示例：(-12 + 3) // 2 = -5，两个父代生成一个子代。
#
# 5️⃣ 变异操作（Mutation）
# 以一定概率对个体进行微小随机修改。
#
# 保持种群多样性，避免陷入局部最优。
#
# 🎓 示例：-5 → -2，子代基因发生微调。
#
# 6️⃣ 更新种群（Population Update）
# 用新一代个体替换旧种群，进入下一轮迭代。
#
# 可保留部分最优个体（精英策略）。
#
# 7️⃣ 终止条件（Termination）
# 达到最大迭代次数或适应度达到目标。
#
# 输出最优解。

import random

POP_SIZE = 20
GENES = list(range(-100, 101))
GENERATIONS = 1000
MUTATION_RATE = 0.1


def fitness(x):
    return -x ** 2


def create_population():
    return [random.choice(GENES) for _ in range(POP_SIZE)]


def selection(population):
    scores = [fitness(ind) for ind in population]
    total = sum(scores)
    probs = [score / total for score in scores]
    return random.choices(population, weights=probs, k=POP_SIZE)

def crossover(parent1, parent2):
    return (parent1+parent2)//2

def mutate(individual):
    if random.random() < MUTATION_RATE:
        return individual+random.randint(-5,5)
    return individual


def genetic_algorithm():
    population = create_population()
    for generation in range(GENERATIONS):
        selected = selection(population)
        children = []
        for i in range(0,POP_SIZE,2):
            p1,p2 = selected[i],selected[i+1]
            child1 = mutate(crossover(p1,p2))
            child2 = mutate(crossover(p2,p1))
            children.extend([child1,child2])
        population = children
        best = max(population,key=fitness)
        print(f"the {generation+1}th generation optimal: x={best},f(x) = {best**2}")
    return best


best_solution = genetic_algorithm()
print(f"the best solution is {best_solution}")

