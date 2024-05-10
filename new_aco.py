import networkx as nx
import matplotlib.pyplot as plt
import random 
import copy


def show_graph(edges, optimal_path):
    # Create a new graph
    G = nx.Graph()

    # Add edges with weights to the graph
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])

    # Define positions 
    pos = nx.spring_layout(G)

    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color="lightblue", font_weight="bold")

    # Color the edges of the path differently
    path_edges = [(optimal_path[i], optimal_path[i+1]) for i in range(len(optimal_path)-1)]
    path_edges += [(optimal_path[-1], optimal_path[0])]  # Connect last vertex to first to close the loop
    edge_colors = ['red' if edge in path_edges or edge[::-1] in path_edges else 'black' for edge in G.edges()]

    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color=edge_colors)

    # Add edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Label the starting vertex
    nx.draw_networkx_labels(G, pos, labels={optimal_path[0]: f'Start: {optimal_path[0]}'}, font_size=12, font_color='blue')

    plt.show()

def show_graph_optimal_path(optimal_path):
    # Create a new directed graph
    G = nx.DiGraph()

    # Add edges based on the optimal path
    for i in range(len(optimal_path)-1):
        G.add_edge(optimal_path[i], optimal_path[i+1])

    # Define positions for the nodes (optional)
    pos = nx.spring_layout(G)

    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color="lightblue", font_weight="bold")

    # Color the edges of the optimal path differently
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='red', arrows=True)

    # Label the starting vertex
    nx.draw_networkx_labels(G, pos, labels={optimal_path[0]: f'Start: {optimal_path[0]}'}, font_size=12, font_color='blue')

    plt.show()
def show_chart(show_result):
    x_values = list(show_result.keys())
    y_values = list(show_result.values())

    # Plotting the data
    plt.plot(x_values, y_values, marker='o', linestyle='-')
    plt.xlabel('Global Iteration Number')
    plt.ylabel('Global Shortest Path Length')
    plt.title('Global Shortest Path Length vs. Global Iteration Number')
    plt.grid(True)
    plt.show()
    
    

class Edge:
    def __init__(self, vertex1, vertex2):       
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.weight = 0
        self.pher_amt = 0
        self.prob = random.uniform(0.1, 0.2)
        
class Ant:
    def __init__(self, ant): #ant is a list
        self.name = ant
        self.curr_vertex = None
        self.visited_vertex = []
        self.edge_taken = []
           
class Vertex:
    def __init__(self, name):
        self.name = name
        self.neighbour = []


