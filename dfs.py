import random

class Node:
    def __init__(self, name):
        self.name = name
        self.children = {}

    def add_child(self, child, cost):
        self.children[child] = cost

def print_graph(nodes):
    for node in nodes.values():
        print(f"{node.name}:")
        for child, cost in node.children.items():
            print(f"\t{child.name} (costo={cost})")

def read_graph_from_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        init_node = None
        goal_node = None
        nodes = {}

        for line in lines:
            if line.startswith("Init:"):
                init_node = line.strip().split()[1]
            elif line.startswith("Goal:"):
                goal_node = line.strip().split()[1]
            else:
                parts = line.strip().split()
                if len(parts) == 1:
                    name = parts[0]
                    nodes[name] = Node(name)
                elif len(parts) == 3:
                    parent, child, cost = parts
                    nodes[parent].add_child(nodes[child], int(cost))
                elif len(parts) != 0:
                    print(f"Error: línea no válida: {line}")

    return init_node, goal_node, nodes

def depth_first_search(init_node, goal_node, nodes):
    init = nodes[init_node]
    goal = nodes[goal_node]

    stack = [(init, [])]
    explored = set()

    path = []
    total_cost = 0
    node_expansions = {node.name: 0 for node in nodes.values()}

    while stack:
        node, path_so_far = stack.pop()
        if node not in explored:
            explored.add(node)
            node_expansions[node.name] += 1

            if node == goal:
                path = path_so_far + [node.name]
                total_cost = sum(nodes[path[i]].children[nodes[path[i+1]]] for i in range(len(path)-1))
                return path, total_cost, node_expansions

            children = list(node.children.items())
            random.shuffle(children)

            for child, cost in children:
                stack.append((child, path_so_far + [node.name]))

    return None, None, None

if __name__ == "__main__":
    init_node, goal_node, nodes = read_graph_from_file("graph.txt")

    path, total_cost, node_expansions = depth_first_search(init_node, goal_node, nodes)

    if path:
        print(" -> ".join(path))
        print(f"Costo: {total_cost}")
        for node, expansions in node_expansions.items():
            print(f"{node}: número de veces que se expandió: {expansions}")
    else:
        print("No se encontró una solución")