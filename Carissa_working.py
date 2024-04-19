# these ant are the dense ones

import random

antNames = ["Antony", "Marie Antoinette", "Tiny Dancer", "Leggy Larry", "Sir March-a-Lot", "Mini Muncher", "Houdini", "Napoleon", 
            "Six-Stepper","Micro McTiny"]

class Ant:
    def __init__(self, id):
        self.id = id
        self.name = random.choice(antNames)
        self.tabuList = []

    def __repr__(self):
        return (f"___________\n\n* Ant {self.id} *\nName: {self.name}\nTabu List: {self.tabuList}\n___________\n")

ants = []
for ant in range(10):
    ants += [Ant(ant)]

for a in ants: print(a)

