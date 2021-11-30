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
            'rotateNoScan': 6,
            'moveToScannedGold': -1, #scan returned gold, let's go!
            'moveToScannedPit': 10, #JUST DON'T
            'moveToNullBeacon': 0, #move if scan returned null
            'movedAfterNull' : 2, #already moved after scan ret null
            'moveNoScan' : 11,
            'goal': -5 #we won!
        }

        root = Node(None, x, y, miner_compass, None, None)
        root.setCost(heurVal['notScanned'])

        gridSize = self.grid.size

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
            if currAction == 'move':
                self.grid.miner.move()
                currX = self.grid.miner.coordinates['x']
                currY = self.grid.miner.coordinates['y']
            elif currAction == 'scan':
                retVal = self.grid.smartScan()
                if retVal == 'P':
                    currentNode.setPit(True)
                elif retVal == 'G':
                    currentNode.setGold(True)
                else:
                    currentNode.moveToNullBeacon(True)
            elif currAction == 'rotate':
                self.grid.miner.rotate()
                currFront = self.grid.miner.compass
                currentNode.setScanned(False)

            checkCurrTile = self.grid.check()
            checkPass = False
            
            if checkCurrTile == 'gold':
                inGold = True
                newNode = Node(None, currX, currY, currFront, "goal", currentNode)
                goalNode = newNode

                break

            for x in closedList:
                if(currX == x.x and currY == x.y and currFront == x.front and currAction == x.actions):
                    checkPass = True
            if not checkPass:
                if currentNode.scannedPit:
                    rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                    rotateNode.setCost(heurVal['rotateAwayPit'])

                    openList.append(rotateNode)
                elif currentNode.moveToNull:
                    moveNode = Node(None, currX, currY, currFront, "move", currentNode)
                    moveNode.setCost(heurVal['moveToNullBeacon'])
                    
                    openList.append(moveNode)
                elif not currentNode.scannedGold and not currentNode.moveToNull:
                    if checkCurrTile != 'gold' or checkCurrTile != 'pit':
                        if (currX >= 0 and currFront !='north') and (currY >= 0 and currFront != 'west'):
                            if not scannedFront and ((currX != gridSize-1 and currFront!='south') or (currY != gridSize-1 and currFront != 'east')):
                                scanNode = Node(None, currX, currY, currFront, "scan", currentNode)
                                scanNode.setScanned(True)
                                scanNode.setCost(heurVal['alreadyScanned'])

                                rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                                rotateNode.setCost(heurVal['rotateNoScan'])

                                moveNode = Node(None, currX, currY, currFront, "move", currentNode)
                                moveNode.setCost(heurVal['moveNoScan'])

                                openList.append(moveNode)
                                openList.append(rotateNode)
                                openList.append(scanNode)
                                print("1 elif")

                            elif not scannedFront and ((currX == gridSize-1 and currFront =='south') or (currY == gridSize-1 and currFront == 'east')):
                                rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                                rotateNode.setCost(heurVal['rotateAwayEdge'])

                                openList.append(rotateNode)
                                print("2 elif")

                            elif not scannedFront and ((currX == 0 and currFront =='north') or (currY == 0 and currFront == 'west')):
                                rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                                rotateNode.setCost(heurVal['rotateAwayEdge'])

                                openList.append(rotateNode)
                                print("3 elif")

                            elif scannedFront and ((currX != gridSize-1 and currFront!='south') or (currY != gridSize-1 and currFront != 'east')):
                                scanNode = Node(None, currX, currY, currFront, "scan", currentNode)
                                scanNode.setScanned(True)
                                scanNode.setCost(heurVal['alreadyScanned'])

                                moveNode = Node(None, currX, currY, currFront, "move", currentNode)
                                moveNode.setScanned(True)
                                moveNode.setCost(heurVal['movedAfterNull'])

                                rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                                rotateNode.setScanned(False)

                                openList.append(rotateNode)
                                openList.append(moveNode)
                                print("4 elif")

                            elif scannedFront and ((currX == gridSize-1 and currFront =='south') or (currY == gridSize-1 and currFront == 'east')):
                                rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                                rotateNode.setCost(heurVal['rotateAwayEdge'])
                                rotateNode.setScanned(False)

                                openList.append(rotateNode)
                                print("5 elif")
                            elif scannedFront and ((currX == 0 and currFront =='north') or (currY == 0 and currFront == 'west')):
                                rotateNode = Node(None, currX, currY, currFront, "rotate", currentNode)
                                rotateNode.setCost(heurVal['rotateAwayEdge'])
                                rotateNode.setScanned(False)

                                openList.append(rotateNode)
                                print("6 elif")
                elif currentNode.scannedGold: #we found the goal node, our only option is to move forward
                    moveNode = Node(None, currX, currY, currFront, "move", currentNode)
                    moveNode.setCost(heurVal['moveToScannedGold'])
                    moveNode.setGold(True)
                    openList.append(moveNode)
                
                closedList.append(currentNode)
            
            self.grid.show_grid()
            print(currAction)
        if inGold:
            print('found')