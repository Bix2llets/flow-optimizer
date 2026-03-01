import cvxpy as cp
import numpy as np
from network import Node, Link


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


def optimize_layer(
    current_layer: list[Node], prev_layer: list[Node], connecting_edge: list[Link]
):
    constraints = []
    edge_value = cp.Variable(len(connecting_edge))
    # NOTE: Bound the flow between 0 and bandwidth (both inclusive)
    edge_cap = np.array([link.flow.cap_value for link in connecting_edge])

    constraints.append(0 <= edge_value)
    constraints.append(edge_value <= edge_cap)

    # NOTE: Add the constraint of matching previous layer's output
    compress_map = {}
    for node in prev_layer:
        if node.id in compress_map:
            pass
        else:
            compress_map[node.id] = len(compress_map)

    prev_output_vector = [node.output.actual_value for node in prev_layer]
    output_mul_matrix = np.zeros((len(prev_layer), len(connecting_edge)))
    for node in prev_layer:
        row = compress_map[node]
        for col, edge in enumerate(connecting_edge):
            if edge.start_id == node.id:
                output_mul_matrix[row, col] = 1

    constraints.append(output_mul_matrix @ edge_value == prev_output_vector)

    pass
