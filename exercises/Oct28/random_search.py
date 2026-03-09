import random as rd

def objective(x, y):
    return x ** 2 + y ** 2


def random_search(iteration=1000, bounds=[(-20, 20), (-20, 20)]):
    best_x, best_y = None, None
    best_score = float("inf")

    for i in range(iteration):
        x = rd.uniform(bounds[0][0], bounds[0][1])
        y = rd.uniform(bounds[1][0], bounds[1][1])
        score = objective(x, y)
        # print("iteration:", i, "x:", x, "y:", y, "score:", score)
        if score < best_score:
            best_x, best_y = x, y
            best_score = score
    print(f"iteration:{iteration}, Best score: {best_score}")
    return best_x,best_y,best_score


iterations = [10,100,1000,10000,100000,1000000]
for iteration in iterations:
    random_search(iteration=iteration)


