# 🤖 simulate() 函数逐行双语解析

```python
def simulate(genome, instance, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST, MAX_PROGRAM_LENGTH=100):
```
定义模拟函数，用于执行机器人程序并记录全过程。  
Defines the simulation function to execute a robot program and record its full history.

---

## 📥 输入处理与限制

```python
fuel_budget = genome[0]
commands = genome[1:]
```
提取程序的燃料预算和指令序列。  
Extracts fuel budget and command sequence from the genome.

```python
if len(commands) > MAX_PROGRAM_LENGTH:
    commands = commands[:MAX_PROGRAM_LENGTH]
```
限制程序长度不超过最大允许值。  
Truncates command list to the maximum allowed program length.

```python
if fuel_budget > MAX_FUEL:
    fuel_budget = MAX_FUEL
```
限制燃料预算不超过最大燃料上限。  
Caps the fuel budget to the maximum allowed fuel.

---

## 🗺 地图与状态初始化

```python
N, M = instance.shape[:2]
current_instance = instance.copy()
```
获取地图尺寸并复制地图以避免修改原始数据。  
Gets map dimensions and creates a copy to avoid modifying the original instance.

```python
def make_map():
    m = current_instance.copy()
    m[x, y, 0] = -1  # mark the robot location
    return m
```
定义辅助函数，在地图上标记机器人当前位置。  
Defines helper to mark robot's current location on the map.

---

## 🤖 机器人初始状态

```python
x, y = 0, 0
fuel_remaining = fuel_budget
items_held = []
total_value = -fuel_budget * FUEL_COST_PER_UNIT
```
初始化位置为 HOME，设置剩余燃料、空载物品列表，并计算初始燃料成本。  
Initializes robot at HOME, sets remaining fuel, empty inventory, and fuel cost penalty.

---

## 📊 历史记录结构初始化

```python
history = {
    'total_value': 0,
    'crashed': False,
    'positions': [(x, y)],
    'fuel_history': [fuel_remaining],
    'value_history': [total_value],
    'weight_history': [ROBOT_WEIGHT],
    'map_history': [make_map()],
    'actions': []
}
```
创建字典记录每一步的状态、动作、地图快照等。  
Creates a dictionary to track robot's state, actions, and map snapshots at each step.

---

## 🧭 方向映射与坠毁处理

```python
directions = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
```
定义方向命令与坐标偏移的映射。  
Defines movement directions and their coordinate offsets.

```python
def crash():
    history['crashed'] = True
    history['total_value'] = total_value - ROBOT_COST
    return history
```
定义坠毁处理函数，更新状态并扣除坠毁惩罚。  
Defines crash handler to update status and apply penalty.

---

## 🔁 主循环：逐条执行命令

```python
for cmd in commands:
```
遍历每条指令，逐步执行。  
Iterates through each command in the program.

---

### 🏠 回家命令处理

```python
if cmd == 'H':
```
如果是回家命令，计算回家所需燃料。  
If command is 'H', calculate fuel needed to return home.

```python
distance_to_home = abs(x) + abs(y)
current_weight = ROBOT_WEIGHT + sum(weight for _, weight in items_held)
fuel_needed = distance_to_home * current_weight / 100
```
计算曼哈顿距离与当前负载，估算燃料消耗。  
Computes Manhattan distance and current weight to estimate fuel needed.

```python
if fuel_remaining < fuel_needed:
    history['actions'].append('H_CRASH')
    return crash()
```
若燃料不足则坠毁。  
Triggers crash if fuel is insufficient.

```python
fuel_remaining -= fuel_needed
x, y = 0, 0
total_value += sum(value for value, _ in items_held)
items_held = []
history['actions'].append('H')
```
成功回家：扣除燃料、清空负载、加总价值。  
Successful return: deduct fuel, deposit items, add value.

---

### 🚶 移动命令处理

```python
elif cmd in directions:
```
如果是方向命令，计算新位置。  
If movement command, compute new coordinates.

```python
dx, dy = directions[cmd]
new_x, new_y = x + dx, y + dy
```
根据方向偏移计算目标位置。  
Calculates target position based on direction.

```python
if not (0 <= new_x < N and 0 <= new_y < M):
    history['actions'].append(f'{cmd}_BLOCKED')
```
若越界则记录为 BLOCKED。  
Records blocked move if out of bounds.

```python
else:
    current_weight = ROBOT_WEIGHT + sum(weight for _, weight in items_held)
    fuel_needed = current_weight / 100
```
计算当前负载下的移动燃料消耗。  
Calculates fuel needed for one-step move.

```python
if fuel_remaining < fuel_needed:
    history['actions'].append(f'{cmd}_CRASH')
    return crash()
```
若燃料不足则坠毁。  
Triggers crash if fuel is insufficient.

```python
fuel_remaining -= fuel_needed
x, y = new_x, new_y
```
更新位置并扣除燃料。  
Updates position and deducts fuel.

```python
if current_instance[x, y, 0] > 0:
    item_value = current_instance[x, y, 0]
    item_weight = current_instance[x, y, 1]
    items_held.append((item_value, item_weight))
    current_instance[x, y, 0] = 0
    current_instance[x, y, 1] = 0
    history['actions'].append(f'{cmd}_PICKUP')
else:
    history['actions'].append(cmd)
```
若当前位置有物品则拾取并清除地图标记。  
Picks up item if present and clears it from the map.

---

### 🧾 每步更新历史记录

```python
history['positions'].append((x, y))
history['fuel_history'].append(fuel_remaining)
history['value_history'].append(total_value)
current_carried_weight = ROBOT_WEIGHT + sum(weight for _, weight in items_held)
history['weight_history'].append(current_carried_weight)
history['map_history'].append(make_map())
```
记录当前位置、燃料、价值、负载与地图快照。  
Updates history with current position, fuel, value, weight, and map snapshot.

---

## 🏁 程序结束自动回家

```python
distance_to_home = abs(x) + abs(y)
current_weight = ROBOT_WEIGHT + sum(weight for _, weight in items_held)
fuel_needed = distance_to_home * current_weight / 100
```
计算回家所需燃料。  
Computes fuel needed to return home at end.

```python
if fuel_remaining < fuel_needed:
    history['actions'].append('FINAL_H_CRASH')
    return crash()
```
若燃料不足则坠毁。  
Triggers crash if fuel is insufficient.

```python
fuel_remaining -= fuel_needed
total_value += sum(value for value, _ in items_held)
```
成功回家并加总剩余物品价值。  
Successful return and deposit remaining items.

```python
history['total_value'] = total_value
history['actions'].append('FINAL_H')
history['positions'].append((0, 0))
history['fuel_history'].append(fuel_remaining)
history['value_history'].append(total_value)
history['weight_history'].append(ROBOT_WEIGHT)
history['map_history'].append(make_map())
```
记录最终状态与地图快照。  
Records final state and map snapshot.

```python
return history
```
返回完整运行历史。  
Returns full execution history.