class Graph:
    def __init__(self):
        self.vertices = []  # a list of vertices object
        self.edges = []
  
    def add_vertex(self, ver): #vertex can be anything 
        v = Vertex(ver) #create a vertex object
        self.vertices.append(v)    #certices looks like [V.]

    def add_edge(self, vertex1, vertex2):
        if (vertex1 in self.vertices) and (vertex2 in self.vertices):
            edge1 = Edge(vertex1, vertex2)
            edge2 = Edge(vertex2, vertex1)
            self.edges.append(edge1)
            self.edges.append(edge2)
            vertex1.neighbour.append(vertex2)
            vertex2.neighbour.append(vertex1)

    def get_edge(self, vertex1, vertex2):
        for edge in self.edges:
            if (edge.vertex1 == vertex1 and edge.vertex2 == vertex2):
                return edge
        return "edges does not exist"
    

    def add_weight(self, edge, weight_val):
        edge.weight = weight_val # edge a -> b weight update, also have to update b -> a with same val
        edge2 = self.get_edge(edge.vertex2, edge.vertex1)  # get the edge b -> a
        edge2.weight = weight_val

    def calculate_tour_length(self, tour): #tour is list of vertex
        length = 0
        for i in range(len(tour) - 1):
            length += self.get_edge_weight(tour[i], tour[i + 1])
        return length  

    def get_edge_weight(self, vertex1, vertex2):
        for edge in self.edges:
            if (edge.vertex1 == vertex1 and edge.vertex2 == vertex2) or (edge.vertex1 == vertex2 and edge.vertex2 == vertex1):
                return edge.weight
        return float('inf')  
    
    def create_k_graph(self,edges):
        i=0
        for edge in edges:
            self.add_edge(self.vertices[edge[0]], self.vertices[edge[1]])
            self.add_weight(self.edges[i], edge[2])
            i+=2
        
    def calulate_prob(self, edge_to_take, alpha, beta):
        edge_visibility = 1/edge_to_take.weight
        numerator = (edge_to_take.pher_amt**alpha) * (edge_visibility**beta)

        summation_denominator = 0
        for edge in self.edges:
            e_visibility = 1/edge.weight
            summation_denominator += (edge.pher_amt**alpha) * (e_visibility**beta)
        
        transition_prob = numerator/summation_denominator
        return transition_prob
    

    def optmization(self, Q, alpha, beta , row, ants): #ants is a list of ant instance 
        shortest_path = None
        ant_taking_short_path = None
        all_paths_travelled_by_ants = {}
        shortest_path_length = float('inf')
        random_numbers = random.sample(range(len(ants)),len(ants)) #list of random nums; args depending on vertices
        
        #assign the starting vertex for the tour randomly
        for ant in ants:
            if random_numbers:
                random_index = random_numbers.pop()               
                curr_vertex = self.vertices[random_index]
                ant.visited_vertex.append(curr_vertex)
                ant.curr_vertex = curr_vertex
                
        for v in range(len(self.vertices)):       
            for ant in ants:
                curr_vertex = ant.curr_vertex  #get the current vertex so that we can get its neighbors and respective probalities of going to a neighbor
                vertex_to_go = None
                edge_to_take = None
                potential_edges = []
    
                for neighbour in curr_vertex.neighbour:    
                    if neighbour not in ant.visited_vertex: #if that town has not been visited
                        pot_edge = self.get_edge(ant.curr_vertex, neighbour) #get the edge between that neighbour and curr ver
                        potential_edges.append(pot_edge) 

                if potential_edges:
                    max_prob = potential_edges[0].prob
                    edge_to_take = potential_edges[0]
                    
                    for i in range(0,len(potential_edges)):
                        if potential_edges[i].prob >= max_prob:
                            max_prob = potential_edges[i].prob
                            edge_to_take = potential_edges[i]
                            vertex_to_go = potential_edges[i].vertex2 

                    ant.curr_vertex = vertex_to_go  
                    ant.visited_vertex.append(vertex_to_go)
                    visited_town_list = [ver.name for ver in ant.visited_vertex]
                    edge_to_take.pher_amt = row*edge_to_take.pher_amt + Q/edge_to_take.weight  #collect trail(pher amt) left by ant on that particular edge
                    edge_to_take.prob = self.calulate_prob(edge_to_take, alpha, beta) #change the prob of that edge after the ant has left trail (pher amt)

                
#                 else:
#                     print("ant ", ant.ant, " visited all vertex except back to its 1st starting vertex")

                
        # Checking if the current tour is shorter than the globally based shortest path
        for ant in ants:
            path_taken  = []
            
            #we have not added the starting vertex to the complete H. tour, so we add here
            first_vertex = None
            for i in range(len(ant.visited_vertex)):
                if i == 0:
                    first_vertex = ant.visited_vertex[i]
            ant.visited_vertex.append(first_vertex)

            #
            for verti in ant.visited_vertex:
                v_name = verti.name
                path_taken.append(v_name)
            
            #dictionary to store paths taken by each ant
            all_paths_travelled_by_ants[ant.name] = path_taken
            #tour length of each ant
            tour_length = self.calculate_tour_length(ant.visited_vertex) 

            #is that tour shortest of all found 
            if tour_length < shortest_path_length:
                shortest_path = ant.visited_vertex[:]
                shortest_path_length = tour_length
                ant_taking_short_path = ant.name

            ant.visited_vertex = [] #empty the tabu list
            ant.curr_vertex = None
            
        path = [v.name for v in shortest_path]

        return ant_taking_short_path, path, shortest_path_length, all_paths_travelled_by_ants
#         return all_paths_travelled_by_ants


graph = Graph()

for vertex_label in range(0,20):
    graph.add_vertex(vertex_label)
    
# Create a list of ants
ants = [Ant(i) for i in range(20)] 

