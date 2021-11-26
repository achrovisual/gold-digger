from object import Object
from miner import Miner
import random

class Grid():
    def __init__(self, size):
        # Initialize the grid
        self.size = size
        self.grid = [["-" for i in range(self.size)] for i in range(self.size)]

        # Initialize objects
        self.miner = Miner("Miner", {"x": 1, "y": 1}, self.size)
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
            
    def scanMinerFront(self):
        minerLoc = self.miner.coordinates
        minerCompass = self.miner.compass
        iterator = 0
        anchorVal = 0
        retVal = ''

        #lateral movement
        if minerCompass == 'east':
            iterator = int(minerLoc['y'])
            anchorVal = int(minerLoc['x']) - 1

            while iterator < self.size and (retVal != 'B' or retVal != 'P'):
                if self.grid[anchorVal][iterator] == 'B':
                    retVal = 'B'
                elif self.grid[anchorVal][iterator] == 'G':
                    retVal = 'G'
                elif self.grid[anchorVal][iterator] == 'P':
                    retVal = 'P'
                iterator+=1

        if minerCompass == 'west':
            iterator = int(minerLoc['y']) - 2
            anchorVal = int(minerLoc['x']) - 1

            while iterator > 0 and (retVal != 'B' or retVal != 'P'):
                if self.grid[anchorVal][iterator] == 'B':
                    retVal = 'B'
                elif self.grid[anchorVal][iterator] == 'G':
                    retVal = 'G'
                elif self.grid[anchorVal][iterator] == 'P':
                    retVal = 'P'
                iterator-=1
        
        #longitudinal movement
        if minerCompass == 'south':
            iterator = int(minerLoc['x'])
            anchorVal = int(minerLoc['y']) - 1

            while iterator < self.size and (retVal != 'B' or retVal != 'P'):
                if self.grid[iterator][anchorVal] == 'B':
                    retVal = 'B'
                elif self.grid[iterator][anchorVal] == 'G':
                    retVal = 'G'
                elif self.grid[iterator][anchorVal] == 'P':
                    retVal = 'P'
                iterator+=1        
        
        if minerCompass == 'north':
            iterator = int(minerLoc['x']) - 2
            anchorVal = int(minerLoc['y']) - 1

            while iterator < self.size and (retVal != 'B' or retVal != 'P'):
                if self.grid[iterator][anchorVal] == 'B':
                    retVal = 'B'
                elif self.grid[iterator][anchorVal] == 'G':
                    retVal = 'G'
                elif self.grid[iterator][anchorVal] == 'P':
                    retVal = 'P'
                iterator-=1     
        
        self.miner.scanRes(retVal)
    
    def checkCurrPos(self):
        minerLoc = self.miner.coordinates
        xPos = int(minerLoc['x']) - 1
        yPos = int(minerLoc['y']) - 1

        if self.grid[xPos][yPos] == 'B':
            print("Beacon found: <x> squares to goal")
        elif self.grid[xPos][yPos] == 'P':
            print("ded")
        elif self.grid[xPos][yPos] == 'G':
            print("Congratulations! You won!")
        
