import numpy as np
import yaml

from network import Capped, Link, LinkCollection, Node, NodeCollection


class GraphInfo:
    def __init__(
        self,
        layer_count,
        min_node,
        max_node,
        min_in_cap,
        max_in_cap,
        min_out_cap,
        max_out_cap,
        min_flow,
        max_flow,
        min_process,
        max_process,
        link_chance,
        graph_name,
        seed=0,
    ):
        self.layer_count = layer_count
        self.min_node = min_node
        self.max_node = max_node
        self.min_in_cap = min_in_cap
        self.max_in_cap = max_in_cap
        self.min_out_cap = min_out_cap
        self.max_out_cap = max_out_cap
        self.min_flow = min_flow
        self.max_flow = max_flow
        self.min_process = min_process
        self.max_process = max_process
        self.seed = seed
        self.link_chance = link_chance
        self.graph_name = graph_name


def create_graph(graph_info: GraphInfo):
    node_count: list[int] = []
    node_list = NodeCollection()
    id_accumulation = int(0)
    rng = np.random.default_rng(seed=graph_info.seed)

    # Generate number of nodes in each layer
    if isinstance(graph_info.min_node, int) and isinstance(graph_info.max_node, int):
        # Same range for all layers
        node_count = list(
            rng.integers(
                low=graph_info.min_node,
                high=graph_info.max_node + 1,
                size=int(graph_info.layer_count),
                dtype=int,
            )
        )
    elif (
        isinstance(graph_info.min_node, list)
        and isinstance(graph_info.max_node, list)
        and len(graph_info.min_node) == graph_info.layer_count
        and len(graph_info.max_node) == graph_info.layer_count
    ):
        # Per-layer ranges
        for i in range(graph_info.layer_count):
            low = graph_info.min_node[i]
            high = graph_info.max_node[i]
            node_count.append(int(rng.integers(low=low, high=high + 1, dtype=int)))
    else:
        raise ValueError(
            "min_node and max_node must both be int or list with length layer_count"
        )

    for layer, value in enumerate(node_count):
        for i in range(value):
            id = int(id_accumulation + i)
            input_cap = rng.integers(
                graph_info.min_in_cap, graph_info.max_in_cap, dtype=int
            )
            output_cap = rng.integers(
                graph_info.min_out_cap, graph_info.max_out_cap, dtype=int
            )
            layer_id = layer
            process = rng.integers(
                graph_info.min_process, graph_info.max_process, dtype=int
            )
            node_list.add_nodes(
                id, layer_id, int(input_cap), int(output_cap), int(process)
            )

        id_accumulation += value

    # Randomly generate links between consecutive layers only
    link_list = LinkCollection()
    for layer in range(graph_info.layer_count - 1):
        current_layer_nodes = node_list.get_layer(layer)
        next_layer_nodes = node_list.get_layer(layer + 1)

        print(f"Generating links between layer {layer} and layer{layer + 1}")
        for start_node in current_layer_nodes:
            for end_node in next_layer_nodes:
                # Randomly decide whether to create a link from start_node to end_node
                if rng.random() <= graph_info.link_chance:
                    flow_cap = rng.integers(
                        graph_info.min_flow, graph_info.max_flow, dtype=int
                    )
                    # layer index of the link is the lower (source) layer
                    link_list.add_link(
                        float(flow_cap), layer, start_node.id, end_node.id
                    )
                    print("Added links")

    return (node_list, link_list)


def print_graph(output_file_name, graph_info: GraphInfo):
    (nodes, links) = create_graph(graph_info)
    with open(output_file_name, "w", encoding="utf8") as outfile:
        yaml.dump(
            {
                "nodes": [
                    {
                        "id": node.id,
                        "layer_id": node.layer_id,
                        "input_cap": node.input.cap_value,
                        "output_cap": node.output.cap_value,
                        "process": node.process,
                    }
                    for node in nodes.dump_nodes()
                ],
                "links": [
                    {
                        "layer_id": link.layer_id,
                        "start_id": link.start_id,
                        "end_id": link.end_id,
                        "bandwidth": link.flow.cap_value,
                    }
                    for link in links.dump_links()
                ],
            },
            outfile,
        )
    nodes.print_nodes_info()
    links.print_links_info()
    for node in nodes.dump_nodes():
        print(
            f"Node {node.id}, layer {node.layer_id}, input cap {node.input.cap_value}, output cap {node.output.cap_value}, process {node.process}, actual input {node.input.actual_value}, actual output {node.output.actual_value}"
        )
    for link in links.dump_links():
        print(
            f"Link from {link.start_id} to {link.end_id} with bandwidth {link.flow.cap_value} and actual flow {link.flow.actual_value}"
        )


def load_graph_spec(spec_file_name: str) -> GraphInfo:

    DEFAULT_LINK_CHANCE = 0.5
    MINIMUM_PROCESS_SPEED = 1
    MINIMUM_NODE_LAYER = 1
    with open(spec_file_name, "r", encoding="utf8") as input_file:
        data = yaml.safe_load(input_file)

    graph_name = data.get("name", "default_graph")

    layer_count = int(data.get("layers", 0))

    min_node = int(data.get("min_node", MINIMUM_NODE_LAYER))
    max_node = int(data.get("max_node", min_node))

    min_in_cap = int(data["input_min"])
    max_in_cap = int(data["input_max"])
    min_out_cap = int(data.get("output_min", min_in_cap)) + 1
    max_out_cap = int(data.get("output_max", max_in_cap)) + 1

    min_flow = int(data["flow_min"])
    max_flow = int(data["flow_max"])

    min_process = int(data.get("process_min", MINIMUM_PROCESS_SPEED))
    max_process = int(data.get("process_max", min_process)) + 1

    link_chance = float(data.get("link_chance", DEFAULT_LINK_CHANCE))
    seed = int(data.get("seed", 0))

    print(yaml.dump(data))
    return GraphInfo(
        graph_name=graph_name,
        layer_count=layer_count,
        min_node=min_node,
        max_node=max_node,
        min_in_cap=min_in_cap,
        max_in_cap=max_in_cap,
        min_out_cap=min_out_cap,
        max_out_cap=max_out_cap,
        min_flow=min_flow,
        max_flow=max_flow,
        min_process=min_process,
        max_process=max_process,
        link_chance=link_chance,
        seed=seed,
    )


def read_spec_files() -> GraphInfo:

    spec_file_name = input("Type the spec file's name: ")
    return load_graph_spec(spec_file_name)


graph_info = read_spec_files()
(node, links) = create_graph(graph_info)
print_graph(f"{graph_info.graph_name}.yaml", graph_info)

# graph_spec.yaml
# graph_spec.yaml