# 4
# edges = [(0, 1, 4), (0, 2, 3), (0, 3, 3), 
#          (1, 2, 2), (1, 3, 2), 
#          (2, 3, 3)
#         ]


# K5
# edges = [
#     (0, 1, 10), (0, 2, 8), (0, 3, 7), (0, 4, 9),
#     (1, 2, 12), (1, 3, 8), (1, 4, 8),
#     (2, 3, 8), (2, 4, 13),
#     (3, 4, 4)
# ]

#k6
# edges = [
#     (0, 1, 10), (0, 2, 8), (0, 3, 7), (0, 4, 9), (0,5,4),
#     (1, 2, 12), (1, 3, 8), (1, 4, 8), (1,5,7),
#     (2, 3, 8), (2, 4, 13), (2,5,9),
#     (3, 4, 4), (3,5,5),
#     (4,5,4)
# ]

# k7
# edges = [(0, 1, 10), (0, 2, 14), (0, 3, 3), (0, 4, 5), (0, 5, 15), (0, 6, 20), 
#          (1, 2, 12), (1, 3, 8), (1, 4, 8), (1, 5, 7), (1, 6, 10), 
#          (2, 3, 18), (2, 4, 5), (2, 5, 9), (2, 6, 17), 
#          (3, 4, 12), (3, 5, 10), (3, 6, 11), 
#          (4, 5, 8), (4, 6, 14), 
#          (5, 6, 10)
#         ]

#k10
# edges = [
#     (0, 1, 11), (0, 2, 15), (0, 3, 14), (0, 4, 10), (0, 5, 6), (0, 6, 18), (0, 7, 14), (0, 8, 14), (0, 9, 10), 
#     (1, 2, 5), (1, 3, 8), (1, 4, 7), (1, 5, 13), (1, 6, 15), (1, 7, 7), (1, 8, 6), (1, 9, 4), 
#     (2, 3, 7), (2, 4, 20), (2, 5, 17), (2, 6, 4), (2, 7, 10), (2, 8, 15), (2, 9, 8), 
#     (3, 4, 17), (3, 5, 7), (3, 6, 9), (3, 7, 7), (3, 8, 18), (3, 9, 19), 
#     (4, 5, 6), (4, 6, 7), (4, 7, 13), (4, 8, 18), (4, 9, 16), 
#     (5, 6, 19), (5, 7, 7), (5, 8, 19), (5, 9, 13), 
#     (6, 7, 8), (6, 8, 4), (6, 9, 13), 
#     (7, 8, 5), (7, 9, 11), 
#     (8, 9, 16)
# ]

edges  = [(0, 1, 13), (0, 2, 10), (0, 3, 10), (0, 4, 9), (0, 5, 11), (0, 6, 12), (0, 7, 16), (0, 8, 6), (0, 9, 6), (0, 10, 19), (0, 11, 7), (0, 12, 12), (0, 13, 10), (0, 14, 6), 
          (1, 2, 9), (1, 3, 13), (1, 4, 19), (1, 5, 4), (1, 6, 4), (1, 7, 15), (1, 8, 16), (1, 9, 10), (1, 10, 7), (1, 11, 7), (1, 12, 17), (1, 13, 12), (1, 14, 12), 
          (2, 3, 19), (2, 4, 13), (2, 5, 8), (2, 6, 10), (2, 7, 17), (2, 8, 20), (2, 9, 9), (2, 10, 20), (2, 11, 12), (2, 12, 12), (2, 13, 14), (2, 14, 19), 
          (3, 4, 14), (3, 5, 6), (3, 6, 16), (3, 7, 5), (3, 8, 13), (3, 9, 12), (3, 10, 19), (3, 11, 4), (3, 12, 20), (3, 13, 20), (3, 14, 4), 
          (4, 5, 19), (4, 6, 17), (4, 7, 9), (4, 8, 8), (4, 9, 16), (4, 10, 19), (4, 11, 19), (4, 12, 6), (4, 13, 7), (4, 14, 11), 
          (5, 6, 11), (5, 7, 11), (5, 8, 18), (5, 9, 18), (5, 10, 14), (5, 11, 16), (5, 12, 14), (5, 13, 13), (5, 14, 10), 
          (6, 7, 7), (6, 8, 6), (6, 9, 19), (6, 10, 10), (6, 11, 5), (6, 12, 4), (6, 13, 14), (6, 14, 7), 
          (7, 8, 9), (7, 9, 6), (7, 10, 7), (7, 11, 16), (7, 12, 9), (7, 13, 7), (7, 14, 9), 
          (8, 9, 8), (8, 10, 12), (8, 11, 11), (8, 12, 9), (8, 13, 4), (8, 14, 16), 
          (9, 10, 20), (9, 11, 18), (9, 12, 15), (9, 13, 17), (9, 14, 19), 
          (10, 11, 11), (10, 12, 20), (10, 13, 17), (10, 14, 20), 
          (11, 12, 6), (11, 13, 15), (11, 14, 5), 
          (12, 13, 20), (12, 14, 15), 
          (13, 14, 20)
         ]

