import random
import matplotlib.pyplot
import matplotlib.pyplot as plt

plt

search_space = [-10, 10]


def objective_function(x):
    return -(x - 3) ** 2 + 10


def init(search_space):
    return random.uniform(search_space[0], search_space[1])


def nbr(search_space, current, step):
    left = max(current - step, search_space[0])
    right = min(current + step, search_space[1])
    return [left, right]


def hill_climbing_fixed_step(f, step_siz=0.5, max_iterations=1000, search_space=None):
    current_x = init(search_space)
    current_y = f(current_x)

    final_iteration = 0

    for i in range(max_iterations):
        neighbours = nbr(search_space, current_x, step_siz)
        next_x = max(neighbours, key=f)
        next_y = f(next_x)

        if next_y > current_y:
            current_x, current_y = next_x, next_y
        else:
            final_iteration = i
            break
    return current_x, current_y, final_iteration


def hill_climbing_linear(f, initial_step=0.5, decay_rate=0.01, max_iterations=1000, search_space=None):
    current_x = init(search_space)
    current_y = f(current_x)

    for i in range(max_iterations):
        step_size = max(initial_step * (1 - decay_rate), 0.01)
        neighbours = nbr(search_space, current_x, step_size)
        next_x = max(neighbours, key=f)
        next_y = f(next_x)
        if next_y > current_y:
            current_x, current_y = next_x, next_y
        else:
            final_iteration = i
            break

    return current_x, current_y, final_iteration


def hill_climbing_exponential(f, initial_step=0.5, decay_factor=0.99, max_iterations=1000, search_space=None):
    current_x = init(search_space)
    current_y = f(current_x)

    for i in range(max_iterations):
        step_size = max(initial_step * (decay_factor ** i), 0.01)
        neighbours = nbr(search_space, current_x, step_size)
        next_x = max(neighbours, key=f)
        next_y = f(next_x)
        if next_y > current_y:
            current_x, current_y = next_x, next_y
        else:
            final_iteration = i
            break

    return current_x, current_y, final_iteration


# adaptive shrinking step-size
def hill_climbing_adaptive(f, initial_step=0.5, shrink_factor=0.7, patience=5, max_iterations=1000, search_space=None):
    epsilon = 1e-5
    current_x = init(search_space)
    current_y = f(current_x)

    step_size = initial_step
    no_improvement = 0

    for i in range(max_iterations):
        neighbours = nbr(search_space, current_x, step_size)
        next_x = max(neighbours, key=f)
        next_y = f(next_x)
        if next_y > current_y:
            current_x, current_y = next_x, next_y
            no_improvement = 0
        else:
            no_improvement += 1
            if no_improvement > patience:
                step_size = max(shrink_factor * step_size, 0.01)
                if (no_improvement >= patience and step_size <= 0.01) or (abs(next_y - current_y) < epsilon):
                    final_iteration = i
                    break
                else:
                    no_improvement = 0

    return current_x, current_y, final_iteration


strategies = ['fixed step', 'linear decay', 'exponential decay', 'adaptive shrinking']
search_space = [-10, 10]


def hill_climbing(f, strategy, outer_iter):
    iterations = []
    for _ in range(outer_iter):
        if strategy == 'fixed step':
            best_x, best_y, final_iteration = hill_climbing_fixed_step(f, max_iterations=1000,
                                                                       search_space=search_space)
        elif strategy == 'linear decay':
            best_x, best_y, final_iteration = hill_climbing_linear(f, max_iterations=1000, search_space=search_space)
        elif strategy == 'exponential decay':
            best_x, best_y, final_iteration = hill_climbing_exponential(f, max_iterations=1000,
                                                                        search_space=search_space)
        elif strategy == 'adaptive shrinking':
            best_x, best_y, final_iteration = hill_climbing_adaptive(f, max_iterations=1000, search_space=search_space)
    iterations.append(final_iteration + 1)
    return iterations


def visualize_data(results):
    plt.figure(figsize=(10, 6))
    colors = ["green", "red", "pink", "purple"]
    plt.bar(strategies, results, color=colors)

    for i, v in enumerate(results):
        plt.text(i, v + 1, f'{v:.1f}', ha='center', va='bottom', fontsize=10)

    plt.title('Hill Climbing :changeable steps experiment')
    plt.xlabel('Strategy')
    plt.ylabel('iterations')
    plt.show()



# test
results = []
for strategy in strategies:
    all_iterations = hill_climbing(objective_function,strategy,outer_iter=100)
    avg_iterations = sum(all_iterations) / len(all_iterations)
    results.append(avg_iterations)


visualize_data(results)

