# 1. 📦 CollectionBot 核心代码解析（中英双语）

---

## 🔧 模块导入（Imports）

```python
import numpy as np
import random
```

- `numpy` 用于处理网格地图和实例数据结构。  
- `random` 用于生成随机物品位置、价值和重量。

---

## 1.1. 🚀 simulate(genome, instance, ...) — 机器人程序模拟器

```python
def simulate(genome, instance, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST, MAX_PROGRAM_LENGTH=100):
```

- 输入为一个程序 `genome`（列表：燃料 + 指令序列）和地图实例。  
- 输出为一个字典，记录机器人每一步的状态变化、动作、燃料、价值等历史。

### 1.1.1. 🧬 genome 格式说明

```python
genome = [fuel_budget, 'E', 'E', 'H', ...]
```

- 第一个元素是初始燃料量。  
- 后续元素是指令：`N`, `S`, `E`, `W`, `H`。

### 1.1.2. 📜 返回结果字段说明

- `'total_value'`: 最终目标函数值（价值 − 燃料成本 − 坠毁惩罚）  
- `'crashed'`: 是否坠毁  
- `'positions'`: 每一步的坐标  
- `'fuel_history'`: 每一步剩余燃料  
- `'value_history'`: 每一步累计价值  
- `'weight_history'`: 每一步携带重量  
- `'map_history'`: 每一步地图状态（含机器人位置）  
- `'actions'`: 每一步执行的动作（含 BLOCKED/CRASH）

---

## 🧮 simulate 内部逻辑解析

### 🔹 初始设置

- 限制程序长度为 `MAX_PROGRAM_LENGTH`。  
- 限制燃料不超过 `MAX_FUEL`。  
- 初始化机器人位置为 `(0,0)`，起始燃料与空载。

### 🔹 指令执行循环

- 对每个指令执行以下逻辑：

#### ✅ 移动指令（N/S/E/W）

- 检查是否越界，越界则记录为 `BLOCKED`。  
- 计算当前负载下的燃料消耗（每步为 `weight / 100`）。  
- 若燃料不足则坠毁，记录为 `CRASH`。  
- 若移动成功，检查是否拾取物品，更新地图与负载。

#### 🏠 回家指令（H）

- 计算回家路径距离（曼哈顿距离）。  
- 计算回家所需燃料（`distance × weight / 100`）。  
- 若燃料不足则坠毁，记录为 `H_CRASH`。  
- 若成功回家，清空负载并加总价值。

### 🔚 程序结束自动回家

- 程序结束后自动尝试回家。  
- 若燃料不足则 `FINAL_H_CRASH`，否则成功并加总剩余价值。

---

## 1.2. 🎯 objective(genome, instance, ...) — 黑盒目标函数

```python
def objective(genome, instance, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST):
```

- 调用 `simulate()` 并返回最终目标值。  
- 用于黑盒优化算法的评价函数。

---

## 🗺 generate_instance(...) — 随机地图生成器

```python
def generate_instance(width, height, num_items, seed=None):
```

- 创建一个 `height × width` 的网格地图。  
- 随机放置 `num_items` 个物品（排除 HOME）。  
- 每个物品随机赋值（1–20）与重量（1–20g）。

---

## 1.3. 📊 print_instance_stats(instance) — 地图统计信息

- 打印地图尺寸、物品数量、总价值与总重量。  
- 显示平均价值与平均重量。

---

## 👁 view_instance(instance) — 地图可视化

- 打印地图网格：HOME、机器人位置、物品值。  
- 显示每个物品的坐标、价值、重量与性价比（V/W）。

---

## 1.4. 🎞 visualise_program_behaviour(...) — 程序行为可视化

```python
def visualise_program_behaviour(instance, program, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST):
```

- 执行程序并逐步打印地图状态、动作与当前价值。  
- 用于调试程序行为与验证路径逻辑。

---

## 🧠 教学提示（Teaching Notes）

- 所有优化算法必须通过 `objective()` 获取反馈，不能解析地图结构。  
- `simulate()` 是核心评估器，记录完整运行轨迹。  
- `generate_instance()` 可用于构造多样化测试场景。  
- `visualise_program_behaviour()` 是调试与教学的利器。