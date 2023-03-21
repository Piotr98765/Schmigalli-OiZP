import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

# przykładowa tabela z detalami i ich kolejnością operacji
details = {
    "detail1": {"packages": 100, "operations": "cbabdgihjf"},
    "detail2": {"packages": 100, "operations": "cabagdhijh"},
    "detail3": {"packages": 100, "operations": "acfbigfc"},
    "detail4": {"packages": 100, "operations": "cacbdgjhj"},
}

# wyznaczanie rozmiaru macierzy powiązań
max_operation = max([max(list(details[detail]["operations"])) for detail in details])
size = ord(max_operation) - ord("a") + 1

# inicjalizacja macierzy powiązań
matrix = np.zeros((size, size))
for i in range(size):
    for j in range(size):
        if i == j:
            matrix[i, j] = np.nan


# wypełnianie macierzy powiązań
for detail in details.values():
    packages = detail["packages"]
    operations = detail["operations"]
    for i in range(len(operations) - 1):
        source = ord(operations[i]) - ord("a")
        destination = ord(operations[i+1]) - ord("a")
        matrix[source, destination] += packages
        matrix[destination, source] += packages


# stworzenie siatki
m = 10
n = 10
G = nx.triangular_lattice_graph(m, n)

# policzona ręcznie
order_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

pos = nx.get_node_attributes(G, 'pos')

total_costs = {}


# liczba iteracji
for i in range(10):

    # miejsce na pierwszy wierzchołek
    vertices = list(G.nodes())
    a = (2,4)

    # wybieramy losowo drugi wierzchołek połączony z pierwszym
    b = random.choice(list(G.neighbors(a)))

    # tworzymy zbiór wierzchołków połączonych z pierwszymi dwoma
    connected_nodes = set(G.neighbors(a)).union(set(G.neighbors(b)))


    # dodanie etykiet dla pierwszych dwóch wierzchołków
    labels = {a: order_list[0], b: order_list[1]}

    # określenie początkowego kosztu między wierzchołkiem pierwszym i drugim
    total_cost = 1140

    # zbiór wierzchołków już wykorzystanych
    chosen_nodes = set([a, b])

    # dodanie kolejnych wierzchołków i krawędzi

    for label in order_list[2:]:
        
        # wybieramy losowy wierzchołek
        c = random.choice(list(connected_nodes - set([a, b]) - chosen_nodes))

        
        # dodajemy wierzchołek
        # celowe ominięcie wierzchołka "E"
        if label != "E":
            G.add_node(c)
            # aktualizujemy zbiór wierzchołków połączonych z już wybranymi
            connected_nodes = connected_nodes.union(set(G.neighbors(c))).difference(set([a, b]))
            chosen_nodes.add(c)
            # dodajemy etykietę dla nowego wierzchołka
            labels[c] = label
            # Sprawdzenie czy nowo dodany wierzchołek ma wspólną wartość z dodanymi wierzchołkami w macierzy
            for l in labels.values():
                index_col = ord(labels[c]) - ord("A")
                index_row = ord(l) - ord("A")
                distances = {}
                if matrix[index_col][index_row] != 0 and np.isnan(matrix[index_col,index_row]) == False:
                    for position, name in labels.items():
                        if name == labels[c]:
                            w1 = position
                        elif name == l:
                            w2 = position
                    # obliczenie najkrótszej drogi
                    distance = nx.shortest_path_length(G, source=w1, target=w2)
                    # aktulizacja kosztu
                    total_cost += distance*matrix[index_col][index_row]
            a, b = b, c

    total_costs[total_cost] = labels

# znalezienie najmniejszej wartości (Q)
min_key = min(total_costs.keys())
min_value = total_costs[min_key]
print(min_key)

#wygenerowanie grafu
m = 8
n = 8
G = nx.triangular_lattice_graph(m, n)

pos = nx.get_node_attributes(G, 'pos')

vertices = list(G.nodes())

nx.draw(G, pos=pos, with_labels=True)

nx.draw_networkx_labels(G, pos, labels=labels, font_size=16, font_color='r')

plt.show()

