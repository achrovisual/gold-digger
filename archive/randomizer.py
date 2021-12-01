from object import Object
from miner import Miner
import random

class Randomizer():
    def __init__(self, agent, size):
        self.agent = agent
        self.size = size

    def random_action(self):
        actions = ('move', 'rotate', 'scan')

        # perform random actions
        valid = False #used to loop incase an action was invalid
        while not valid:
            choice = random.choice(actions)
            if choice == 'move':
                if self.check_move(choice):
                    self.agent.move()
                    valid = True
                else:
                    valid = False
            elif choice == 'rotate':
                self.agent.rotate()
                valid = True
            elif choice == 'scan':
                self.agent.scan()
                valid = True

    # validate action -- check if move is valid
    def check_move(self, action):
        if action == 'move':
            # if miner is at the edge
            if self.agent.coordinates.get("x") == self.size and self.agent.compass == "east":
                pass
            elif self.agent.coordinates.get("x") == 1 and self.agent.compass == "west":
                pass
            elif self.agent.coordinates.get("y") == self.size and self.agent.compass == "south":
                pass
            elif self.agent.coordinates.get("y") == 1 and self.agent.compass == "north":
                pass
            # if miner is not at the edge -- valid
            else:
                return True
            return False