# edges = [(0, 1, 13), (0, 2, 15), (0, 3, 11), (0, 4, 15), (0, 5, 3), (0, 6, 4), (0, 7, 3), (0, 8, 15), (0, 9, 6), (0, 10, 10), (0, 11, 13), (0, 12, 12), (0, 13, 4), (0, 14, 14), (0, 15, 8), (0, 16, 7), (0, 17, 10), (0, 18, 8), (0, 19, 8), (0, 20, 4), (0, 21, 5), (0, 22, 9), (0, 23, 13), (0, 24, 9), (0, 25, 3), (0, 26, 14), (0, 27, 7), (0, 28, 6), (0, 29, 15), (1, 2, 6), (1, 3, 11), (1, 4, 4), (1, 5, 10), (1, 6, 13), (1, 7, 3), (1, 8, 4), (1, 9, 8), (1, 10, 6), (1, 11, 13), (1, 12, 5), (1, 13, 14), (1, 14, 12), (1, 15, 14), (1, 16, 15), (1, 17, 5), (1, 18, 14), (1, 19, 12), (1, 20, 12), (1, 21, 15), (1, 22, 3), (1, 23, 15), (1, 24, 6), (1, 25, 3), (1, 26, 15), (1, 27, 14), (1, 28, 9), (1, 29, 13), (2, 3, 11), (2, 4, 5), (2, 5, 12), (2, 6, 3), (2, 7, 6), (2, 8, 15), (2, 9, 12), (2, 10, 13), (2, 11, 6), (2, 12, 6), (2, 13, 6), (2, 14, 14), (2, 15, 8), (2, 16, 12), (2, 17, 11), (2, 18, 13), (2, 19, 12), (2, 20, 9), (2, 21, 10), (2, 22, 9), (2, 23, 13), (2, 24, 13), (2, 25, 3), (2, 26, 11), (2, 27, 13), (2, 28, 15), (2, 29, 3), (3, 4, 15), (3, 5, 7), (3, 6, 6), (3, 7, 4), (3, 8, 12), (3, 9, 10), (3, 10, 13), (3, 11, 12), (3, 12, 5), (3, 13, 7), (3, 14, 14), (3, 15, 4), (3, 16, 3), (3, 17, 15), (3, 18, 3), (3, 19, 5), (3, 20, 7), (3, 21, 3), (3, 22, 14), (3, 23, 4), (3, 24, 5), (3, 25, 9), (3, 26, 7), (3, 27, 12), (3, 28, 8), (3, 29, 10), (4, 5, 9), (4, 6, 4), (4, 7, 7), (4, 8, 3), (4, 9, 7), (4, 10, 5), (4, 11, 3), (4, 12, 10), (4, 13, 9), (4, 14, 10), (4, 15, 9), (4, 16, 14), (4, 17, 8), (4, 18, 15), (4, 19, 7), (4, 20, 10), (4, 21, 13), (4, 22, 5), (4, 23, 9), (4, 24, 11), (4, 25, 6), (4, 26, 5), (4, 27, 13), (4, 28, 9), (4, 29, 6), (5, 6, 9), (5, 7, 14), (5, 8, 9), (5, 9, 5), (5, 10, 13), (5, 11, 6), (5, 12, 7), (5, 13, 3), (5, 14, 14), (5, 15, 11), (5, 16, 6), (5, 17, 9), (5, 18, 6), (5, 19, 3), (5, 20, 5), (5, 21, 15), (5, 22, 6), (5, 23, 3), (5, 24, 15), (5, 25, 9), (5, 26, 4), (5, 27, 3), (5, 28, 3), (5, 29, 5), (6, 7, 3), (6, 8, 12), (6, 9, 14), (6, 10, 12), (6, 11, 13), (6, 12, 12), (6, 13, 7), (6, 14, 14), (6, 15, 3), (6, 16, 14), (6, 17, 15), (6, 18, 7), (6, 19, 5), (6, 20, 9), (6, 21, 6), (6, 22, 10), (6, 23, 15), (6, 24, 9), (6, 25, 14), (6, 26, 3), (6, 27, 13), (6, 28, 5), (6, 29, 12), (7, 8, 10), (7, 9, 5), (7, 10, 13), (7, 11, 6), (7, 12, 11), (7, 13, 12), (7, 14, 8), (7, 15, 5), (7, 16, 10), (7, 17, 15), (7, 18, 15), (7, 19, 14), (7, 20, 11), (7, 21, 4), (7, 22, 13), (7, 23, 10), (7, 24, 10), (7, 25, 4), (7, 26, 6), (7, 27, 14), (7, 28, 4), (7, 29, 14), (8, 9, 10), (8, 10, 3), (8, 11, 12), (8, 12, 9), (8, 13, 5), (8, 14, 15), (8, 15, 10), (8, 16, 10), (8, 17, 10), (8, 18, 12), (8, 19, 8), (8, 20, 8), (8, 21, 9), (8, 22, 6), (8, 23, 6), (8, 24, 5), (8, 25, 3), (8, 26, 12), (8, 27, 6), (8, 28, 14), (8, 29, 10), (9, 10, 5), (9, 11, 14), (9, 12, 8), (9, 13, 4), (9, 14, 9), (9, 15, 12), (9, 16, 4), (9, 17, 12), (9, 18, 8), (9, 19, 4), (9, 20, 6), (9, 21, 14), (9, 22, 8), (9, 23, 4), (9, 24, 11), (9, 25, 15), (9, 26, 3), (9, 27, 15), (9, 28, 8), (9, 29, 6), (10, 11, 15), (10, 12, 8), (10, 13, 5), (10, 14, 10), (10, 15, 7), (10, 16, 5), (10, 17, 12), (10, 18, 14), (10, 19, 14), (10, 20, 14), (10, 21, 14), (10, 22, 5), (10, 23, 5), (10, 24, 10), (10, 25, 13), (10, 26, 5), (10, 27, 12), (10, 28, 8), (10, 29, 3), (11, 12, 5), (11, 13, 12), (11, 14, 8), (11, 15, 5), (11, 16, 13), (11, 17, 9), (11, 18, 3), (11, 19, 5), (11, 20, 10), (11, 21, 12), (11, 22, 14), (11, 23, 13), (11, 24, 7), (11, 25, 4), (11, 26, 10), (11, 27, 13), (11, 28, 13), (11, 29, 3), (12, 13, 7), (12, 14, 8), (12, 15, 12), (12, 16, 6), (12, 17, 12), (12, 18, 15), (12, 19, 11), (12, 20, 7), (12, 21, 13), (12, 22, 3), (12, 23, 3), (12, 24, 11), (12, 25, 11), (12, 26, 13), (12, 27, 12), (12, 28, 12), (12, 29, 15), (13, 14, 4), (13, 15, 9), (13, 16, 12), (13, 17, 14), (13, 18, 9), (13, 19, 7), (13, 20, 11), (13, 21, 10), (13, 22, 15), (13, 23, 10), (13, 24, 13), (13, 25, 9), (13, 26, 10), (13, 27, 7), (13, 28, 10), (13, 29, 7), (14, 15, 12), (14, 16, 15), (14, 17, 7), (14, 18, 6), (14, 19, 11), (14, 20, 5), (14, 21, 12), (14, 22, 11), (14, 23, 15), (14, 24, 14), (14, 25, 7), (14, 26, 14), (14, 27, 9), (14, 28, 9), (14, 29, 3), (15, 16, 9), (15, 17, 15), (15, 18, 13), (15, 19, 8), (15, 20, 13), (15, 21, 12), (15, 22, 14), (15, 23, 14), (15, 24, 6), (15, 25, 12), (15, 26, 14), (15, 27, 13), (15, 28, 14), (15, 29, 7), (16, 17, 15), (16, 18, 9), (16, 19, 15), (16, 20, 8), (16, 21, 13), (16, 22, 13), (16, 23, 6), (16, 24, 3), (16, 25, 4), (16, 26, 5), (16, 27, 11), (16, 28, 9), (16, 29, 12), (17, 18, 9), (17, 19, 6), (17, 20, 13), (17, 21, 6), (17, 22, 7), (17, 23, 8), (17, 24, 10), (17, 25, 8), (17, 26, 4), (17, 27, 5), (17, 28, 13), (17, 29, 15), (18, 19, 8), (18, 20, 11), (18, 21, 4), (18, 22, 11), (18, 23, 15), (18, 24, 12), (18, 25, 3), (18, 26, 11), (18, 27, 8), (18, 28, 11), (18, 29, 4), (19, 20, 6), (19, 21, 6), (19, 22, 13), (19, 23, 7), (19, 24, 5), (19, 25, 15), (19, 26, 10), (19, 27, 9), (19, 28, 14), (19, 29, 10), (20, 21, 8), (20, 22, 3), (20, 23, 7), (20, 24, 14), (20, 25, 12), (20, 26, 5), (20, 27, 5), (20, 28, 12), (20, 29, 12), (21, 22, 12), (21, 23, 10), (21, 24, 11), (21, 25, 13), (21, 26, 12), (21, 27, 13), (21, 28, 15), (21, 29, 13), (22, 23, 6), (22, 24, 13), (22, 25, 13), (22, 26, 9), (22, 27, 9), (22, 28, 10), (22, 29, 7), (23, 24, 12), (23, 25, 8), (23, 26, 9), (23, 27, 5), (23, 28, 7), (23, 29, 5), (24, 25, 13), (24, 26, 10), (24, 27, 13), (24, 28, 4), (24, 29, 5), (25, 26, 9), (25, 27, 6), (25, 28, 15), (25, 29, 9), (26, 27, 15), (26, 28, 9), (26, 29, 5), (27, 28, 8), (27, 29, 9), (28, 29, 15)]

