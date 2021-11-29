from agent import Agent
from node import Node
from grid import Grid

class gbfs(Agent):
    def __init__(self, grid):
        self.grid = grid
        self.start()

    def start(self):
        solving = True
        solvable = False

        # Initialize tree
        miner_location = self.grid.miner.coordinates
        x  = int(miner_location["x"])
        y = int(miner_location["y"])
        miner_compass = self.grid.miner.compass

        #establish heuristic values
        heurVal = {
            'notScanned': 0, #haven't scanned the front yet
            'alreadyScanned': 5, #already scanned the front, do we really want to scan again?
            'rotateAwayNull': 1, #scan returned null, do we rotate?
            'rotateAwayPit': 0, #avoid at all cost
            'rotateAwayBeacon': 1, #nope
            'rotateAwayEdge': 0, #reached the edge
            'moveToScannedGold': -1, #scan returned gold, let's go!
            'moveToScannedPit': 10, #JUST DON'T
            'moveToNullBeacon': 0, #move if scan returned null
            'movedAfterNull' : 2 #already moved after scan ret null
        }

        root = Node(None, x, y, miner_compass, None, None)
        root.set_cost(0)
        root.setScanned(False)
        root.setGold(False)
        openList = []
        closedList = []

        openList.append(root)

        goalNode = None
        inGold = False

        while openList and not inGold:
            currentNode = openList.pop()
            currFront = currentNode.front
            currX = currentNode.x
            currY = currentNode.y
            currAction = currentNode.actions
            scannedFront = currentNode.scannedFront
            #deploy actions here
            checkCurrTile = self.grid.check()
            
            
            if not currentNode.scannedGold:
                if checkCurrTile != 'gold' or checkCurrTile != 'pit':
                    pass
                elif checkCurrTile == 'gold':
                    inGold = True
            else: #we found the goal node, our only option is to move forward
                pass
            
            closedList.append(currentNode)