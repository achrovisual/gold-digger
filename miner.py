from object import Object

class Miner(Object):
    def __init__(self, name, coordinates):
        self.name = "Miner"
        self.coordinates = {"x": 1, "y": 1}
        self.compass = "east"
        self.scanned = None
    def move(self):
        # Update coordinates here
        if self.compass == 'east': #add a condition that not at the edge of the map
            self.coordinates['x']+=1
        elif self.compass=='north' and self.coordinates['y'] != 1:
            self.coordinates['y']-=1
        elif self.compass=='south': #add a condition that not at the edge of the map
            self.coordinates['y']+=1
        elif self.compass=='west' and self.coordinates['x'] != 1:
            self.coordinates['x']-=1

    def rotate(self):
        # Update compass here
        if self.compass == 'north':
            self.compass = 'east'
        elif self.compass == 'east':
            self.compass = 'south'
        elif self.compass == 'south':
            self.compass = 'west'
        elif self.compass == 'west':
            self.compass = 'north'

    def scan(self):
        # Update scanned here
        returner = None

        #visit front of miner
        
    def check():
        # Check if current block is goal
        pass
