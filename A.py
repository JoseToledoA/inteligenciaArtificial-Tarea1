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

def a_star_search(init_node, goal_node, nodes):
    init = nodes[init_node]
    goal = nodes[goal_node]

    frontier = PriorityQueue()
    frontier.put((0, init))
    came_from = {}
    cost_so_far = {}
    node_expansions = {node.name: 0 for node in nodes.values()}
    came_from[init.name] = None
    cost_so_far[init.name] = 0

    while not frontier.empty():
        current_cost, current = frontier.get()

        if current == goal:
            path = []
            while current is not None:
                path.append(current.name)
                current = came_from[current.name]
            path.reverse()
            return path, cost_so_far[goal.name], node_expansions

        for child, edge_cost in current.children.items():
            new_cost = cost_so_far[current.name] + edge_cost
            if child.name not in cost_so_far or new_cost < cost_so_far[child.name]:
                cost_so_far[child.name] = new_cost
                priority = new_cost + child.heuristic
                frontier.put((priority, child))
                came_from[child.name] = current
                node_expansions[current.name] += 1

    return None, None, None

if __name__ == "__main__":
    init_node, goal_node, nodes = read_graph_from_file("graph_euristicas.txt")

    path, total_cost, node_expansions = a_star_search(init_node, goal_node, nodes)

    if path:
        print(" -> ".join(path))
        print(f"Costo: {total_cost}")
        for node, expansions in node_expansions.items():
            print(f"{node}: número de veces que se expandió: {expansions}")
    else:
        print("No se encontró una solución")
