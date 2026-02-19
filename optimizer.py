import cvxpy as cp
import numpy as np


def cvxpy_testing_function():
    A = np.random.randint(-10, 10, (2, 3))
    x = cp.Variable(3)
    B = np.random.randint(0, 10, 2)

    objective_func = cp.Minimize(cp.sum_squares(A @ x - B))

    constraints = [0 <= x, x <= 10]
    problem = cp.Problem(objective_func, constraints)
    problem.solve()

    print(x.value)
    print(A)
    print(B)

    pass


cvxpy_testing_function()
