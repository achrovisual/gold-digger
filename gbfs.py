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
            'scan': 0,
            'move': 1,
            'rotate': 1
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
            min = 0

            #priority queueing
            for index in range(0, len(openList)):
                if openList[index].cost < openList.cost:
                    min = index
            
            currentNode = openList.pop(min)
            currFront = currentNode.front
            currX = currentNode.x
            currY = currentNode.y
            currAction = currentNode.actions
            scannedFront = currentNode.scannedFront

            checkCurrTile = self.grid.check()
            #deploy actions here
            
            if not currentNode.scannedGold:
                if checkCurrTile != 'gold' or checkCurrTile != 'pit':
                    pass
            else: #we found the goal node, our only option is to move forward
                ##################################### MOVE NODE ################################################
                #generate child node
                newNode= Node(None, self.grid.miner.coordinates['x'], self.grid.miner.coordinates['y'], self.grid.miner.compass, "move", currentNode)
                #set chlid node cost
                newNode.set_cost(heurVal['move'])
                #set child to scanned
                newNode.setScanned(True)
                #set child node to scanned gold
                newNode.setGold(True)
                #append to open list
                openList.append(newNode)
            
            closedList.append(currentNode)