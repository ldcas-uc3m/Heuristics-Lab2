import sys
import queue


class Student():
    '''
    Student definition
    '''
    def __init__(self, id: int, troublesome: str, red_mobility: str, seat: int):
        self.id = id

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

        self.seat = seat

    def __str__(self):
        string = str(self.id)

        if self.troublesome: string += "C"
        else: string += "X"

        if self.red_mobility: string += "R"
        else: string += "X"

        # return string + "-" + str(self.seat)
        return string

    def __repr__(self) -> str:
        return self.__str__()


class Node():
    state = []
    cost = 0

    def __str__(self) -> str:
        return str(self.state)

    def __eq__(self, other: object) -> bool:
        return self.state == other.state

    def calculateCost():
        pass

    def isGoal(data: tuple) -> int:
        pass

    def descendants(data: tuple) -> tuple:
        """
        Returns a tuple of nodes, with their cost calculated
        """
        pass



def h1(node: Node) -> int:
    pass


def h2(node: Node) -> int:
    pass


def parser(input_file: str) -> tuple:

    data = []

    with open(input_file, "r") as f:
        input = eval(f.read())  # dict

    for student in input:
        data.append(Student(student[0], student[1], student[2], input[student]))

    return tuple(data)


def printSolution(input_file: str, solution: Node):

    # compute output file path
    output_file = ".".join(input_file.split(".")[:-1]) + ".output"

    # read initial state
    with open(input_file, "r") as f:
        input = eval(f.read())

    # write output file
    with open(output_file, "w") as f:
        
        # write initial state
        f.write("INITIAL: " + str(input) + "\n")
        if solution is None:
            print("No solution was found")
            return

        # parse solution
        parsed_solution = {}
        for student in solution.state:
            parsed_solution[str(student)] = student.seat

        f.write("FINAL: " + str(parsed_solution))

    print("The cost was:", solution.cost)


def aStar(data: tuple, heuristic):
    # list of nodes that have been visited but not all the neighbors inspected starting with the start node
    open = queue.PriorityQueue
    start_node = Node()

    open.put((0, start_node))

    # list of nodes that have been visited and the neighbors have also been inspected
    closed = set()

    while (not open.empty()):
        node = open.get()
        if node.isGoal(data):
            return node
        if node in closed:
            continue
        
        children = node.descendants(data)

        for child in children:
            # insert each child in order of f(child)
            f = heuristic(child) + child.cost
            open.put((f, child))
        
        closed.add(node)

    return None


def main():
    print("Reading", sys.argv[1], "\b...")
    PATH = sys.argv[1]
    data = parser(PATH)
    heuristic = sys.argv[2]
    
    if heuristic == 1: heuristic = h1
    if heuristic == 2: heuristic = h2

    solution = aStar(data, heuristic)

    printSolution(data, solution, PATH)
    
    
def test():
    PATH = sys.argv[1]
    solution = Node()
    solution.state = [Student(69, "C", "R", 420)]

    printSolution(PATH, solution)

if __name__ == "__main__":
    # test()
    main()
