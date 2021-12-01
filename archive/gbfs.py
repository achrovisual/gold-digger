from pygame.version import PygameVersion
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
        """
        #establish heuristic values
        heurVal = {
            'notScanned': 0, #haven't scanned the front yet
            'alreadyScanned': 5, #already scanned the front, do we really want to scan again?
            'rotateAwayNull': 3, #scan returned null, do we rotate?
            'rotateAwayPit': 0, #avoid at all cost
            'rotateAwayBeacon': 1, #nope
            'rotateAwayEdge': 0, #reached the edge
            'rotateNoScan': 6,
            'moveToScannedGold': -1, #scan returned gold, let's go!
            'moveToScannedPit': 10, #JUST DON'T
            'moveToNullBeacon': 0, #move if scan returned null
            'movedAfterNull' : 2, #already moved after scan ret null
            'moveNoScan' : 11,
            'goal': -5 #we won!
        }"""

        root = Node(None, x, y, miner_compass, None, None)
        #root.setCost(heurVal['notScanned'])

        gridSize = self.grid.size

        openList = []
        closedList = []

        openList.append(root)

        goalNode = None
        inGold = False
        inPit = False
        inBeacon = False
        while openList and not inGold and not inPit and not inBeacon:
            currentNode = openList.pop()
            currFront = currentNode.front
            currX = currentNode.x
            currY = currentNode.y
            currAction = currentNode.actions
            scannedFront = currentNode.scannedFront
            breaker = False
            #deploy actions here
            if currAction == 'move':
                reachedEdge = self.grid.miner.move()
                if not reachedEdge:
                   currentNode.setEdge(True) 
                currX = self.grid.miner.coordinates['x']
                currY = self.grid.miner.coordinates['y']
                currentNode.x = currX
                currentNode.y = currY
            elif currAction == 'scan':
                retVal = self.grid.scan()
                currentNode.setScanned(True)
                if retVal == 'P':
                    currentNode.setPit(True)
                    print('scanned pit')
                elif retVal == 'G':
                    currentNode.setGold(True)
                elif retVal == 'B':
                    currentNode.setBeacon(True)
                else:
                    currentNode.moveToNullBeacon(True)
            elif currAction == 'rotate':
                self.grid.miner.rotate()
                currFront = self.grid.miner.compass
                currentNode.front = currFront
                currentNode.setScanned(False)
                currentNode.setGold(False)
                currentNode.setPit(False)
                currentNode.setNull(False)
            print(currAction)
            self.grid.show_grid()
            
            checkCurrTile = self.grid.check()
            checkPass = False

            if checkCurrTile == 'gold':
                inGold = True
                newNode = Node(None, currX, currY, currFront, "goal", currentNode)
                goalNode = newNode
                breaker = True
            if checkCurrTile == 'pit':
                inPit = True
                newNode = Node(None, currX, currY, currFront, "pit", currentNode)
                goalNode = newNode
                breaker = True
            if checkCurrTile == 'beacon':
                breaker = True
                inBeacon = True
                newNode = Node(None, currX, currY, currFront, 'in beacon', currentNode)
                openList.append(newNode)
            for x in closedList:
                if(currX == x.x and currY == x.y and currFront == x.front and currAction==x.actions):# and currFront == x.front and currAction == x.actions):
                    checkPass = True
            if checkPass and not breaker:
                if currentNode.scannedGold: #we found the goal node, our only option is to move forward
                    moveNode = Node(None, currX, currY, currFront, "move", currentNode)
                    #moveNode.setCost(heurVal['moveToScannedGold'])
                    moveNode.setScanned(True)
                    moveNode.setGold(True)

                    openList.append(moveNode)
                    print("to gold")
                elif currentNode.scannedPit:
                    rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                    #rotateNode.setCost(heurVal['rotateAwayPit'])
                    print("rotate away pit")
                    openList.append(rotateNode)

                elif currentNode.scannedFront:
                    if not currentNode.scannedPit and not currentNode.reachedEdge:
                        moveNode = Node(None, currX, currY, currFront, "move", currentNode)
                        openList.append(moveNode)
                    else:
                        rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                        openList.append(rotateNode)
                else:
                    if not currentNode.reachedEdge:
                        scanNode = Node(None, currX, currY, currFront, "scan", currentNode)
                        moveNode = Node(None, currX, currY, currFront, "move", currentNode)
                        openList.append(moveNode)
                        openList.append(scanNode)
                        print("here")
                    else:
                        rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                        openList.append(rotateNode)
                    
            elif not checkPass and not breaker:
                moveNode = None
                scanNode = None
                rotateNode = None

                if currentNode.scannedPit:
                    rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                    #rotateNode.setCost(heurVal['rotateAwayPit'])
                    print("rotate away pit")
                    openList.append(rotateNode)

                elif currentNode.scannedGold: #we found the goal node, our only option is to move forward
                    moveNode = Node(None, currX, currY, currFront, "move", currentNode)
                    #moveNode.setCost(heurVal['moveToScannedGold'])
                    moveNode.setScanned(True)
                    moveNode.setGold(True)

                    openList.append(moveNode)
                    print("to gold")
                elif currentNode.scannedBeacon:
                    moveNode = Node(None, currX, currY, currFront, "move", currentNode)
                    #moveNode.setCost(heurVal['moveToScannedGold'])
                    moveNode.setScanned(True)
                    moveNode.setGold(True)

                    openList.append(moveNode)
                elif currentNode.moveToNull:
                    moveNode = Node(None, currX, currY, currFront, "move", currentNode)
                    #moveNode.setCost(heurVal['moveToNullBeacon'])
                    
                    scanNode = Node(None, currX, currY, currFront, "scan", currentNode)
                    #scanNode.setCost(heurVal['notScanned'])

                    rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                    #rotateNode.setCost(heurVal['rotateNoScan'])

                    openList.append(moveNode)
                    openList.append(scanNode)
                    openList.append(rotateNode)

                    """
                    if(moveNode.cost > scanNode.cost and moveNode.cost > rotateNode.cost):
                        openList.append(moveNode)
                        if(scanNode.cost > rotateNode.cost):
                            openList.append(scanNode)
                            openList.append(rotateNode)
                        else:
                            openList.append(rotateNode)
                            openList.append(scanNode)
                    elif(scanNode.cost > moveNode.cost and scanNode.cost > rotateNode.cost):
                        openList.append(scanNode)
                        if(moveNode.cost > rotateNode):
                            openList.append(moveNode)
                            openList.append(rotateNode)
                        else:
                            openList.append(rotateNode)
                            openList.append(moveNode)
                    elif(rotateNode.cost > moveNode.cost and rotateNode.cost > scanNode.cost):
                        openList.append(rotateNode)
                        if(moveNode.cost > scanNode.cost):
                            openList.append(moveNode)
                            openList.append(scanNode)
                        else:
                            openList.append(scanNode)
                            openList.append(moveNode)
                elif currentNode.reachedEdge:
                    rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                    rotateNode.setCost(heurVal['rotateAwayEdge'])
                    
                    openList.append(rotateNode)
                    """
                elif not currentNode.scannedGold and not currentNode.moveToNull:
                    if checkCurrTile != 'gold' or checkCurrTile != 'pit':
                        if (currX >= 0) and (currY >= 0 ):# and currFront !='north'         and currFront != 'west'
                            if ((currY == 0 and currFront =='north') or ( currX == 0 and currFront == 'west')):
                                rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                                #rotateNode.setCost(heurVal['rotateAwayEdge'])

                                openList.append(rotateNode)
                                print("3 elif")

                            elif not scannedFront and ((currY < gridSize-1 and currFront!='south') or (currX < gridSize-1 and currFront != 'east')):
                                scanNode = Node(None, currX, currY, currFront, "scan", currentNode)
                                scanNode.setScanned(True)
                                #scanNode.setCost(heurVal['alreadyScanned'])

                                rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                                #rotateNode.setCost(heurVal['rotateNoScan'])

                                moveNode = Node(None, currX, currY, currFront, "move", currentNode)
                                #moveNode.setCost(heurVal['moveNoScan'])
                                
                                openList.append(moveNode)
                                openList.append(rotateNode)
                                openList.append(scanNode)
                                """
                                if(moveNode.cost > scanNode.cost and moveNode.cost > rotateNode.cost):
                                    openList.append(moveNode)
                                    if(scanNode.cost > rotateNode.cost):
                                        openList.append(scanNode)
                                        openList.append(rotateNode)
                                    else:
                                        openList.append(rotateNode)
                                        openList.append(scanNode)
                                elif(scanNode.cost > moveNode.cost and scanNode.cost > rotateNode.cost):
                                    openList.append(scanNode)
                                    if(moveNode.cost > rotateNode):
                                        openList.append(moveNode)
                                        openList.append(rotateNode)
                                    else:
                                        openList.append(rotateNode)
                                        openList.append(moveNode)
                                elif(rotateNode.cost > moveNode.cost and rotateNode.cost > scanNode.cost):
                                    openList.append(rotateNode)
                                    if(moveNode.cost > scanNode.cost):
                                        openList.append(moveNode)
                                        openList.append(scanNode)
                                    else:
                                        openList.append(scanNode)
                                        openList.append(moveNode)
                                """
                                print("1 elif")

                            elif scannedFront and ((currY < gridSize-1 and currFront!='south') or (currX < gridSize-1 and currFront != 'east')):

                                moveNode = Node(None, currX, currY, currFront, "move", currentNode)
                                moveNode.setScanned(True)
                                #moveNode.setCost(heurVal['movedAfterNull'])

                                rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                                rotateNode.setScanned(False)
                                #rotateNode.setCost(heurVal['rotateAwayNull'])

                                """
                                if rotateNode.cost > moveNode.cost:
                                    openList.append(rotateNode)
                                    openList.append(moveNode)
                                else:
                                    openList.append(moveNode)
                                    openList.append(rotateNode)"""
                                
                                openList.append(rotateNode)
                                openList.append(moveNode)
                                print("4 elif")

                            elif ((currY == gridSize-1 and currFront =='south') or (currX == gridSize-1 and currFront == 'east')):
                                rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                                #rotateNode.setCost(heurVal['rotateAwayEdge'])

                                openList.append(rotateNode)
                                print("2 elif")
                
                closedList.append(currentNode)
            
        if inGold:
            print('found')
        if inPit:
            print("landed in pit")
        if inBeacon:
            print("in beacon")
