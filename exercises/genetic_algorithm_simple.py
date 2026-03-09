import random  # 导入随机模块 | Import random module

# 🧩 参数设置 | Parameter Setup
POP_SIZE = 6           # 种群大小 | Population size
GENES = list(range(-10, 11))  # 基因范围 [-10, 10] | Gene range
GENERATIONS = 5        # 迭代次数 | Number of generations
MUTATION_RATE = 0.3    # 变异概率 | Mutation probability
ELITE_COUNT = 1        # 精英保留个体数 | Number of elite individuals to keep

# 🎯 适应度函数 | Fitness Function
# 我们希望最小化 f(x) = x^2，所以适应度定义为 -x^2（越大越好）
def fitness(x):
    return -x**2

# 🧬 初始化种群 | Initialize Population
def create_population():
    return [random.choice(GENES) for _ in range(POP_SIZE)]

# 🎯 选择操作：轮盘赌选择（适应度平移为正）| Selection: Roulette Wheel with Shifted Fitness
def selection(population):
    scores = [fitness(ind) for ind in population]
    min_score = min(scores)
    adjusted_scores = [s - min_score + 1 for s in scores]  # 所有值变为正数 | Shift to positive
    total = sum(adjusted_scores)
    probs = [s / total for s in adjusted_scores]
    return random.choices(population, weights=probs, k=POP_SIZE - ELITE_COUNT)

# 🔀 交叉操作：整数平均 | Crossover: Integer Averaging
def crossover(p1, p2):
    return (p1 + p2) // 2

# 🧪 变异操作：更强变异 | Mutation: Stronger Mutation
def mutate(ind):
    if random.random() < MUTATION_RATE:
        return max(-10, min(10, ind + random.randint(-5, 5)))  # 限制范围 | Clamp to [-10, 10]
    return ind

# 🧠 主遗传算法流程 | Main Genetic Algorithm Loop
def genetic_algorithm():
    population = create_population()
    print(f"初始种群: {population}")

    for gen in range(GENERATIONS):
        # 精英保留 | Keep best individuals
        sorted_pop = sorted(population, key=lambda x: x**2)
        elites = sorted_pop[:ELITE_COUNT]

        # 选择父代并生成子代 | Select parents and generate children
        selected = selection(population)
        children = []
        for i in range(0, len(selected), 2):
            p1 = selected[i]
            p2 = selected[(i+1) % len(selected)]
            child1 = mutate(crossover(p1, p2))
            child2 = mutate(crossover(p2, p1))
            children.extend([child1, child2])

        # 更新种群 | Update population
        population = elites + children[:POP_SIZE - ELITE_COUNT]
        best = min(population, key=lambda x: x**2)
        print(f"第 {gen+1} 代种群: {population} | 最优解: x = {best}, f(x) = {best**2}")

    return best

# 🚀 运行算法 | Run the algorithm
best_solution = genetic_algorithm()
print(f"\n最终最优解: x = {best_solution}, f(x) = {best_solution**2}")
