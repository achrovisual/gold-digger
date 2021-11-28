from agent import Agent
from grid import Grid
from node import Node
import copy

class BFS(Agent):
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
            'scan': -1
        }

        inGold = False

        #store all 
        goalList = []

        gridSize = self.grid.size

        while openList and not inGold:
            currentNode = openList.pop()
            currX = int(currentNode['x'])
            currY = int(currentNode['y'])
            currFront = currentNode['front']

            checkCurrTile = self.grid.check()
            if checkCurrTile != ('gold' or 'pit'):
                if (currentNode not in closedList) and (currentNode['actions'] != 'scan'):
                    #we are in the middle of the grid
                    if (currX != gridSize-1 and currY != gridSize-1) and (currX > 0 and currY > 0):
                        #generate child node
                        newNode = Node(None, currX, currY, currFront, "scan", currentNode)
                        #set child node cost
                        newNode.set_cost(heurVal['scan'])
                        #add child node to open list
                        openList.append(newNode)
                        #perform scan operation here
                        scanVal = self.grid.scan()
                        #if the value returned is pit, rotate and avert game over
                        if scanVal == 'pit':
                            #generate independent copy of miner
                            tempMiner = copy.deepcopy(self.grid.miner)
                            #reassign reference of previously generated node
                            tempNode = newNode
                            #rotate copied miner
                            tempMiner.rotate()
                            #generate child node
                            newNode = Node(None,currX, currY, tempMiner['compass'], "rotate", tempNode)
                            #set child node cost
                            newNode.set_cost(heurVal['rotate'])
                            #append to open list
                            openList.append(newNode)

                        #generate independent copy of miner
                        tempMiner = copy.deepcopy(self.grid.miner)
                        #rotate copied miner
                        tempMiner.rotate()
                        #generate child node
                        newNode = Node(None,currX, currY, tempMiner['compass'], "rotate", currentNode)
                        #set child node cost
                        newNode.set_cost(heurVal['rotate'])
                        #append to open list
                        openList.append(newNode)

                        #generate independent copy of miner
                        tempMiner = copy.deepcopy(self.grid.miner)
                        #perform move before adding to open list
                        tempMiner.move()
                        #get copied miner's new coordinates
                        tempMinerXY = tempMiner.coordinates
                        #generate child node
                        newNode= Node(None, tempMinerXY['x'], tempMinerXY['y'], tempMiner['compass'], "move", currentNode)
                        #set chlid node cost
                        newNode.set_cost(heurVal('move'))
                        #append to open list
                        openList.append(newNode)
                    elif  (currX  == gridSize-1 or currY == gridSize-1):
                        #We are at the eastern/southern edge of the grid, our choices are either scan or rotate.
                        #We can scan only if we're not facing the edge, we can only rotate
                        #if we are facing the eastern edge/southern edge.
                        if (currX == gridSize-1 and currFront == 'east') or (currY == gridSize-1 and currFront == 'south'):
                            #generate independent copy of miner
                            tempMiner = copy.deepcopy(self.grid.miner)
                            #rotate copied miner
                            tempMiner.rotate()
                            #generate child node
                            newNode = Node(None, currX, currY, tempMiner['compass'], "rotate", currentNode)
                            #set child node cost
                            newNode.set_cost(heurVal['rotate'])
                            #append to open list
                            openList.append(newNode)

                    #append current node to the closed list since we know our possible decisions
                    closedList.append(currentNode)
                #if this node already scanned the area, moving and rotating are the only possible choices because
                #we don't want to abuse the negative heurostic nor do we want to enter an infinite loop
                elif (currentNode not in closedList) and (currentNode['actions'] == 'scan'):
                    pass
