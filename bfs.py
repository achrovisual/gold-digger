from agent import Agent
from node import Node

from queue import Queue
from queue import LifoQueue
from time import sleep

class BFS(Agent):
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
        actions = []
        actions2 = []

        root = Node(node_counter, x, y, miner_compass, None, None)

        # Initialize node queue
        node_queue = Queue()
        node_queue.put(root)

        # Initialize visited nodes list
        visited_nodes = []
        visited_nodes.append({"x": x, "y": y, "front": self.grid.miner.compass})

        while solving:
            # print(self.grid.check())
            if node_queue.empty():
                break

            current = node_queue.get()
            self.grid.miner.coordinates["x"] = current.x
            self.grid.miner.coordinates["y"] = current.y
            self.grid.miner.compass = current.front
            actions = []
            actions2 = []

            if self.grid.miner.compass == "east":
                if self.grid.miner.coordinates["x"] + 1 <= self.grid.size - 1:
                    temp_scan = self.grid.scan()
                    actions.append("scan")

                    temp_node = {"x": self.grid.miner.coordinates["x"] + 1, "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                    visited = True if visited_nodes.count(temp_node) > 0 else False
                    if not visited:
                        if temp_scan == "" or temp_scan == "B":
                            if self.grid.miner.move():
                                actions.append("move")

                            node_counter += 1
                            visited_nodes.append(temp_node)
                            child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                            node_queue.put(child)
                        elif temp_scan == "P":
                            if self.grid.miner.move():
                                actions.append("move")

                            temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                            visited = True if visited_nodes.count(temp_node) > 0 else False

                            if not visited:
                                node_counter += 1
                                visited_nodes.append(temp_node)
                                child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                                node_queue.put(child)
                        elif temp_scan == "G":
                            if self.grid.miner.move():
                                # print('moving towards gold', self.grid.miner.coordinates)
                                actions.append("move")

                            if self.grid.check() == 'gold':
                                solvable = True

                                node_counter += 1
                                visited_nodes.append(temp_node)
                                child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                                node_queue.put(child)

                                goal = child
                                solving = False

                elif self.grid.miner.coordinates["x"] + 1 > self.grid.size - 1:
                    if self.grid.miner.rotate():
                        actions2.append("rotate")

                    temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                    visited = True if visited_nodes.count(temp_node) > 0 else False

                    if not visited:
                        node_counter += 1
                        visited_nodes.append(temp_node)
                        child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions2, current)
                        node_queue.put(child)

                self.grid.miner.coordinates["x"] = current.x
                self.grid.miner.coordinates["y"] = current.y

                if self.grid.miner.rotate():
                    actions2.append("rotate")

                temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                visited = True if visited_nodes.count(temp_node) > 0 else False

                if not visited:
                    node_counter += 1
                    visited_nodes.append(temp_node)
                    child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions2, current)
                    node_queue.put(child)

                self.grid.miner.compass = "east"
            elif self.grid.miner.compass == "west":
                if self.grid.miner.coordinates["x"] - 1 >= 0:
                    temp_scan = self.grid.scan()
                    actions.append("scan")

                    temp_node = {"x": self.grid.miner.coordinates["x"] - 1, "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                    visited = True if visited_nodes.count(temp_node) > 0 else False

                    if not visited:
                        if temp_scan == "" or temp_scan == "B":
                            if self.grid.miner.move():
                                actions.append("move")

                            node_counter += 1
                            visited_nodes.append(temp_node)
                            child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                            node_queue.put(child)
                        elif temp_scan == "P":
                            if self.grid.miner.move():
                                actions.append("move")

                            temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                            visited = True if visited_nodes.count(temp_node) > 0 else False

                            if not visited:
                                node_counter += 1
                                visited_nodes.append(temp_node)
                                child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                                node_queue.put(child)
                        elif temp_scan == "G":
                            if self.grid.miner.move():
                                actions.append("move")

                            if self.grid.check() == 'gold':
                                solvable = True

                                node_counter += 1
                                visited_nodes.append(temp_node)
                                child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                                node_queue.put(child)

                                goal = child
                                solving = False

                elif self.grid.miner.coordinates["x"] - 1 < 0:
                    if self.grid.miner.rotate():
                        actions2.append("rotate")

                    temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                    visited = True if visited_nodes.count(temp_node) > 0 else False

                    if not visited:
                        node_counter += 1
                        visited_nodes.append(temp_node)
                        child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions2, current)
                        node_queue.put(child)

                self.grid.miner.coordinates["x"] = current.x
                self.grid.miner.coordinates["y"] = current.y

                if self.grid.miner.rotate():
                    actions2.append("rotate")

                temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                visited = True if visited_nodes.count(temp_node) > 0 else False

                if not visited:
                    node_counter += 1
                    visited_nodes.append(temp_node)
                    child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions2, current)
                    node_queue.put(child)

                self.grid.miner.compass = "west"
            elif self.grid.miner.compass == "south":
                if self.grid.miner.coordinates["y"] + 1 <= self.grid.size - 1:
                    temp_scan = self.grid.scan()
                    actions.append("scan")

                    temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"] + 1, "front": self.grid.miner.compass}
                    visited = True if visited_nodes.count(temp_node) > 0 else False

                    if not visited:
                        if temp_scan == "" or temp_scan == "B":
                            if self.grid.miner.move():
                                actions.append("move")

                            node_counter += 1
                            visited_nodes.append(temp_node)
                            child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                            node_queue.put(child)
                        elif temp_scan == "P":
                            if self.grid.miner.move():
                                actions.append("move")

                            temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                            visited = True if visited_nodes.count(temp_node) > 0 else False

                            if not visited:
                                node_counter += 1
                                visited_nodes.append(temp_node)
                                child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                                node_queue.put(child)
                        elif temp_scan == "G":
                            if self.grid.miner.move():
                                actions.append("move")

                            if self.grid.check() == 'gold':
                                solvable = True

                                node_counter += 1
                                visited_nodes.append(temp_node)
                                child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                                node_queue.put(child)

                                goal = child
                                solving = False

                elif self.grid.miner.coordinates["y"] + 1 > self.grid.size - 1:
                    if self.grid.miner.rotate():
                        actions2.append("rotate")

                    temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                    visited = True if visited_nodes.count(temp_node) > 0 else False

                    if not visited:
                        node_counter += 1
                        visited_nodes.append(temp_node)
                        child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions2, current)
                        node_queue.put(child)

                self.grid.miner.coordinates["x"] = current.x
                self.grid.miner.coordinates["y"] = current.y

                if self.grid.miner.rotate():
                    actions2.append("rotate")

                temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                visited = True if visited_nodes.count(temp_node) > 0 else False

                if not visited:
                    node_counter += 1
                    visited_nodes.append(temp_node)
                    child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions2, current)
                    node_queue.put(child)

                self.grid.miner.compass = "south"
            elif self.grid.miner.compass == "north":
                if self.grid.miner.coordinates["y"] - 1 >= 0:
                    temp_scan = self.grid.scan()
                    actions.append("scan")

                    temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"] - 1, "front": self.grid.miner.compass}
                    visited = True if visited_nodes.count(temp_node) > 0 else False

                    if not visited:
                        if temp_scan == "" or temp_scan == "B":
                            if self.grid.miner.move():
                                actions.append("move")

                            node_counter += 1
                            visited_nodes.append(temp_node)
                            child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                            node_queue.put(child)
                        elif temp_scan == "P":
                            if self.grid.miner.move():
                                actions.append("move")

                            temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                            visited = True if visited_nodes.count(temp_node) > 0 else False

                            if not visited:
                                node_counter += 1
                                visited_nodes.append(temp_node)
                                child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                                node_queue.put(child)
                        elif temp_scan == "G":
                            if self.grid.miner.move():
                                actions.append("move")

                elif self.grid.miner.coordinates["y"] - 1 < 0:
                    if self.grid.miner.rotate():
                        actions2.append("rotate")

                    temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                    visited = True if visited_nodes.count(temp_node) > 0 else False

                    if not visited:
                        node_counter += 1
                        visited_nodes.append(temp_node)
                        child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions2, current)
                        node_queue.put(child)

                self.grid.miner.coordinates["x"] = current.x
                self.grid.miner.coordinates["y"] = current.y

                if self.grid.miner.rotate():
                    actions2.append("rotate")

                temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                visited = True if visited_nodes.count(temp_node) > 0 else False

                if not visited:
                    node_counter += 1
                    visited_nodes.append(temp_node)
                    child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions2, current)
                    node_queue.put(child)

                self.grid.miner.compass = "north"

            if self.grid.check() == 'gold':
                self.grid.solving = 2
                solvable = True
                node_counter += 1
                visited_nodes.append(temp_node)
                child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                node_queue.put(child)

                goal = child
                solving = False
            elif self.grid.check() == 'pit':
                self.grid.solving = 2
                solvable = False
                solving = False
                # print('i am in da pit')

            # print(self.grid.miner.coordinates, self.grid.miner.compass, self.grid.scan())
            self.grid.show_grid()
            # print(self.grid.miner.actions)
            if solvable:
                # print("search success")
                self.grid.miner.actions = [0, 0, 0] # reset action counter

                temp = goal

                path = LifoQueue()

                path.put(temp)

                while temp.parent is not None:
                    temp = temp.parent
                    path.put(temp)

                # a = 0
                # b = 0
                # c = 0

                sleep(2.5)
                while not path.empty():
                    sleep(.25)
                    temp = path.get()
                    self.grid.miner.coordinates["x"] = temp.x
                    self.grid.miner.coordinates["y"] = temp.y
                    self.grid.miner.compass = temp.front

                    # print("__________")
                    # print("Node ID: ", temp.id)

                    # print(temp.actions)

                    if temp.actions is not None:
                        # a += temp.actions.count("rotate")
                        # b += temp.actions.count("scan")
                        # c += temp.actions.count("move")
                        self.grid.miner.actions[0] += temp.actions.count("move")
                        self.grid.miner.actions[1] += temp.actions.count("rotate")
                        self.grid.miner.actions[2] += temp.actions.count("scan")
                    
                    self.grid.show_grid()
                    # print(self.grid.miner.actions)
                    # print("Number of rotates: ", a)
                    # print("Number of scans: ", b)
                    # print("Number of moves: ", c)
