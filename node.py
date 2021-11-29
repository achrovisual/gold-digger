class Node():
    def __init__(self, id, x, y, front, actions, parent):
        self.id = id
        self.x = x
        self.y = y
        self.front = front
        self.actions = actions
        self.parent = parent
        self.cost = None
        self.scannedFront = False #we use this value to ensure that we only scan once in the direction we're facing
        self.scannedGold = False

    def set_cost(self, cost):
        self.cost = int(cost)
    
    def setScanned(self, value):
        self.scannedFront = value
        
    def setGold(self, value):
        self.scannedGold = value