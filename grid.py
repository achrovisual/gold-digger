from object import Object
from miner import Miner
import random

class Grid():
    def __init__(self, size):
        # Initialize the grid
        self.size = size
        self.grid = [["-" for i in range(self.size)] for i in range(self.size)]

        # Initialize objects
        self.miner = Miner("Miner", {"x": 1, "y": 1})
        self.gold = Object("Gold", {"x": random.randrange(1, self.size, 1), "y": random.randrange(1, self.size, 1)})
        self.pit = Object("Pit", {"x": random.randrange(1, self.size, 1), "y": random.randrange(1, self.size, 1)})
        self.beacon = Object("Beacon", {"x": random.randrange(1, self.size, 1), "y": random.randrange(1, self.size, 1)})

        # Update the grid
        self.update_grid(self.miner)
        self.update_grid(self.gold)
        self.update_grid(self.pit)
        self.update_grid(self.beacon)

    def update_grid(self, object):
        x = object.coordinates.get("x")
        y = object.coordinates.get("y")

        self.grid[x - 1][y - 1] = object.name[0]

    def show_grid(self):
        for row in self.grid:
            for element in row:
                print(element, end = "")
            print()
