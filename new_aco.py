
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

    def calulate_prob(self, edge_to_take, alpha, beta):
        edge_visibility = 1/edge_to_take.weight
        numerator = (edge_to_take.pher_amt**alpha) * (edge_visibility**beta)

        summation_denominator = 0
        for edge in self.edges:
            e_visibility = 1/edge.weight
            summation_denominator += (edge.pher_amt**alpha) * (e_visibility**beta)
        
        transition_prob = numerator/summation_denominator
        return transition_prob
    

    def optmization(self, Q, alpha, beta , ants): #ants is a list of ant instance 
        shortest_path = None
        shortest_path_length = float('inf')
        random_numbers = random.sample(range(5), 5) #random nums depending on vertices

        for ant in ants:
            if random_numbers:
                random_index = random_numbers.pop()               
                curr_vertex = self.vertices[random_index]
                ant.visited_vertex.append(curr_vertex)
                ant.curr_vertex = curr_vertex
                # print(ant.ant, "curr vertex -> ", ant.curr_vertex, "visited vertex -> ", ant.visited_vertex[0].name)
        # for i in range(len(ants)):
        #     print(ants[i].ant, " -> The first town assigned ", ant.visited_vertex[i].name)

        for v in range(len(self.vertices)):       
            for ant in ants:
                curr_vertex = ant.curr_vertex  #get the current vertex so that we can get its neighbors and respective probalities of going to a neighbor
                vertex_to_go = None
                edge_to_take = None
                potential_edges = []


                print("--------------------------")
                print("ant: ",ant.ant, "current vertex -> ", curr_vertex.name)
                
        #         print(" before: ant visited vertex length -> ", len(ant.visited_vertex))
                for neighbour in curr_vertex.neighbour: #getting the neighbour town: thi    
                    if neighbour not in ant.visited_vertex: #if that town has not been visited
                        print(ant.ant, "current vertex:", curr_vertex.name,  " neighbours ", neighbour.name)
                        pot_edge = self.get_edge(ant.curr_vertex, neighbour)
                        # print(pot_edge)
                        potential_edges.append(pot_edge)

                if potential_edges:
                    print("potential edges len:", len(potential_edges))
                    max_prob = potential_edges[0].prob
                    edge_to_take = potential_edges[0]

                
                    for i in range(0,len(potential_edges)):
                        if potential_edges[i].prob >= max_prob:
                            max_prob = potential_edges[i].prob
                            edge_to_take = potential_edges[i]
                            vertex_to_go = potential_edges[i].vertex2 
                    print("max_prob ", max_prob, "edge to take ", edge_to_take.vertex2.name, vertex_to_go.name, "edge to take prob ", edge_to_take.prob)
                
                    ant.current_vertex = vertex_to_go  
                    print("current new vertex: ", ant.current_vertex.name)
        #         print("ant ", ant.ant, " curr vertex ->" ,ant.current_vertex.name)
                # visited_town_list = [ver.name for ver in ant.visited_vertex]
                # print(" before: ant visited vertex length -> ", len(ant.visited_vertex))
                
                    ant.visited_vertex.append(vertex_to_go) #since the vertex been visited add it to that ants visited_vertex list
                    edge_to_take.pher_amt = 0.5*edge_to_take.pher_amt + Q/edge_to_take.weight  #collect trail(pher amt) left by ant on that particular edge
                    edge_to_take.prob = self.calulate_prob(edge_to_take, alpha, beta) #change the prob of that edge after the ant has left trail (pher amt)

                
                else:
                    print("ant ", ant.ant, " visited all vertex expect back to its 1st starting vertex")

                
                # Checking if the current tour is shorter than the globally based shortest path
                tour_length = self.calculate_tour_length(ant.visited_vertex) # visited vertex is a list vertices
                if tour_length < shortest_path_length:
                    shortest_path = ant.visited_vertex[:]
                    shortest_path_length = tour_length
            
            path = [v.name for v in shortest_path]

        return path, shortest_path_length

graph = Graph()

for vertex_label in range(0, 5):
    graph.add_vertex(vertex_label)


graph.add_edge(graph.vertices[0], graph.vertices[1])
graph.add_weight(graph.edges[0], 10)
graph.add_edge(graph.vertices[0], graph.vertices[2])
graph.add_weight(graph.edges[2], 9)
# graph.add_edge(graph.vertices[0], graph.vertices[3])
graph.add_edge(graph.vertices[1], graph.vertices[2])
graph.add_weight(graph.edges[4], 4)
graph.add_edge(graph.vertices[1], graph.vertices[3])
graph.add_weight(graph.edges[6], 3)
graph.add_edge(graph.vertices[2], graph.vertices[4])
graph.add_weight(graph.edges[8], 8)
graph.add_edge(graph.vertices[3], graph.vertices[4])
graph.add_weight(graph.edges[10], 7)


# Create a list of ants
ants = [Ant(i) for i in range(5)] 


# # Perform optimization
# shortest_path, shortest_path_length = graph.optmization(Q=1, alpha=1, beta=1, ants=ants)
print()

print(graph.optmization(Q=1, alpha=1, beta=1, ants=ants))







            
                




                










