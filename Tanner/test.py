import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

nodes = [1, 2, 3, 4]
edges = [[1, 2], [1, 3], [3, 4], [2, 4]]

G.add_nodes_from(nodes)
G.add_edges_from(edges)
