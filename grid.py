from object import Object
from miner import Miner
import random

class Grid():
    def __init__(self, size):
        # Initialize the grid
        self.size = size
        self.grid = [["-" for i in range(self.size)] for i in range(self.size)]

        # Initialize objects
        self.miner = Miner("Miner", {"x": 0, "y": 0}, self.size)
        self.gold = Object("Gold", {"x": random.randrange(0, self.size, 1), "y": random.randrange(0, self.size, 1)})
        self.pit = Object("Pit", {"x": random.randrange(0, self.size, 1), "y": random.randrange(0, self.size, 1)})
        self.beacon = Object("Beacon", {"x": random.randrange(0, self.size, 1), "y": random.randrange(0, self.size, 1)})

        # Update the grid
        self.update_grid(self.miner)
        self.update_grid(self.gold)
        self.update_grid(self.pit)
        self.update_grid(self.beacon)

    def update_grid(self, object):
        x = object.coordinates.get("x")
        y = object.coordinates.get("y")

        self.grid[x][y] = object.name[0]

    def show_grid(self):
        # Update the grid
        self.grid = [["-" for i in range(self.size)] for i in range(self.size)]
        self.update_grid(self.miner)
        self.update_grid(self.gold)
        self.update_grid(self.pit)
        self.update_grid(self.beacon)


        for row in self.grid:
            for element in row:
                print(element, end = "")
            print()

    def scan(self):
        miner_location = self.miner.coordinates
        miner_compass = self.miner.compass
        iterator = 0
        anchor_value = 0
        return_value = ''

        #lateral movement
        if miner_compass == 'east':
            iterator = int(miner_location['y'])
            anchor_value = int(miner_location['x'])

            while iterator < self.size and (return_value != 'B' or return_value != 'P'):
                if self.grid[anchor_value][iterator] == 'B':
                    return_value = 'B'
                elif self.grid[anchor_value][iterator] == 'G':
                    return_value = 'G'
                elif self.grid[anchor_value][iterator] == 'P':
                    return_value = 'P'
                iterator += 1

        elif miner_compass == 'west':
            iterator = int(miner_location['y'])
            anchor_value = int(miner_location['x'])

            while iterator >= 0 and (return_value != 'B' or return_value != 'P'):
                if self.grid[anchor_value][iterator] == 'B':
                    return_value = 'B'
                elif self.grid[anchor_value][iterator] == 'G':
                    return_value = 'G'
                elif self.grid[anchor_value][iterator] == 'P':
                    return_value = 'P'
                iterator -= 1

        #longitudinal movement
        elif miner_compass == 'south':
            iterator = int(miner_location['x'])
            anchor_value = int(miner_location['y'])

            while iterator < self.size and (return_value != 'B' or return_value != 'P'):
                if self.grid[iterator][anchor_value] == 'B':
                    return_value = 'B'
                elif self.grid[iterator][anchor_value] == 'G':
                    return_value = 'G'
                elif self.grid[iterator][anchor_value] == 'P':
                    return_value = 'P'
                iterator += 1

        elif miner_compass == 'north':
            iterator = int(miner_location['x'])
            anchor_value = int(miner_location['y'])

            while iterator >= 0 and (return_value != 'B' or return_value != 'P'):
                if self.grid[iterator][anchor_value] == 'B':
                    return_value = 'B'
                elif self.grid[iterator][anchor_value] == 'G':
                    return_value = 'G'
                elif self.grid[iterator][anchor_value] == 'P':
                    return_value = 'P'
                iterator -= 1
        else:
            return False

        self.miner.scan(return_value)
        return True

    def check(self):
        miner_location = self.miner.coordinates

        if self.miner.compass == "east" or self.miner.compass == "west":
            x  = int(miner_location['x'])
            y = int(miner_location['y']) + 1
        else:
            x  = int(miner_location['x']) + 1
            y = int(miner_location['y'])

        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return "out"

        if self.grid[x][y] == 'B':
            return "beacon"
        elif self.grid[x][y] == 'P':
            return "pit"
        elif self.grid[x][y] == 'G':
            return "gold"
        else:
            return "null"
    
    def smartScan(self):
        miner_location = self.miner.coordinates
        miner_compass = self.miner.compass
        iterator = 0
        anchor_value = 0
        return_value = ''

        #lateral movement
        if miner_compass == 'east':
            iterator = int(miner_location['y'])
            anchor_value = int(miner_location['x'])

            while iterator < self.size and (return_value != 'B' or return_value != 'P'):
                if self.grid[anchor_value][iterator] == 'B':
                    return_value = 'B'
                elif self.grid[anchor_value][iterator] == 'G':
                    return_value = 'G'
                elif self.grid[anchor_value][iterator] == 'P':
                    return_value = 'P'
                iterator += 1

        elif miner_compass == 'west':
            iterator = int(miner_location['y'])
            anchor_value = int(miner_location['x'])

            while iterator >= 0 and (return_value != 'B' or return_value != 'P'):
                if self.grid[anchor_value][iterator] == 'B':
                    return_value = 'B'
                elif self.grid[anchor_value][iterator] == 'G':
                    return_value = 'G'
                elif self.grid[anchor_value][iterator] == 'P':
                    return_value = 'P'
                iterator -= 1

        #longitudinal movement
        elif miner_compass == 'south':
            iterator = int(miner_location['x'])
            anchor_value = int(miner_location['y'])

            while iterator < self.size and (return_value != 'B' or return_value != 'P'):
                if self.grid[iterator][anchor_value] == 'B':
                    return_value = 'B'
                elif self.grid[iterator][anchor_value] == 'G':
                    return_value = 'G'
                elif self.grid[iterator][anchor_value] == 'P':
                    return_value = 'P'
                iterator += 1

        elif miner_compass == 'north':
            iterator = int(miner_location['x'])
            anchor_value = int(miner_location['y'])

            while iterator >= 0 and (return_value != 'B' or return_value != 'P'):
                if self.grid[iterator][anchor_value] == 'B':
                    return_value = 'B'
                elif self.grid[iterator][anchor_value] == 'G':
                    return_value = 'G'
                elif self.grid[iterator][anchor_value] == 'P':
                    return_value = 'P'
                iterator -= 1
        else:
            return return_value

        return return_value