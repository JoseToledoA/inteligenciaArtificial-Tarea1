from queue import PriorityQueue

class Node:
    def __init__(self, name, heuristic):
        self.name = name
        self.heuristic = heuristic
        self.children = {}

    def add_child(self, child, cost):
        self.children[child] = cost

    def __lt__(self, other):
        return self.heuristic < other.heuristic


def print_graph(nodes):
    for node in nodes.values():
        print(f"{node.name} (h={node.heuristic}):")
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
                if len(parts) == 2:
                    name, heuristic = parts
                    nodes[name] = Node(name, int(heuristic))
                elif len(parts) == 3:
                    parent, child, cost = parts
                    nodes[parent].add_child(nodes[child], int(cost))
                elif len(parts) != 0:
                    print(f"Error: línea no válida: {line}")
                
    return init_node, goal_node, nodes



def greedy_search(init_node, goal_node, nodes):
    init = nodes[init_node]
    goal = nodes[goal_node]

    frontier = {init}
    explored = set()

    path = []
    total_cost = 0
    node_expansions = {node.name: 0 for node in nodes.values()}

    while frontier:
        node = min(frontier)
        frontier.remove(node)

        if node == goal:
            path.append(node.name)
            return path, total_cost, node_expansions

        explored.add(node)
        node_expansions[node.name] += 1

        for child, cost in sorted(node.children.items(), key=lambda x: x[1] + x[0].heuristic):
            if child not in explored and child not in frontier:
                frontier.add(child)

        if frontier:
            next_node = min(frontier, key=lambda x: x.heuristic)
            edge_cost = node.children[next_node]
            total_cost += edge_cost
        path.append(node.name)

    return None, None, None





if __name__ == "__main__":
    init_node, goal_node, nodes = read_graph_from_file("graph_euristicas.txt")

    path, total_cost, node_expansions = greedy_search(init_node, goal_node, nodes)

    if path:
        print(" -> ".join(path))
        print(f"Costo: {total_cost}")
        for node, expansions in node_expansions.items():
            print(f"{node}: número de veces que se expandió: {expansions}")
    else:
        print("No se encontró una solución")