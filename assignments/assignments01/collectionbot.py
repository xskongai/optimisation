import numpy as np
import random


def simulate(genome, instance, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST, MAX_PROGRAM_LENGTH=100):
    """
    Simulate the robot program and return detailed history.
    
    Args:
        genome: [fuel_budget, cmd0, cmd1, ...]
        instance: numpy array of shape (height, width, 2)
        
    Returns:
        dict with keys:
        - 'total_value': final objective value
        - 'crashed': boolean, True if robot crashed
        - 'positions': list of (x, y) positions at each step
        - 'fuel_history': list of fuel remaining at each step
        - 'value_history': list of total value collected at each step
        - 'weight_history': list of total weight carried at each step
        - 'map_history': list of instance states at each step
        - 'actions': list of actual actions taken (failed moves recorded as 'BLOCKED')
    """
    fuel_budget = genome[0]
    commands = genome[1:]

    # added 10 Oct 2025: limit program length
    if len(commands) > MAX_PROGRAM_LENGTH:
        commands = commands[:MAX_PROGRAM_LENGTH]

    if fuel_budget > MAX_FUEL:
        fuel_budget = MAX_FUEL
    
    # Instance dimensions
    N, M = instance.shape[:2]
    current_instance = instance.copy()  # Work with a copy

    def make_map():
        m = current_instance.copy()
        m[x, y, 0] = -1 # mark the robot location
        return m
    
    # Robot state
    x, y = 0, 0
    fuel_remaining = fuel_budget
    items_held = []
    total_value = -fuel_budget * FUEL_COST_PER_UNIT
    
    # History tracking
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
    
    directions = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    
    def crash():
        history['crashed'] = True
        history['total_value'] = total_value - ROBOT_COST
        return history
    
    for cmd in commands:
        if cmd == 'H':
            # Go home command
            distance_to_home = abs(x) + abs(y)
            current_weight = ROBOT_WEIGHT + sum(weight for _, weight in items_held)
            fuel_needed = distance_to_home * current_weight / 100
            
            if fuel_remaining < fuel_needed:
                history['actions'].append('H_CRASH')
                return crash()
            
            # Successfully return home
            fuel_remaining -= fuel_needed
            x, y = 0, 0
            
            # Deposit items
            total_value += sum(value for value, _ in items_held)
            items_held = []
            
            history['actions'].append('H')
            
        elif cmd in directions:
            # Movement command
            dx, dy = directions[cmd]
            new_x, new_y = x + dx, y + dy
            
            # Check bounds
            if not (0 <= new_x < N and 0 <= new_y < M):
                # Blocked by boundary
                history['actions'].append(f'{cmd}_BLOCKED')
            else:
                current_weight = ROBOT_WEIGHT + sum(weight for _, weight in items_held)
                fuel_needed = current_weight / 100
                
                if fuel_remaining < fuel_needed:
                    history['actions'].append(f'{cmd}_CRASH')
                    return crash()
                
                # Move successfully
                fuel_remaining -= fuel_needed
                x, y = new_x, new_y
                
                # Check for item at new location
                if current_instance[x, y, 0] > 0:
                    item_value = current_instance[x, y, 0]
                    item_weight = current_instance[x, y, 1]
                    items_held.append((item_value, item_weight))
                    # Remove item from map
                    current_instance[x, y, 0] = 0
                    current_instance[x, y, 1] = 0
                    history['actions'].append(f'{cmd}_PICKUP')
                else:
                    history['actions'].append(cmd)
        
        # Update history after each command
        history['positions'].append((x, y))
        history['fuel_history'].append(fuel_remaining)
        history['value_history'].append(total_value)
        current_carried_weight = ROBOT_WEIGHT + sum(weight for _, weight in items_held)
        history['weight_history'].append(current_carried_weight)
        history['map_history'].append(make_map())
    
    # End of program - automatic return home
    distance_to_home = abs(x) + abs(y)
    current_weight = ROBOT_WEIGHT + sum(weight for _, weight in items_held)
    fuel_needed = distance_to_home * current_weight / 100
    
    if fuel_remaining < fuel_needed:
        history['actions'].append('FINAL_H_CRASH')
        return crash()
    
    # Successfully complete mission
    fuel_remaining -= fuel_needed
    total_value += sum(value for value, _ in items_held)
    
    # Final objective
    history['total_value'] = total_value
    
    # Add final state
    history['actions'].append('FINAL_H')
    history['positions'].append((0, 0))
    history['fuel_history'].append(fuel_remaining)
    history['value_history'].append(total_value)
    history['weight_history'].append(ROBOT_WEIGHT)
    history['map_history'].append(make_map())
    
    return history

