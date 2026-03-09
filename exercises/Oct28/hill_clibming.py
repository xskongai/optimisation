import random
import matplotlib.pyplot as plt

from numpy.ma.extras import average


def objective_function(x):
    return -(x - 3) ** 2 + 10


def init(search_space):
    return random.uniform(search_space[0], search_space[1])


def nbr(search_space, current, step_size):
    left = max(current - step_size, search_space[0])
    right = min(current + step_size, search_space[1])
    return left, right


def hill_climbing(f, step_size=0.1, max_iterations=100000, search_space=None):
    current_x = init(search_space)
    current_y = f(current_x)
    final_iteration = 0

    for i in range(max_iterations):
        neighbours = nbr(search_space, current_x, step_size)
        neighbour_x = max(neighbours, key=f)
        neighbour_y = f(neighbour_x)
        print(f"iteration {i},the neighbors:{neighbours}, neighbor_x:{neighbour_x},neighbor_y:{neighbour_y}")

        if neighbour_y > current_y:
            current_x, current_y = neighbour_x, neighbour_y
            print(f"current_x:{current_x},current_y:{current_y}")
        else:
            print(f" iteration {i},then found the optimal solution ")
            final_iteration = i
            break
    return current_x, current_y, final_iteration


#  demo
search_space = [-10, 10]
final_iterations = []
# for i in range(100):
#     best_x, best_y, final_iteration = hill_climbing(objective_function, search_space=search_space)
#     final_iterations.append(final_iteration)
#     print(f"best_x:{best_x},best_y:{best_y}")
#     print(best_x, best_y)
#     print(f"final_iteration{final_iteration}")
# mean = average(final_iterations) + 1
# print(f"mean:{mean}")

steps = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
means = []
for step in steps:
    for i in range(100):
        best_x, best_y, final_iteration = hill_climbing(objective_function, step_size=step, search_space=search_space)
        final_iterations.append(final_iteration)
        print(f"best_x:{best_x},best_y:{best_y}")
        print(best_x, best_y)
        print(f"final_iteration{final_iteration}")
    mean = average(final_iterations) + 1
    means.append(mean)
    print(f"mean:{mean}")


def visualize_results(steps, means):
    # create a figure window with size 10*6 inches
    plt.figure(figsize=[12, 8])
    # plot a line chart:x-axis,is step size ,y-axis is average iterations,with blue circle markers
    plt.plot(steps, means, marker='o', linestyle='-', color='blue')

    # add value labels to each point
    for x, y in zip(steps, means):
        plt.text(x, y + 1, f'{y:.1f}', ha='center', va='bottom', fontsize=10)

    # set the chart title to "Relationship between step size and average iterations"
    plt.title("hill-climbing:Relationship between stepsize and average iterations")
    plt.xlabel("step size")
    plt.ylabel("average iterations")

    plt.show()


visualize_results(steps, means)
