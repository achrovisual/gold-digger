from pygame.version import PygameVersion
from agent import Agent
from node import Node
from grid import Grid
from queue import LifoQueue
from time import sleep

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
        actions = []

        root = Node(node_counter, x, y, miner_compass, None, None)

        # Initialize node stack
        node_stack = LifoQueue()
        node_stack.put(root)

        visited_nodes = []
        visited_nodes.append({"x": x, "y": y, "front": self.grid.miner.compass})

        beacon_list = []

        while solving:
            # print('-------------')
            temp_node = None
            if node_stack.empty():
                break

            current = node_stack.get()
            self.grid.miner.coordinates["x"] = current.x
            self.grid.miner.coordinates["y"] = current.y
            self.grid.miner.compass = current.front
            self.grid.miner.scanned = None
            actions = []

            scanning = True
            counter = 0
            scan_results = []
            gold_found = False
            # print('current ', self.grid.miner.coordinates, self.grid.miner.compass)

            while scanning and not gold_found:
                self.grid.miner.scanned = None
                if counter == 3:
                    scanning = False
                # print('facing ', self.grid.miner.compass, self.grid.scan())
                # print((self.grid.miner.compass == 'west' and self.grid.miner.coordinates["x"] - 1 >= self.grid.size - 0))

                if (self.grid.miner.compass == 'east' and self.grid.miner.coordinates["x"] + 1 < self.grid.size - 1) or (self.grid.miner.compass == 'west' and self.grid.miner.coordinates["x"] - 1 >= 0) or (self.grid.miner.compass == 'south' and self.grid.miner.coordinates["y"] + 1 < self.grid.size - 1) or (self.grid.miner.compass == 'north' and self.grid.miner.coordinates["y"] - 1 >= 0):
                    # print({"direction": self.grid.miner.compass, "result": self.grid.scan()})
                    scan_results.append({"direction": self.grid.miner.compass, "result": self.grid.scan()})
                    actions.append("scan")

                    if self.grid.miner.rotate():
                        actions.append("rotate")

                    temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                    visited = True if visited_nodes.count(temp_node) > 0 else False

                    if not visited:
                        node_counter += 1
                        visited_nodes.append(temp_node)
                        child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                        node_stack.put(child)
                else:
                    if self.grid.miner.rotate():
                        actions.append("rotate")

                    temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                    visited = True if visited_nodes.count(temp_node) > 0 else False

                    if not visited:
                        node_counter += 1
                        visited_nodes.append(temp_node)
                        child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                        node_stack.put(child)

                counter += 1

            self.grid.miner.compass = current.front

            for i in scan_results:
                # print(i)
                if 'G' == i["result"]:
                    self.grid.miner.compass = i["direction"]
                    # print('moving towards gold', self.grid.miner.coordinates, self.grid.miner.compass)
                    gold_found = True
                    break

            for i in scan_results:
                if 'B' == i["result"] and not gold_found:
                    if beacon_list.count(self.grid.miner.coordinates) == 0:
                        self.grid.miner.compass = i["direction"]
                        # print('moving towards beacon', self.grid.miner.coordinates, self.grid.miner.compass)
                        break
            for i in scan_results:
                if 'P' == i["result"] and i["direction"] == self.grid.miner.compass and not gold_found:
                    if self.grid.miner.rotate():
                        # print('rotating away from pit', self.grid.miner.coordinates)
                        actions.append("rotate")
                    node_counter += 1
                    visited_nodes.append(temp_node)
                    child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                    node_stack.put(child)
                    break

            if (self.grid.miner.compass == 'east' and self.grid.miner.coordinates["x"] + 1 <= self.grid.size - 1) or (self.grid.miner.compass == 'west' and self.grid.miner.coordinates["x"] - 1 >=  0) or (self.grid.miner.compass == 'south' and self.grid.miner.coordinates["y"] + 1 <= self.grid.size - 1) or (self.grid.miner.compass == 'north' and self.grid.miner.coordinates["y"] - 1 >= 0):
                if self.grid.miner.move():
                    # print('moving forward ', self.grid.miner.coordinates, self.grid.miner.compass)
                    actions.append("move")
                temp_node = {"x": self.grid.miner.coordinates["x"], "y": self.grid.miner.coordinates["y"], "front": self.grid.miner.compass}
                visited = True if visited_nodes.count(temp_node) > 0 else False

                if not visited:
                    node_counter += 1
                    visited_nodes.append(temp_node)
                    child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                    node_stack.put(child)
            else:
                if self.grid.miner.rotate():
                    # print('rotating away from edge', self.grid.miner.coordinates)
                    actions.append("rotate")
                node_counter += 1
                visited_nodes.append(temp_node)
                child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                node_stack.put(child)

            node_counter += 1
            visited_nodes.append(temp_node)
            child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
            node_stack.put(child)

            if self.grid.check() == 'gold':
                solvable = True

                node_counter += 1
                visited_nodes.append(temp_node)
                child = Node(node_counter, self.grid.miner.coordinates["x"], self.grid.miner.coordinates["y"], self.grid.miner.compass, actions, current)
                node_stack.put(child)

                goal = child
                solving = False
            elif self.grid.check() == 'pit':
                solvable = False
                solving = False
                # print('i am in da pit')

            elif self.grid.check() == 'beacon':
                beacon_list.append(self.grid.miner.coordinates)
                # print('im in da beacon')

            if solvable:
                # print("search success")

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
                    # print("__________")
                    # print("Node ID: ", temp.id)

                    # print(temp.actions)

                    if temp.actions is not None:
                        a += temp.actions.count("rotate")
                        b += temp.actions.count("scan")
                        c += temp.actions.count("move")

                    # print("Number of rotates: ", a)
                    # print("Number of scans: ", b)
                    # print("Number of moves: ", c)

            self.grid.show_grid()
