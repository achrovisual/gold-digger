from agent import Agent
from grid import Grid
from node import Node
import copy

class astar(Agent):
    def __init__(self, grid):
        self.grid = grid
        self.start()

    def start(self):
        # Initialize tree
        miner_location = self.grid.miner.coordinates
        x  = int(miner_location["x"])
        y = int(miner_location["y"])
        miner_compass = self.grid.miner.compass
        actions = []
        actions2 = []

        root = Node(None, x, y, miner_compass, None, None)

        root.set_cost(0)

        # Initialize node lists
        openList = [] #unexamined nodes
        closedList = [] #examined nodes
        openList.append(root)

        moveList = []
        #heuristic values

        heurVal = {
            'move': 1,
            'rotate': 2, #we make rotate expensive in the worst-case that upon scan, we found a pit
            'scan': -1,
            'goal': 0
        }

        inGold = False

        #store all 
        goalNode = None

        gridSize = self.grid.size

        while openList and not inGold:
            min = 0
            #priority queue popping
            for i in range(len(openList)):
                try:
                    if openList[i].cost < openList[min].cost:
                        min = i
                except:
                    pass
            currentNode = openList.pop(min)
            currX = int(currentNode['x'])
            currY = int(currentNode['y'])
            currFront = currentNode['front']
            currAction = currentNode['actions']

            ##################################### CURRENT NODE ACTION ################################################
            if currAction == 'scan':
                #perform scan operation here
                scanVal = self.grid.scan()
                #if the value returned is pit, rotate and avert a game over
                if scanVal == 'pit':
                    #reassign reference of previously generated node
                    tempNode = newNode
                    #rotate copied miner
                    self.grid.miner.rotate()
                    #reassign miner reference
                    tempMiner = self.grid.miner
                    #generate child node
                    newNode = Node(None,currX, currY, tempMiner['compass'], "rotate", tempNode)
                    #set child node cost
                    newNode.set_cost(heurVal['rotate'])
                    #append to closed list since we have to do this immediately
                    closedList.append(newNode)
            elif currAction == 'move':
                #perform move before adding to open list
                self.grid.miner.move()
            elif currAction == 'rotate':
                self.grid.miner.rotate()

            checkCurrTile = self.grid.check()
            if checkCurrTile != ('gold' or 'pit') and (currentNode not in closedList):
                if (currentNode not in closedList) and not currentNode['scannedFront']:
                    #we are in the middle of the grid OR we are in the edge of the grid but we're 
                    #not facing the wall
                    if ((currX <= gridSize-1 and currY <= gridSize-1) and (currX >= 0 and currY >= 0)) and ((
                        (currX == gridSize-1 and currFront != 'south') or (currY == gridSize-1 and currFront != 'east')) or (
                            (currX == 0 and currFront != 'north') or (currY == 0 and currFront != 'west'))):
                       
                       ##################################### SCAN NODE ################################################
                        #generate child node
                        newNode = Node(None, currX, currY, currFront, "scan", currentNode)
                        #set child node cost
                        newNode.set_cost(heurVal['scan'])
                        #set childe node to scanned
                        newNode.setScanned(True)
                        #add child node to open list
                        openList.append(newNode)
                        
                        ##################################### MOVE NODE ################################################
                        #get miner's coordinates
                        tempMinerXY = self.grid.miner.coordinates
                        #generate child node
                        newNode= Node(None, tempMinerXY['x'], tempMinerXY['y'], tempMiner['compass'], "move", currentNode)
                        #set chlid node cost
                        newNode.set_cost(heurVal('move'))
                        #set childe node to scanned
                        newNode.setScanned(True)
                        #append to open list
                        openList.append(newNode)

                    elif  (currX  >= gridSize-1 or currY >= gridSize-1):
                        #We are at the souther/eastern edge of the grid and we're facing the wall
                        if ((currX >= gridSize-1 and currFront == 'south') or (currY >= gridSize-1 and currFront == 'east')):
                            #generate reassigned reference of miner
                            tempMiner = self.grid.miner
                            #generate child node
                            newNode = Node(None, currX, currY, tempMiner['compass'], "rotate", currentNode)
                            #set child node cost
                            newNode.set_cost(heurVal['rotate'])
                            #append to open list
                            openList.append(newNode)

                    elif  (currX  <= 0 or currY <= 0):
                        #We are at the northern/western edge of the grid and we're facing the wall
                        if ((currX <= 0 and currFront == 'north') or (currY <= 0 and currFront == 'west')):
                            #generate reassigned reference of miner
                            tempMiner = self.grid.miner
                            #generate child node
                            newNode = Node(None, currX, currY, tempMiner['compass'], "rotate", currentNode)
                            #set child node cost
                            newNode.set_cost(heurVal['rotate'])
                            #append to open list
                            openList.append(newNode)
                    
                #if this node already scanned the area, moving and rotating are the only possible choices because
                #we don't want to abuse the negative heuristic nor do we want to enter an infinite loop
                elif (currentNode not in closedList) and currentNode['scannedFront']:
                    pass
                #append current node to the closed list since we know our possible decisions
                closedList.append(currentNode)
            elif checkCurrTile == 'gold':
                inGold = True
                tempMiner = self.grid.miner
                #generate child node
                newNode = Node(None, currX, currY, tempMiner['compass'], "goal", currentNode)
                #set child node cost
                newNode.set_cost(heurVal['goal'])
                goalNode = newNode
                closedList.append(goalNode)