class Capped:
    def __init__(self, cap_value=0, actual_value=0):
        self.cap_value = cap_value
        self.actual_value = actual_value


class Node:
    def __init__(
        self, id: int, layer_id: int, input: Capped, output: Capped, process: int
    ):
        self.layer_id = layer_id
        self.id = id
        self.input = input
        self.output = output
        self.process = process


class Link:
    def __init__(self, flow: Capped, layer_id, start_id: int, end_id: int):
        self.layer_id = layer_id
        self.flow = flow
        self.start_id = start_id
        self.end_id = end_id


class NodeCollection:
    def __init__(self, layer_id):
        self.nodes: list[Node] = []
        self.layer_id = layer_id

    def is_layer_blank(self, layer):
        for node in self.nodes:
            if node.layer_id == layer:
                return True
        return False

    def add_nodes(
        self, id: int, layer_id: int, input_cap: int, output_cap: int, process: int
    ):
        for node in self.nodes:
            if node.id == id:
                print("")
                return

        new_node = Node(
            id,
            layer_id,
            Capped(cap_value=input_cap, actual_value=0),
            Capped(cap_value=output_cap, actual_value=0),
            process,
        )
        self.nodes.append(new_node)


class LinkCollection:
    def __init__(self, layer_id):
        self.links: list[Link] = []
        self.layer_id = layer_id

    def is_blank(self):
        return len(self.links) == 0

    def add_link(self, bandwidth: int, layer_id: int, start_id: int, end_id: int):
        for link in self.links:
            if link.start_id == start_id and link.end_id == end_id:
                print("Existing link")
                return

        self.links.append(Link(Capped(bandwidth, 0), layer_id, start_id, end_id))

    def get_layer(self, layer_id):
        return [link for link in self.links if link.layer_id == layer_id]

    def get_starts_at(self, start_id):
        return [link for link in self.links if link.start_id == start_id]

    def get_ends_at(self, end_id):
        return [link for link in self.links if link.end_id == end_id]
