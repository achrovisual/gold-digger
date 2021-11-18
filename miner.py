from object import Object

class Miner(Object):
    def __init__(self, name, coordinates):
        self.name = "Miner"
        self.coordinates = {"x": 1, "y": 1}
        self.compass = "east"
        self.scanned = None
    def move(self):
        # Update coordinates here
        pass
    def rotate(self):
        # Update compass here
        pass
    def scan(self):
        # Update scanned here
        pass
    def check():
        # Check if current block is goa
        pass
