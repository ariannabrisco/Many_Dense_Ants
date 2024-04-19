"""
Graph Theory HW5
Author: Tanner Collins
Date: 4/10/2024
"""

import networkx as nx
import matplotlib.pyplot as plt
from math import inf

def dfs(graph, start, NOV):
    low = [inf for _ in range(NOV)]
    disc = [-1 for _ in range(NOV)]
    parents = [None for _ in range(NOV)]
    stack = []  # Stack to keep track of visited vertices
    articulation_points = set()  # Set to store articulation points
    blockNum = 1

    def dfs_recursive(node, time):
        nonlocal low, disc, parents, stack, blockNum, articulation_points
       
        disc[node-1] = time
        low[node-1] = time
        time += 1
       
        # Add node to the stack
        stack.append(node)

        # Add unvisited neighbors to the stack
        for neighbor in graph.neighbors(node):
            if disc[neighbor-1] == -1:
                parents[neighbor-1] = node
                time = dfs_recursive(neighbor, time)

                low[node-1] = min(low[node-1], low[neighbor-1])
               
                # Check for articulation points
                if low[neighbor-1] >= disc[node-1] and parents[node-1] is not None:
                    articulation_points.add(node)

            elif neighbor != parents[node-1]:
                low[node-1] = min(low[node-1], disc[neighbor-1])

        # Check for biconnected components
        if all(low[neighbor-1] >= disc[node-1] for neighbor in graph.neighbors(node) if neighbor != parents[node-1]):
            # Pop vertices off the stack until the current node is popped
            biconnected_component = []
            while stack[-1] != node:
                biconnected_component.append(stack.pop())
            biconnected_component.append(stack.pop())
            if parents[biconnected_component[-1]-1]:
                biconnected_component.append(parents[biconnected_component[-1]-1])
            print("Block {0} size {1}, Vertices: ".format(blockNum, len(biconnected_component)), end="")
            print(*biconnected_component, sep=" ")
            blockNum += 1                

        return time

    dfs_recursive(start, 0)
   
    print("Articulation Points: ", end="")
    print(*articulation_points, sep=" ")

numberOfVertices, numberOfEdges = map(
    int,
    (input("Please input 2 numbers separated by a space, the first will be the number of vertices and the second will be the number of edges: ")).split())

edges = [
    list(
        map(
            int,
            input("Please do so again for each edge, each number will be one of the two vertices that the edge connects: ").split()))
    for _ in range(numberOfEdges)
]
   
G = nx.Graph()

G.add_nodes_from(list(map(lambda a : a + 1, range(numberOfVertices))))
G.add_edges_from(edges)

nx.draw(G, with_labels = True)
plt.savefig("filename.png")

print("DFS traversal starting from node 1:")
test = dfs(G, 1, 8)