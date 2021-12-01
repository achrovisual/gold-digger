from object import Object

class Miner(Object):
    def __init__(self, name, coordinates, size):
        self.name = name
        self.coordinates = coordinates
        self.compass = "east"
        self.scanned = None
        self.size = size
        self.actions = [0, 0, 0] # move, rotate, scan

    def move(self):
        # Update coordinates here
        self.actions[0] += 1
        if self.compass == 'east' and self.coordinates['x'] + 1 <= self.size - 1: #add a condition that not at the edge of the map
            self.coordinates['x'] += 1
            return True
        elif self.compass=='north' and self.coordinates['y'] - 1 >= 0:
            self.coordinates['y'] -= 1
            return True
        elif self.compass=='west' and self.coordinates['x'] - 1 >= 0:
            self.coordinates['x'] -= 1
            return True
        elif self.compass=='south' and self.coordinates['y'] + 1 <= self.size - 1: #add a condition that not at the edge of the map
            self.coordinates['y'] += 1
            return True
        else:
            # print('reached edge')
            return False

    def rotate(self):
        # Update compass here
        self.actions[1] += 1
        if self.compass == 'north':
            self.compass = 'east'
            return True
        elif self.compass == 'east':
            self.compass = 'south'
            return True
        elif self.compass == 'south':
            self.compass = 'west'
            return True
        elif self.compass == 'west':
            self.compass = 'north'
            return True
        return False

    def scan(self, result):
        # Update scanned here
        self.scanned = result
        self.actions[2] += 1
        #perform decision here
        #if self.gridScanRetVal == <X>, then <Y>
