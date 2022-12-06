import sys
import json
import queue


class Student(object):
    '''
    Student definition
    '''
    def __init__(self, id, year, troublesome, red_mobility, id_sibling):
        self.id = id

        if year not in (1, 2): raise ValueError
        self.year = year

        if troublesome == "C":
            self.troublesome = True
        elif troublesome == "X":
            self.troublesome = False
        else: raise ValueError

        if red_mobility == "R":
            self.red_mobility = True
        elif red_mobility == "X":
            self.red_mobility = False
        else: raise ValueError

        self.id_sibling = id_sibling


    def __str__(self):
        string = str(self.id)

        if self.troublesome: string += "C"
        else: string += "X"

        if self.red_mobility: string += "R"
        else: string += "X"

        return string


class Node():
    state = []
    cost = 0

    def __str__(self) -> str:
        return str(self.state)

    def __eq__(self, other: object) -> bool:
        return self.state == other.state

    def calculateCost():
        pass

    def isGoal(data: dict):
        pass

    def descendants(data: dict) -> tuple:
        """
        Returns a tuple of nodes, with their cost calculated
        """
        pass



def h1(node: Node) -> int:
    pass


def h2(node: Node) -> int:
    pass


def parser(input_file: str) -> dict:
    pass



def aStar(data: dict, heuristic: function):
    # list of nodes that have been visited but not all the neighbors inspected starting with the start node
    open = queue.PriorityQueue
    start_node = Node()

    open.put((0, start_node))

    # list of nodes that have been visited and the neighbors have also been inspected
    closed = set()

    while (not open.empty()):
        node = open.get()
        if node.isGoal(data):
            return node.cost
        if node in closed:
            continue
        
        children = node.descendants(data)

        for child in children:
            # insert each child in order of f(child)
            f = heuristic(child) + child.cost
            open.put((f, child))
        
        closed.add(node)

    return {}


def main():
    print("Reading", sys.argv[1], "\b...")
    data = parser(sys.argv[1])
    heuristic = sys.argv[2]
    
    if heuristic == 1: heuristic = h1
    if heuristic == 2: heuristic = h2

    aStar(data, heuristic)

    


if __name__ == "__main__":
    main()
