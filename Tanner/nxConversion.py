
import random 
import copy

antNames = ["Antony", "Marie Antoinette", "Tiny Dancer", "Leggy Larry", "Sir March-a-Lot", "Mini Muncher", "Houdini",
            "Napoleon", "Six-Stepper", "Micro McTiny", "Antonio", "Bryant", "Itsy Bitsy", "Queen of the Hill",
            "Sherlock Homeslice", "Buzz McKrill", "Colonel Crumb", "Count Crawly", "Pebble Crusher", "Lil' Pincers",
            "Mighty Mite", "Picasso the Pint-sized", "Scurry McHurry", "Sir Scuttle", "Daisy", "Sparkles", "Bitty",
            "Cupcake", "Button", "Cinnamon", "Pebbles", "Glimmer", "Sugar", "Tink", "Whiskers", "Velvet", "Skittles",
            "Twinkle", "Pippin", "Fluffy", "Dottie", "Sprinkles", "Pixel", "Sunny", "Asher", "Beckett", "Caden",
            "Dexter", "Emory", "Finn", "Graham", "Holden", "Idris", "Jasper", "Kieran", "Leo", "Milo", "Nolan", "Otto",
            "Phoenix", "Quinn", "Ronan", "Silas", "Tobin", "Amelia", "Bella", "Celeste", "Daphne", "Eliza", "Fiona",
            "Giselle", "Hazel", "Isla", "Juniper", "Kira", "Luna", "Marigold", "Nova", "Opal", "Penelope", "Quinley",
            "Rosalyn", "Sadie", "Tessa", "Arianta", "Tanter", "Carissant", "Krishnant"]

class Edge:
    def __init__(self, vertex1, vertex2):       
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.weight = 0
        self.pherAmt = 0
        self.prob = 0
        
    def __repr__(self):
        return f"[{self.vertex1}, {self.vertex2}]"
    
"""class Ant:
    def __init__(self, ant): #ant is a list
        self.ant = ant
        self.curr_vertex = None
        self.visted_vertex = []"""
        
class Ant:
    def __init__(self, ant):
        self.ant = ant
        self.name = random.choice(antNames)
        self.currVertex = None
        self.tabuList = []

    def addTown(self, town):
        if town not in self.tabuList:
            self.tabuList.append(town)
            print(f"{town} added to Ant {self.id} ({self.name}).")

    def getTabuList(self):
        return self.tabuList
    
    def emptyTabuList(self):
        self.tabuList = []

    def __repr__(self):
        return (f"___________\n\n* Ant {self.id} *\nName: {self.name}\nTabu List: {self.tabuList}\n___________\n")
           
class Vertex:
    def __init__(self, vertex):
        self.vertex = vertex
        self.neighbour = []
        
    def getVertex(self):
        return self.vertex
        
    def __repr__(self):
        return f"{self.vertex}"

        
class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        
    def __repr__(self):
        return f"Vertices: {self.vertices}\nedges: {self.edges}"
  
    def getVertices(self):
        return self.vertices
  
    def addVertex(self, vertex):
        v = Vertex(vertex)
        self.vertices.append(v)
        
    def addEdges(self):
        return self.edges

    def addEdge(self, vertex1, vertex2):
        v1 = None
        v2 = None
        
        for vertex in self.vertices:
            if vertex.get_vertex() == vertex1:
                v1 = vertex
            elif vertex.get_vertex() == vertex2:
                v2 = vertex
        
        if vertex1 and vertex2:
            edge1 = Edge(v1, v2)
            self.edges.append(edge1)
            v1.neighbour.append(v2)
            v2.neighbour.append(v1)
            
    def getEdges(self):
        edges = []
        
        for edge in self.edges:
            edges.append(edge)
        
        return edges
        
    def addWeight(self, vertex1, vertex2, weight):
        edge = Edge(vertex1, vertex2)
        if edge in self.edges:
            edge.weight = weight

    def updateProb(self, vertex1, vertex2, probVal):
        edge = Edge(vertex1, vertex2)
        if edge in self.edges:
            edge.prob = probVal

    def addPhermone(self, vertex1, vertex2, phermoneAmt):
        edge = Edge(vertex1, vertex2)
        if edge in self.edges:
            edge.pherAmt = phermoneAmt

    def calulateProb(self, edgeToTake, alpha, beta):
        edgeVisibility = 1/edgeToTake.weight
        numerator = (edgeToTake.pher_amt**alpha) * (edgeVisibility**beta)

        summationDenominator = 0
        for edge in self.edges:
            eVisibility = 1/edge.weight
            summationDenominator += (edge.pher_amt**alpha) * (eVisibility**beta)
        
        transitionProb = numerator/summationDenominator
        return transitionProb
    

    def optmization(self, Q, alpha, beta , ants): #ants is a list of ant instance 
        shortestPath = []
        shuffledTowns = copy.deepcopy(self.vertices)
        random.shuffle(shuffledTowns)

        for ant in ants:
            if self.vertices:
                currVertex = shuffledTowns.pop()
                ant.tabu_list.append(currVertex) 
                ant.curr_vertex = currVertex 

        for v in range(len(self.vertices)):
            for ant in ants:
                currVertex = ant.currVertex  #get the current vertex so that we can get its neighbors and respective probalities of going to a neighbor
            
                greatestProb = 0
                edgeToTake = None
                vertexToGo = None
                potentialEdges = []

                for neighbor in currVertex.neighbour: #getting the neighbour town: thi
                    if neighbor not in ant.visited_vertex: #if that town has not been visited
                        e = Edge(currVertex, neighbor)
                        potentialEdges.append(e)
                    else: #check this
                        e = Edge(currVertex, neighbor)
                        e.pherAmt = edgeToTake.pherAmt + Q/edgeToTake.weight  #collect trail(pher amt) left by ant on that particular edge
                        edgeToTake.prob = self.calulateProb(e, alpha, beta) #change the prob of that edge after the ant has left trail (pher amt)
           
                for edge in potentialEdges:
                    if edge.prob > greatestProb:
                        greatestProb = edge.prob
                        edgeToTake = edge
                        vertexToGo = edge.vertex2

                ant.currentTown = vertexToGo
                ant.tabuList.append(vertexToGo)
                ant.addTown(vertexToGo)


                edgeToTake.pherAmt = 0.5*edgeToTake.pherAmt + Q/edgeToTake.weight  #collect trail(pher amt) left by ant on that particular edge
                edgeToTake.prob = self.calulate_prob(edgeToTake, alpha, beta) #change the prob of that edge after the ant has left trail (pher amt)
                
def graphTraveral(graph, startNode):
    possibleCities = graph.get_vertices()
    paths = graph.get_edges()
    
    

testVertices = ["a", "b", "c", "d"]
testEdges = [["a", 'b'], ["a", "c"], ["b", "d"], ["c", "d"]]

testGraph = Graph()  

for i in testVertices:
    testGraph.add_vertex(i)
    
for i in testEdges:
    testGraph.add_edge(i[0], i[1])

print(testGraph)
