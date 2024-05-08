
import random 
import copy

class Edge:
    def __init__(self, vertex1, vertex2):       
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.weight = 0
        self.pher_amt = 0
        self.prob = random.uniform(0.1, 0.2)
   
class Ant:
    def __init__(self, ant): #ant is a list
        self.ant = ant
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
    
    # def add_weight1(self, ver1, ver2, weight_val):
    #     if ver1
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
        random_numbers = random.sample(range(5), 5) #list of random nums; args depending on vertices

        for ant in ants:
            if random_numbers:
                random_index = random_numbers.pop()               
                curr_vertex = self.vertices[random_index]
                ant.visited_vertex.append(curr_vertex)
                ant.curr_vertex = curr_vertex
                # print("ant ", ant.ant, "curr vertex -> ", ant.curr_vertex.name, "visited vertex -> ", ant.visited_vertex[0].name)
        # for i in range(len(ants)):
        #     print(ants[i].ant, " -> The first town assigned ", ant.visited_vertex[i].name)

        for v in range(len(self.vertices)):       
            for ant in ants:
                curr_vertex = ant.curr_vertex  #get the current vertex so that we can get its neighbors and respective probalities of going to a neighbor
                vertex_to_go = None
                edge_to_take = None
                potential_edges = []


                # print("--------------------------") #testing 
                # print("ant: ",ant.ant, "current vertex -> ", curr_vertex.name) #test
                
        # #         print(" before: ant visited vertex length -> ", len(ant.visited_vertex))
                for neighbour in curr_vertex.neighbour: #getting the neighbour town: thi    
                    if neighbour not in ant.visited_vertex: #if that town has not been visited
                        # print("ant",ant.ant, "current vertex:", curr_vertex.name,  " neighbours ", neighbour.name) #test
                        pot_edge = self.get_edge(ant.curr_vertex, neighbour)
        #                 # print(pot_edge)
                        potential_edges.append(pot_edge)

                if potential_edges:
                    # print("ant",ant.ant,"potential edges len:", len(potential_edges))
                    max_prob = potential_edges[0].prob
                    edge_to_take = potential_edges[0]
                    # print(edge_to_take.vertex2.name, "with prob", max_prob)

                
                    for i in range(0,len(potential_edges)):
                        if potential_edges[i].prob >= max_prob:
                            max_prob = potential_edges[i].prob
                            edge_to_take = potential_edges[i]
                            vertex_to_go = potential_edges[i].vertex2 
                    # print("max_prob ", max_prob, "edge to take ", edge_to_take.vertex2.name, vertex_to_go.name, "edge to take prob ", edge_to_take.prob)
                
                    ant.curr_vertex = vertex_to_go  
                    # print("new current vertex: ", ant.curr_vertex.name)
        # #         print("ant ", ant.ant, " curr vertex ->" ,ant.current_vertex.name)
                    ant.visited_vertex.append(vertex_to_go)
                    visited_town_list = [ver.name for ver in ant.visited_vertex]
                    # print(visited_town_list)
                    # print(" before: ant visited svertex length -> ", len(ant.visited_vertex))
                
                     #since the vertex been visited add it to that ants visited_vertex list
                    # print(" before: ant visited vertex length -> ", len(ant.visited_vertex))
                # print()
                    edge_to_take.pher_amt = row*edge_to_take.pher_amt + Q/edge_to_take.weight  #collect trail(pher amt) left by ant on that particular edge
                    edge_to_take.prob = self.calulate_prob(edge_to_take, alpha, beta) #change the prob of that edge after the ant has left trail (pher amt)

                
                else:
                    print("ant ", ant.ant, " visited all vertex except back to its 1st starting vertex")

                
        #         # Checking if the current tour is shorter than the globally based shortest path

        for ant in ants:
            path_taken  = []
            first_vertex = None
            for i in range(len(ant.visited_vertex)):
                if i == 0:
                    first_vertex = ant.visited_vertex[i]
            ant.visited_vertex.append(first_vertex)

            for verti in ant.visited_vertex:
                v_name = verti.name
                path_taken.append(v_name)

            all_paths_travelled_by_ants[ant.ant] = path_taken
            tour_length = self.calculate_tour_length(ant.visited_vertex) # visited vertex is a list vertices
            if tour_length < shortest_path_length:
                shortest_path = ant.visited_vertex[:]
                shortest_path_length = tour_length
                ant_taking_short_path = ant.ant

            ant.visited_vertex = []
            ant.curr_vertex = None
            
        path = [v.name for v in shortest_path]

        return ant_taking_short_path, path, shortest_path_length, all_paths_travelled_by_ants


graph = Graph()

for vertex_label in range(0, 5):
    graph.add_vertex(vertex_label)


graph.add_edge(graph.vertices[0], graph.vertices[1])
graph.add_weight(graph.edges[0], 10)
graph.add_edge(graph.vertices[0], graph.vertices[2])
graph.add_weight(graph.edges[2], 8)
graph.add_edge(graph.vertices[0], graph.vertices[3])
graph.add_weight(graph.edges[4], 7)
graph.add_edge(graph.vertices[0], graph.vertices[4])
graph.add_weight(graph.edges[6], 9)

# graph.add_edge(graph.vertices[0], graph.vertices[3])

graph.add_edge(graph.vertices[1], graph.vertices[2])
graph.add_weight(graph.edges[8], 6)
graph.add_edge(graph.vertices[1], graph.vertices[3])
graph.add_weight(graph.edges[10], 4)
graph.add_edge(graph.vertices[1], graph.vertices[4])
graph.add_weight(graph.edges[12], 7)

graph.add_edge(graph.vertices[2], graph.vertices[3])
graph.add_weight(graph.edges[14], 8)
graph.add_edge(graph.vertices[2], graph.vertices[4])
graph.add_weight(graph.edges[16], 8)

graph.add_edge(graph.vertices[3], graph.vertices[4])
graph.add_weight(graph.edges[18], 6)

# Create a list of ants
ants = [Ant(i) for i in range(5)] 

global_shortest_path = None
global_ant_taking_short_path = None
global_all_paths_travelled_by_ants = {}
global_shortest_path_length = float('inf')

# Run the optimization code for a certain number of iterations
for iteration in range(10):  # Adjust the number of iterations as needed
    Q = 100  # Pheromone constant (adjust as needed)
    alpha = 2  # Alpha parameter (adjust as needed)  
    beta = 5   # Beta parameter (adjust as needed)
    row = 0.7

    # Run the optimization
    ant_taking_short_path, path, shortest_path_length, all_paths_travelled_by_ants = graph.optmization(Q, alpha, beta, row, ants)

    # Update global shortest path if a shorter path is found
    if shortest_path_length < global_shortest_path_length:
        global_shortest_path = path
        global_ant_taking_short_path = ant_taking_short_path
        global_shortest_path_length = shortest_path_length
        global_all_paths_travelled_by_ants = all_paths_travelled_by_ants

# Output the global shortest path and other relevant information
print("Global shortest path found by ant", global_ant_taking_short_path, ": ", global_shortest_path)
print("Length of global shortest path: ", global_shortest_path_length)
# print("All paths travelled by ants:")
# for ant_id, path_taken in global_all_paths_travelled_by_ants.items():
#     print("Ant", ant_id, ":", path_taken)


















            
                




                
