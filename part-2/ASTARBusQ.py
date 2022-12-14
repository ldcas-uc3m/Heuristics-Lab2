import sys
import queue
import time as clock


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



def h1(data: tuple, node: Node) -> int:
    """
    Heuristic 1: The cost of getting to the solution is the
    number of students left to position in the queue
    """
    return len(data) - len(node.state)


def h2(data: tuple, node: Node) -> int:
    """
    Heuristic 2: 
    """
    pass


def parser(input_file: str) -> tuple:

    data = []

    with open(input_file, "r") as f:
        input = eval(f.read())  # dict

    for student in input:
        data.append(Student(student[0], student[1], student[2], input[student]))

    return tuple(data)


def printSolution(input_file: str, solution: Node, time: int, expanded_nodes: int, heuristic):

    # read initial state
    with open(input_file, "r") as f:
        input = eval(f.read())

    # write solution file
    solution_file = ".".join(input_file.split(".")[:-1]) + "-h" + str(heuristic) + ".output"

    with open(solution_file, "w") as f:
        
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

    # write stats file
    stats_file = ".".join(input_file.split(".")[:-1]) + "-h" + str(heuristic) + ".stat"

    with open(stats_file, "w") as f:
        f.write("Total time: " + str(time) + "\n")
        f.write("Total cost: " + str(solution.cost) + "\n")
        f.write("Plan length: " + str(len(solution.state)) + "\n")
        f.write("Expanded nodes: " + str(expanded_nodes) + "\n")


def aStar(data: tuple, heuristic):
    expanded_nodes = 0  # expanded_nodes it takes to solve the problem

    # list of nodes that have been visited but not all the neighbors inspected starting with the start node
    open = queue.PriorityQueue()
    start_node = Node()

    open.put((0, start_node))

    # list of nodes that have been visited and the neighbors have also been inspected
    closed = set()

    while (not open.empty()):
        node = open.get()
        if node.isGoal(data):
            return node, expanded_nodes
        if node in closed:
            continue
        
        children = node.descendants(data)

        for child in children:
            # insert each child in order of f(child)
            f = heuristic(data, child) + child.cost
            open.put((f, child))
        
        closed.add(node)

        expanded_nodes += 1

    return None


def main():
    print("Reading", sys.argv[1], "\b...")
    PATH = sys.argv[1]
    data = parser(PATH)
    heuristic = sys.argv[2]
    
    if heuristic == 1: heuristic = h1
    if heuristic == 2: heuristic = h2

    tic = clock.perf_counter()
    solution, expanded_nodes = aStar(data, heuristic)
    toc = clock.perf_counter()

    time = int(toc - tic)

    printSolution(PATH, solution, time, expanded_nodes, sys.argv[2])
    
    
def test():
    PATH = sys.argv[1]
    solution = Node()
    solution.state = [Student(69, "C", "R", 420)]
    time = 1
    expanded_nodes = 1

    printSolution(PATH, solution, time, expanded_nodes, sys.argv[2])


if __name__ == "__main__":
    test()
    # main()
