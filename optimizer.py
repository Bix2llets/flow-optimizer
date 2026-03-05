import cvxpy as cp
import numpy as np
from network import Node, Link
from network import NodeCollection, LinkCollection


# NOTE: This function changed from the proposed plan by setting the objective function to maximize flows with penalty of congestion
# NOTE: This is to ensure the solver can work in bottleneck scenario when previous layer's output is greater than the next layer's input
def optimize_layer(
    nodes: NodeCollection,
    links: LinkCollection,
    current_index: int,
    previous_index: int,
    link_index: int,
):
    connecting_edge = links.get_layer(link_index)

    current_layer = nodes.get_layer(current_index)
    previous_layer = nodes.get_layer(previous_index)
    constraints = []
    edge_value = cp.Variable(len(connecting_edge))
    # NOTE: Set objective function

    current_query_dict = {}
    for value in current_layer:
        # print(value.id)
        current_query_dict[value.id] = value

    target_capabilities = []
    for edge in connecting_edge:
        target_node_id = edge.end_id
        target_node = current_query_dict[target_node_id]
        target_capabilities.append(target_node.process)

    network_congestion = target_capabilities @ edge_value
    total_flow = cp.sum(edge_value)

    objective_function = cp.Maximize(total_flow - 0.1 * network_congestion)

    # NOTE: Bound the flow between 0 and cap of current flow, prev output and next input (both inclusive)
    edge_cap = np.array(
        [
            min(
                [
                    link.flow.cap_value,
                    nodes.get_node(link.end_id).input.cap_value,
                    nodes.get_node(link.start_id).output.cap_value,
                ]
            )
            for link in connecting_edge
        ]
    )

    constraints.append(0 <= edge_value)
    constraints.append(edge_value <= edge_cap)

    # NOTE: Add the constraint of matching previous layer's output
    prev_output_compress_map = {}
    for node in previous_layer:
        if node.id in prev_output_compress_map:
            pass
        else:
            prev_output_compress_map[node.id] = len(prev_output_compress_map)

    prev_output_vector = [
        min(
            [
                node.output.actual_value,
                sum([link.flow.cap_value for link in links.get_starts_at(node.id)]),
            ]
        )
        for node in previous_layer
    ]
    output_mul_matrix = np.zeros((len(previous_layer), len(connecting_edge)))
    for node in previous_layer:
        row = prev_output_compress_map[node.id]
        for col, edge in enumerate(connecting_edge):
            if edge.start_id == node.id:
                output_mul_matrix[row, col] = 1

    print(f"output_mul_matrix\n{output_mul_matrix}")
    print(f"edge_value\n{edge_value}")
    print(f"prev_output_vector\n{prev_output_vector}")
    constraints.append(output_mul_matrix @ edge_value <= prev_output_vector)

    # NOTE: Add the constraint of satisfying the next layer's input
    curr_input_compress_map = {}
    for node in current_layer:
        if node.id not in curr_input_compress_map:
            curr_input_compress_map[node.id] = len(curr_input_compress_map)

    input_mul_matrix = np.zeros((len(current_layer), len(connecting_edge)))
    for node in current_layer:
        row = curr_input_compress_map[node.id]
        for col, edge in enumerate(connecting_edge):
            if edge.end_id == node.id:
                input_mul_matrix[row, col] = 1

    curr_input_cap_vector = [node.input.cap_value for node in current_layer]

    print(f"Input mul matrix: {input_mul_matrix}")
    print(f"curr_input_cap_vector: {curr_input_cap_vector}")
    constraints.append(input_mul_matrix @ edge_value <= curr_input_cap_vector)
    # NOTE: Solve the problem
    problem = cp.Problem(objective_function, constraints)
    problem.solve()
    print(edge_value)

    return edge_value


def run_test():

    nodes = NodeCollection()
    links = LinkCollection()

    nodes.add_nodes(1, 1, 3, 3, 4)
    nodes.add_nodes(2, 2, 3, 4, 2)
    nodes.add_nodes(id=3, layer_id=1, input_cap=4, output_cap=2, process=2)

    links.add_link(1, 1, 1, 2)
    links.add_link(2, 1, 3, 2)

    nodes.get_node(1).output.actual_value = 3
    nodes.get_node(3).output.actual_value = 2
    print(nodes.get_layer(1))
    optimized = optimize_layer(nodes, links, 2, 1, 1)
    print(optimized.value)

    pass


run_test()
