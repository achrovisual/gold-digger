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
        node_counter = 0
        miner_location = self.grid.miner.coordinates
        x  = int(miner_location["x"])
        y = int(miner_location["y"])
        miner_compass = self.grid.miner.compass

        heurVal = {
            'scan': 1,
            'move': 1,
            'rotate': 1
        }

        root = Node(node_counter, x, y, miner_compass, None, None)
        root.set_cost(0)
        root.setScanned(False)

        openList = []
        closedList = []

        openList.append(root)

        while openList:
            pass