graph.create_k_graph(edges)    


global_shortest_path = None
global_ant_taking_short_path = None
global_all_paths_travelled_by_ants = {}
global_shortest_path_length = float('inf')
show_result = {}

# Run the optimization code for a certain number of iterations
for iteration in range(40):  # Adjust the number of iterations as needed
    Q = 100  # Pheromone constant (adjust as needed)
    alpha = 2  # Alpha parameter (adjust as needed)
    beta = 5   # Beta parameter (adjust as needed)
    row = 0.7

    # Run the optimization
   
    ant_taking_short_path, path, shortest_path_length, all_paths_travelled_by_ants = graph.optmization(Q, alpha, beta, row, ants)
    print("iter", iteration+1, ":", all_paths_travelled_by_ants, "shortest path: ", path , "shortest path length:", shortest_path_length, "\n")
    show_result[iteration] = global_shortest_path_length
    # Update global shortest path if a shorter path is found
    if shortest_path_length < global_shortest_path_length:
        global_shortest_path = path
        global_ant_taking_short_path = ant_taking_short_path
        global_shortest_path_length = shortest_path_length
        global_all_paths_travelled_by_ants = all_paths_travelled_by_ants
        global_iter_num = iteration+1
        

# Output the global shortest path and other relevant information
print("Global shortest path found by ant", global_ant_taking_short_path, ": ", global_shortest_path, "in ", global_iter_num, " iterations")
print("Length of global shortest path: ", global_shortest_path_length)
print()
print("\t\t Complete graph and optimal path")
show_graph(edges, global_shortest_path) 
print("\t\t Optimal path")
show_graph_optimal_path(global_shortest_path)

show_chart(show_result)
print(show_result)
