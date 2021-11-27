from agent import Agent
from node import Node

from queue import Queue
from queue import LifoQueue

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
            if node_queue.empty():
                break;

            current = node_queue.get()
            self.grid.miner.coordinates["x"] = current.x
            self.grid.miner.coordinates["y"] = current.y
            self.grid.miner.compass = current.front
            actions = []
            actions2 = []

            if self.grid.miner.compass == "east":
                if self.grid.miner.coordinates["y"] + 1 <= self.grid.size - 1:
                    temp_scan = self.grid.check()
                    actions.append("scan")

                    temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"] + 1, "front": self.grid.miner.compass}
                    visited = True if visited_nodes.count(temp_node) > 0 else False
                    if not visited:
                        if temp_scan == "null" or temp_scan == "beacon":
                            if self.grid.miner.move():
                                actions.append("move")

                            node_counter += 1
                            visited_nodes.append(temp_node)
                            child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                            node_queue.put(child)
                        elif temp_scan == "pit":
                            if self.grid.miner.rotate():
                                actions.append("rotate")

                            temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                            visited = True if visited_nodes.count(temp_node) > 0 else False

                            if not visited:
                                node_counter += 1
                                visited_nodes.append(temp_node)
                                child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                                node_queue.put(child)
                        elif temp_scan == "gold":
                            solvable = True

                            if self.grid.miner.move():
                                actions.append("move")

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

                self.grid.miner.compass = "east"
            elif self.grid.miner.compass == "west":
                if self.grid.miner.coordinates["y"] - 1 >= 0:
                    temp_scan = self.grid.check()
                    actions.append("scan")

                    temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"] - 1, "front": self.grid.miner.compass}
                    visited = True if visited_nodes.count(temp_node) > 0 else False

                    if not visited:
                        if temp_scan == "null" or temp_scan == "beacon":
                            if self.grid.miner.move():
                                actions.append("move")

                            node_counter += 1
                            visited_nodes.append(temp_node)
                            child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                            node_queue.put(child)
                        elif temp_scan == "pit":
                            if self.grid.miner.rotate():
                                actions.append("rotate")

                            temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                            visited = True if visited_nodes.count(temp_node) > 0 else False

                            if not visited:
                                node_counter += 1
                                visited_nodes.append(temp_node)
                                child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                                node_queue.put(child)
                        elif temp_scan == "gold":
                            solvable = True

                            if self.grid.miner.move():
                                actions.append("move")

                            node_counter += 1
                            visited_nodes.append(temp_node)
                            child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                            node_queue.put(child)

                            goal = child
                            solving = False

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

                self.grid.miner.compass = "west"
            elif self.grid.miner.compass == "south":
                if self.grid.miner.coordinates["x"] + 1 <= self.grid.size - 1:
                    temp_scan = self.grid.check()
                    actions.append("scan")

                    temp_node = {"x": self.grid.miner.coordinates["x"] + 1, "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                    visited = True if visited_nodes.count(temp_node) > 0 else False

                    if not visited:
                        if temp_scan == "null" or temp_scan == "beacon":
                            if self.grid.miner.move():
                                actions.append("move")

                            node_counter += 1
                            visited_nodes.append(temp_node)
                            child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                            node_queue.put(child)
                        elif temp_scan == "pit":
                            if self.grid.miner.rotate():
                                actions.append("rotate")

                            temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                            visited = True if visited_nodes.count(temp_node) > 0 else False

                            if not visited:
                                node_counter += 1
                                visited_nodes.append(temp_node)
                                child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                                node_queue.put(child)
                        elif temp_scan == "gold":
                            solvable = True

                            if self.grid.miner.move():
                                actions.append("move")

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

                self.grid.miner.compass = "south"
            elif self.grid.miner.compass == "north":
                if self.grid.miner.coordinates["x"] - 1 >= 0:
                    temp_scan = self.grid.check()
                    actions.append("scan")

                    temp_node = {"x": self.grid.miner.coordinates["x"] - 1, "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                    visited = True if visited_nodes.count(temp_node) > 0 else False

                    if not visited:
                        if temp_scan == "null" or temp_scan == "beacon":
                            if self.grid.miner.move():
                                actions.append("move")

                            node_counter += 1
                            visited_nodes.append(temp_node)
                            child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                            node_queue.put(child)
                        elif temp_scan == "pit":
                            if self.grid.miner.rotate():
                                actions.append("rotate")

                            temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                            visited = True if visited_nodes.count(temp_node) > 0 else False

                            if not visited:
                                node_counter += 1
                                visited_nodes.append(temp_node)
                                child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                                node_queue.put(child)
                        elif temp_scan == "gold":
                            solvable = True

                            if self.grid.miner.move():
                                actions.append("move")

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

                self.grid.miner.compass = "north"

            if solvable:
                print("search success")

                temp = goal

                path = LifoQueue()

                path.put(temp)

                while temp.parent is not None:
                    temp = temp.parent
                    path.put(temp)

                a = 0
                b = 0
                c = 0

                while not path.empty():
                    temp = path.get()
                    self.grid.miner.coordinates["x"] = temp.x
                    self.grid.miner.coordinates["y"] = temp.y
                    self.grid.miner.compass = temp.front

                    self.grid.show_grid()
                    print("__________")
                    print("Node ID: ", temp.id)

                    print(temp.actions)

                    if temp.actions is not None:
                        a += temp.actions.count("rotate")
                        b += temp.actions.count("scan")
                        c += temp.actions.count("move")

                    print("Number of rotates: ", a)
                    print("Number of scans: ", b)
                    print("Number of moves: ", c)
