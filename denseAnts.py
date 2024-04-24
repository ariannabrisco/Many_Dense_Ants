# these ant are the dense ones

import random
import networkx as nx
import matplotlib.pyplot as plt

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
        self.tabuList = []

    def __repr__(self):
        return (f"___________\n\n* Ant {self.id} *\nName: {self.name}\nTabu List: {self.tabuList}\n___________\n")


   
G = nx.Graph()

edges = [["a", "b", 1], ["a", "c", 4], ["c", "d", 4], ["b", "d", 1]]

G.add_weighted_edges_from(edges)

nx.draw(G, with_labels = True)
plt.savefig("filename.png")
