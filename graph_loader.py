import yaml

from network import LinkCollection, NodeCollection


def graph_loader(yaml_file) -> tuple[NodeCollection, LinkCollection]:

    with open(yaml_file, "r", encoding="utf8") as input_file:
        data = yaml.safe_load(input_file)

    links = LinkCollection()
    link_data = data.get("links", [])
    for link in link_data:
        links.add_link(
            start_id=link["start_id"],
            end_id=link["end_id"],
            bandwidth=link["bandwidth"],
            layer_id=link["layer_id"],
        )

    nodes = NodeCollection()
    node_data = data.get("nodes", [])
    for node in node_data:
        nodes.add_nodes(
            id=node["id"],
            layer_id=node["layer_id"],
            input_cap=node["input_cap"],
            output_cap=node["output_cap"],
            process=node["process"],
        )
        input_value = node.get("initial_input", 0)
        if input_value > 0:
            nodes.get_node(node["id"]).input.actual_value = input_value
        # print(
        #     f"Initial input for node {node['id']}: {nodes.get_node(node['id']).input.actual_value}"
        # )
    return (nodes, links)
