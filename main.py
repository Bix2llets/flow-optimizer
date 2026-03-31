from bitmask import Bitmask
from graph_loader import graph_loader
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
