class Node():
    def __init__(self, id, x, y, front, actions, parent):
        self.id = id
        self.x = x
        self.y = y
        self.front = front
        self.actions = actions
        self.parent = parent
        self.scanned = ''
