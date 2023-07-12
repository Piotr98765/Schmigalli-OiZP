# Check READ.md for details
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# An example table with details and their sequence of operations
details = {
    "detail1": {"packages": 220, "operations": "cbabdgihjf"},
    "detail2": {"packages": 120, "operations": "cabagdhijh"},
    "detail3": {"packages": 100, "operations": "acfbigfc"},
    "detail4": {"packages": 400, "operations": "cacbdgjhj"},
}

# Determining the size of the adjacency matrix
max_operation = max([max(list(details[detail]["operations"])) for detail in details])
size = ord(max_operation) - ord("a") + 1

# Initialization of the adjacency matrix
adj_matrix = np.zeros((size, size))
np.fill_diagonal(adj_matrix, np.nan)

# Filling the adjacency matrix
for detail in details.values():
    packages = detail["packages"]
    operations = detail["operations"]
    sources = np.array([ord(op) - ord("a") for op in operations[:-1]])
    destinations = np.array([ord(op) - ord("a") for op in operations[1:]])
    adj_matrix[sources, destinations] += packages
    adj_matrix[destinations, sources] += packages


# Creating the lattice grid
m = 10
n = 10
G = nx.triangular_lattice_graph(m, n)

# Manually calculated
order_list = ["H", "J", "I", "G", "D", "B", "A", "C", "F"]

pos = nx.get_node_attributes(G, 'pos')

total_costs = {}

all_neighbors = {node: set(G.neighbors(node)) for node in G.nodes()}

num_of_iterations = 1000

for i in range(num_of_iterations):
    # Place for the first vertex
    a = (2, 4)

    # Randomly choose the second vertex connected to the first one
    b = random.choice(list(all_neighbors[a]))

    # Create a set of vertices connected to the first two vertices
    connected_nodes = all_neighbors[a].union(all_neighbors[b])

    # Add labels for the first two vertices
    labels = {a: order_list[0], b: order_list[1]}

    # Determine the initial cost between the first and second vertices
    total_cost = 1140

    # Set of already chosen vertices
    chosen_nodes = {a, b}

    # Update the adjacency matrix in batches
    adjacency_updates = []

    for label in order_list[2:]:
        # Randomly choose a vertex
        c = random.choice(list(connected_nodes - chosen_nodes))

        # Add the vertex
        if label != "E":
            G.add_node(c)
            # Update the set of vertices connected to the already chosen ones
            connected_nodes = connected_nodes.union(all_neighbors[c]) - chosen_nodes
            chosen_nodes.add(c)
            # Add the label for the new vertex
            labels[c] = label

            # Check if the newly added vertex has a common value with the added vertices in the matrix
            col_index = ord(labels[c]) - ord("A")
            for row_label, row_index in labels.items():
                row_index = ord(row_index) - ord("A")
                if adj_matrix[col_index, row_index] != 0 and not np.isnan(adj_matrix[col_index, row_index]):
                    w1 = c
                    w2 = row_label
                    # Calculate the shortest path
                    distance = nx.shortest_path_length(G, source=w1, target=w2)
                    # Update the cost
                    total_cost += distance * adj_matrix[col_index, row_index]

            adjacency_updates.append((col_index, row_index, c))

        a, b = b, c

    total_costs[total_cost] = labels


# Find the minimum value (Q)
min_key = min(total_costs.keys())
min_value = total_costs[min_key]
print(min_key)


pos = nx.get_node_attributes(G, 'pos')

vertices = list(G.nodes())

nx.draw(G, pos=pos, with_labels=True)

nx.draw_networkx_labels(G, pos, labels=labels, font_size=16, font_color='r')

plt.show()