def objective(genome, instance, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST):
    """Simple objective  function using simulate."""
    result = simulate(genome, instance, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST)
    return result['total_value']




def generate_instance(width, height, num_items, seed=None):
    """
    Generate a random instance for the robot optimization problem.
    
    Args:
        width: Grid width (M dimension)
        height: Grid height (N dimension) 
        num_items: Number of items to place
        seed: Random seed for reproducibility
    
    Returns:
        instance: numpy array of shape (height, width, 2)
                 [:,:,0] contains values, [:,:,1] contains weights
    """

    # create an independent RNG for use inside this function,
    # without affecting the global random state. we can either
    # use a provided seed, or a random seed.
    if seed is None:
        rng = random.Random()
    else:
        rng = random.Random(seed)
    
    # Initialize empty grid
    instance = np.zeros((height, width, 2), dtype=int)
    
    # Generate all possible positions (excluding home at (0,0))
    positions = [(i, j) for i in range(height) for j in range(width) if not (i == 0 and j == 0)]
    
    # Randomly select positions for items
    if num_items > len(positions):
        raise ValueError(f"Cannot place {num_items} items in {width}x{height} grid (max {len(positions)})")
    
    item_positions = rng.sample(positions, num_items)
    
    # Place items with random values and weights
    for i, j in item_positions:
        value = rng.randint(1, 20)  # values 1-20
        weight = rng.randint(1, 20)  # weights 1-20g
        instance[i, j, 0] = value
        instance[i, j, 1] = weight
    
    return instance

def print_instance_stats(instance):
    """Print basic statistics about an instance."""
    height, width = instance.shape[:2]
    items = instance[instance[:,:,0] > 0]
    
    if len(items) > 0:
        total_value = np.sum(items[:, 0])
        total_weight = np.sum(items[:, 1])
        avg_value = np.mean(items[:, 0])
        avg_weight = np.mean(items[:, 1])
        
        print(f"Instance: {width}x{height}, {len(items)} items")
        print(f"Total value: {total_value}, Total weight: {total_weight}")
        print(f"Average value: {avg_value:.1f}, Average weight: {avg_weight:.1f}")
    else:
        print(f"Instance: {width}x{height}, 0 items")


def view_instance(instance):
    """
    Print a visual representation of the instance.
    
    Args:
        instance: numpy array of shape (height, width, 2)
    """
    height, width = instance.shape[:2]
    
    print(f"Instance {width}x{height} (Home at top-left)")
    print("Legend: H=Home, R=Robot, .=Empty, V/W=Value/Weight")
    print()
    
    # Print column numbers header
    print("   ", end="")
    for j in range(width):
        print(f"{j:2d}", end="")
    print()
    
    # Print each row (from top to bottom for normal viewing)
    for i in range(height):
        print(f"{i:2d} ", end="")
        
        for j in range(width):
            if instance[i, j, 0] == -1:
                print(" R", end="")  # Robot position
            elif i == 0 and j == 0:
                print(" H", end="")  # Home position
            elif instance[i, j, 0] > 0:
                value = instance[i, j, 0]
                weight = instance[i, j, 1]
                print(f"{value:2d}", end="")  # Show value
            else:
                print(" .", end="")  # Empty cell
        print()
    
    print()
    
    # Print detailed item list
    items = []
    for i in range(height):
        for j in range(width):
            if instance[i, j, 0] > 0:
                value = instance[i, j, 0]
                weight = instance[i, j, 1]
                items.append((i, j, value, weight))
    
    if items:
        print("Items:")
        print("Pos    Value Weight V/W")
        for i, j, value, weight in items:
            ratio = value / weight
            print(f"({i:2d},{j:2d})  {value:2d}    {weight:2d}  {ratio:.2f}")
    else:
        print("No items in instance.")

def visualise_program_behaviour(instance, program, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST):
    print(f"Fuel: {program[0]:.2f}")
    print(f"Commands: {''.join(program[1:])}")
    history = simulate(program, instance, MAX_FUEL, FUEL_COST_PER_UNIT, ROBOT_WEIGHT, ROBOT_COST)
    for field, action, value in zip(history['map_history'], history['actions'], history['value_history']):
        view_instance(field)
        print(action)
        print(value)
        print("---")
    print(history[visualise_program_behaviour('total_value')])