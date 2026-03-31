from bitmask import Bitmask
from graph_loader import graph_loader
from metric import flow_fairness_metric
from network import Link, LinkCollection, Node, NodeCollection
from optimizer import optimize_layer, update_layer

file_name = "graph_1.yaml"
(nodes, links) = graph_loader(file_name)
max_layer_id = max(node.layer_id for node in nodes.nodes)
for layer_id in range(0, max_layer_id - 1):
    update_layer(
        nodes,
        links,
        optimize_layer(nodes, links, layer_id + 1, layer_id, layer_id),
        layer_id + 1,
        layer_id,
        layer_id,
    )
nodes.print_nodes_info()
links.print_links_info()

flow_fairness_list = []
for node in nodes.dump_nodes():
    output_flow = []
    id = node.id
    for link in links.get_starts_at(id):
        output_flow.append(link.flow.actual_value)
    flow_fairness_list.append(float(flow_fairness_metric(output_flow=output_flow)))

print(flow_fairness_list)
