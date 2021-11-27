class Node():
    def __init__(self, id, x, y, front, actions, parent):
        self.id = id
        self.x = x
        self.y = y
        self.front = front
        self.actions = actions
        self.parent = parent
        self.cost = None
    def set_cost(self, cost):
        self.cost = cost
