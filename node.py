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
        self.scannedNull = False 
        self.scannedPit = False
        self.scannedBeacon = False

        self.reachedEdge = False
        self.moveToNull = False
    
    def setBeacon(self, value):
        self.scannedBeacon = value
    def setCost(self, cost):
        self.cost = int(cost)
    
    def setEdge(self, value):
        self.reachedEdge = value

    def setScanned(self, value):
        self.scannedFront = value
        
    def setGold(self, value):
        self.scannedGold = value

    def setNull(self, value):
        self.scannedNull = value

    def setPit(self, value):
        self.scannedPit = value
    
    def moveToNullBeacon(self, value):
        self.moveToNull = value