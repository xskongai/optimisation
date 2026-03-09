"""
Simulated Annealing Algorithm — 模拟退火算法思想总结

核心思想：
- 模拟退火源于物理中的退火过程：高温下金属原子可自由移动，冷却后逐渐稳定。
- 在优化中，它允许在早期接受“更差的解”，以跳出局部最优，最终收敛到更优解。

算法流程：
1. 从一个初始解开始（例如随机生成的机器人程序）。
2. 每轮生成一个邻域解（小改动）。
3. 如果新解更好，则接受。
4. 如果新解更差，也可能接受，接受概率由公式控制：
   P = exp((new_score - current_score) / temperature)
5. 每轮温度逐渐降低（降温），接受差解的概率也随之降低。

优点：
- 能跳出局部最优，探索更广泛的搜索空间。
- 收敛过程可控，适合复杂问题如路径规划、组合优化。

在 CollectionBot 中的应用：
- genome 表示机器人程序，目标是最大化收集价值。
- 模拟退火帮助我们找到更优的指令序列，避免陷入“只捡最近物品”的局部策略。
"""

import random
import math

from assignments.assignments01.collectionbot import print_instance_stats, visualise_program_behaviour


def init(fuel=1000, length=10):
    commands = random.choices(['N', 'S', 'E', 'W', 'H'], k=length)
    return fuel + commands


def nbr(genome):
    new_genome = genome[:]
    idx = random.randint(1, len(genome) - 1)
    new_genome[idx] = random.choices(['N', 'S', 'E', 'W', 'H'])
    return new_genome


def simulated_annealing(objective, instance, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST, initial_temp=100.0,
                        cooling_rate=0.99, iteration=1000):
    current = init()
    current_score = objective(current, instance, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST)

    best = current
    best_score = current_score

    temp = initial_temp

    for i in range(iteration):
        neighbor = nbr(current)
        neighbor_score = objective(neighbor, instance, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST)

        differ = neighbor_score - current_score
        if differ > 0 or random.random() < math.exp(differ / temp):
            current = neighbor
            current_score = neighbor_score
            if current_score > best_score:
                best = current
                best_score = current_score
        temp *= cooling_rate

    return best, best_score


import random


def generate_instance(width=8, height=8, num_items=10, seed=None):
    if seed is not None:
        random.seed(seed)

    grid = [[None for _ in range(width)] for _ in range(height)]
    items = []

    for _ in range(num_items):
        x = random.randint(0, height - 1)
        y = random.randint(0, width - 1)
        value = random.randint(5, 20)
        weight = random.randint(5, 20)
        grid[x][y] = {'value': value, 'weight': weight}
        items.append((x, y, value, weight))

    return {
        'grid': grid,
        'items': items,
        'width': width,
        'height': height
    }


def objective(genome, instance, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST):
    result = simulate(genome, instance, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST)
    return result['score']


def simulate(genome, instance, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST):
    directions = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    x, y = 0, 0
    fuel_remaining = genome[0]
    items_held = []
    total_value = -fuel_remaining * FUEL_COST_PER_UNIT
    grid = instance['grid']
    width = instance['width']
    height = instance['height']

    for cmd in genome[1:]:
        if cmd == 'H':
            cell = grid[x][y]
            if cell and cell not in items_held:
                total_value += cell['value']
                fuel_remaining -= cell['weight'] / 100
                items_held.append(cell)
        elif cmd in directions:
            dx, dy = directions[cmd]
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < height and 0 <= new_y < width:
                move_cost = (ROBOT_WEIGHT + sum(item['weight'] for item in items_held)) / 100
                fuel_remaining -= move_cost
                x, y = new_x, new_y
            else:
                continue  # BLOCKED

    # 回家
    distance_to_home = abs(x) + abs(y)
    return_cost = (ROBOT_WEIGHT + sum(item['weight'] for item in items_held)) * distance_to_home / 100
    fuel_remaining -= return_cost

    if fuel_remaining < 0:
        total_value -= ROBOT_COST  # 坠毁惩罚

    return {'score': total_value}


MAX_FUEL = 1000
FUEL_COST_PER_UNIT = 0.01
ROBOT_WEIGHT = 100
ROBOT_COST = 5

instance = generate_instance(width=8, height=8, num_items=10, seed=42)

print_instance_stats(instance)

best_genome, best_score = simulated_annealing(
    objective=objective,
    instance=instance,
    MAX_FUEL=MAX_FUEL,
    FUEL_COST_PER_UNIT=FUEL_COST_PER_UNIT,
    ROBOT_WEIGHT=ROBOT_WEIGHT,
    ROBOT_COST=ROBOT_COST,
    initial_temp=100.0,
    cooling_rate=0.99,
    iteration=1000
)

print("\n best genome:", best_genome)
print("best score:", best_score)
print("\n program progress:")
visualise_program_behaviour(instance,best_genome,MAX_FUEL,FUEL_COST_PER_UNIT,ROBOT_WEIGHT,ROBOT_COST)
