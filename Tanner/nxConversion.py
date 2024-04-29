import networkx as nx
import matplotlib.pyplot as plt
import random
import copy

antNames = ["Antony", "Marie Antoinette", "Tiny Dancer", "Leggy Larry", "Sir March-a-Lot", "Mini Muncher", "Houdini",
            "Napoleon", "Six-Stepper", "Micro McTiny", "Antonio", "Bryant", "Itsy Bitsy", "Queen of the Hill", "Sherlock Homeslice", "Buzz McKrill", "Colonel Crumb",
            "Count Crawly", "Pebble Crusher", "Lil' Pincers", "Mighty Mite", "Picasso the Pint-sized", "Scurry McHurry", "Sir Scuttle",
            "Daisy", "Sparkles", "Bitty", "Cupcake", "Button", "Cinnamon", "Pebbles", "Glimmer", "Sugar", "Tink", "Whiskers", "Velvet",
            "Skittles", "Twinkle", "Pippin", "Fluffy", "Dottie", "Sprinkles", "Pixel", "Sunny", "Asher", "Beckett", "Caden", "Dexter", 
            "Emory", "Finn", "Graham", "Holden", "Idris", "Jasper", "Kieran", "Leo", "Milo", "Nolan", "Otto", "Phoenix", "Quinn", "Ronan", 
            "Silas", "Tobin", "Amelia", "Bella", "Celeste", "Daphne", "Eliza", "Fiona", "Giselle", "Hazel", "Isla", "Juniper", "Kira", 
            "Luna", "Marigold", "Nova", "Opal", "Penelope", "Quinley", "Rosalyn", "Sadie", "Tessa", "Arianta", "Tanter", "Carissant"]

class Ant:
    def __init__(self, id):
        self.id = id
        self.name = random.choice(antNames)
        self.town = None
        self.tabuList = []

    def addTown(self, town):
        if town not in self.tabuList:
            self.town = town
            self.tabuList.append(town)
            print(f"{town} added to Ant {self.id} ({self.name}).")

    def getTown(self):
        return self.town

    def getTabuList(self):
        return self.tabuList
    
    def emptyTabuList(self):
        self.tabuList = []

    def __repr__(self):
        return (f"___________\n\n* Ant {self.id} *\nName: {self.name}\nTabu List: {self.tabuList}\n___________\n")

class AntGraph(nx.Graph):
    def __init__(self, colony=[]):
        super(AntGraph, self).__init__()
        # colony is a list of Ant objects
        self.colony = colony

    def add_edge(self, u_of_edge, v_of_edge,  **attr):
        super().add_edge(u_of_edge, v_of_edge, **attr)
        # adds a 
        self.edges[u_of_edge, v_of_edge]['pheremoneIntensity'] = '1'
        
    # code from aco, it has yet to be converted, some or most of it may have to be completely replaced, I am not yet sure, 
    # between colony and some of the additional things added by this just being a spicy networkx graph, a lot of it will
    # need to be reworked and/or can be done easier than it is currently being done, it's all currently pretty messy
        
    def calculate_prob(self, edge_to_take, alpha, beta):
        edge_visibility = 1 / edge_to_take.weight
        numerator = (edge_to_take.pher_amt ** alpha) * (edge_visibility ** beta)

        summation_denominator = 0
        for edge in self.edges:
            e_visibility = 1 / edge.weight
            summation_denominator += (edge.pher_amt ** alpha) * (e_visibility ** beta)

        transition_prob = numerator / summation_denominator
        return transition_prob

    def optimization(self, Q, alpha, beta, ants):  #ants is a list of ant instance
        shortest_path = None
        shortest_path_length = float('inf')
        shuffled_towns = copy.deepcopy(self.nodes)
        random.shuffle(shuffled_towns)

        # this loop sets an ant at each vertex at the start
        for ant in ants:
            if self.nodes:
                curr_vertex = shuffled_towns.pop()
                ant.addTown(curr_vertex)

        # the rest
        for v in range(len(self.nodes)):
            for ant in ants:
                curr_vertex = ant.getTown()  #get the current vertex so that we can get its neighbors and respective probalities of going to a neighbor

                greatest_prob = 0
                edge_to_take = None
                vertex_to_go = None
                potential_edges = []

                for neighbor in curr_vertex.neighbour:  #getting the neighbour town: thi
                    if neighbor not in ant.visited_vertex:  #if that town has not been visited
                        e = Edge(curr_vertex, neighbor)
                        potential_edges.append(e)
                    else:  #check this
                        e = Edge(curr_vertex, neighbor)
                        e.pher_amt = e.pher_amt + Q / e.weight  #collect trail(pher amt) left by ant on that particular edge
                        e.prob = self.calculate_prob(e, alpha,
                                                     beta)  #change the prob of that edge after the ant has left trail (pher amt)

                for edge in potential_edges:
                    if edge.prob > greatest_prob:
                        greatest_prob = edge.prob
                        edge_to_take = edge
                        vertex_to_go = edge.vertex2

                ant.current_vertex = vertex_to_go
                ant.visted_vertex.append(vertex_to_go)

                edge_to_take.pher_amt = 0.5 * edge_to_take.pher_amt + Q / edge_to_take.weight  #collect trail(pher amt) left by ant on that particular edge
                edge_to_take.prob = self.calculate_prob(edge_to_take, alpha,
                                                        beta)  #change the prob of that edge after the ant has left trail (pher amt)

                # Checking if the current tour is shorter than the globally based shortest path
                tour_length = self.calculate_tour_length(ant.visited_vertex)  # visited vertex is a list vertices
                if tour_length < shortest_path_length:
                    shortest_path = ant.visited_vertex[:]
                    shortest_path_length = tour_length
        
# G = nx.Graph()
G = AntGraph()

"""G.add_node('a', pheremoneIntensity=1)
G.add_node('b', pheremoneIntensity=1)
G.add_node('c', pheremoneIntensity=1)
G.add_node('d', pheremoneIntensity=1)"""

nodes = ['a', 'b', 'c', 'd']

for node in nodes:
    G.add_node(node)

"""edges = [['a', 'b', 1], ['a', 'c', 4], ['c', 'd', 4], ['b', 'd', 1]]

G.add_weighted_edges_from(edges)"""

G.add_edge(*['a', 'b'])

print(G.edges['a', 'b'])
    
nx.draw(G, with_labels = True)
plt.savefig("filename.png")

