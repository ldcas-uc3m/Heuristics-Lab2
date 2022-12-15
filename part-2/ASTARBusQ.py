import sys
import queue
import time as clock


# --------
# CLASSES
# --------

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

    def __str__(self) -> str:
        string = str(self.id)

        if self.troublesome: string += "C"
        else: string += "X"

        if self.red_mobility: string += "R"
        else: string += "X"

        # return string + "-" + str(self.seat)
        return string

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class Node():
    """
    Search tree node definition
    """

    def __init__(self, current_state: list = [], current_cost: int = 0, current_student_costs = [], buffer: int = 0):
        self.state = current_state  # state of the queue
        self.cost = current_cost  # cost from start to node
        self.student_costs = current_student_costs  # cost contribution of each individual student
        self.f = 0  # estimated cost from start to goal, through node

        self.buffer = buffer  # buffered cost of the last reduced mobility student

    def __str__(self) -> str:
        return str({
            "state": self.state,
            "cost": self.cost,
            "student costs": self.student_costs,
            "buffer": self.buffer,
        })

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        return self.state == other.state

    def __lt__(self, other: object) -> bool:
        return self.f < other.f

    def __hash__(self) -> int:
        return hash(tuple(self.state))


    def isGoal(self, data: dict) -> bool:
        """
        Check if the current state is a goal state
        """
        # the goal is reached when the queue is full and the last student in the queue is not a student with reduced mobility
        return len(self.state) == len(data) and not self.state[-1].red_mobility


    def generateDescendants(self, data: tuple, heuristic) -> tuple:
        """
        Returns a tuple of the posible descendants (nodes) of the current node,
        given the data of the problem
        """
        descendants = []
        for student in data:
            # a student can be added to the queue if he is not already in the queue
            if student in self.state: continue
            # a student with reduced mobility can only be added to the queue if the last student in the queue is not a student with reduced mobility
            if len(self.state) > 0 and self.state[-1].red_mobility and student.red_mobility: continue
            # the cost of a regual student is 1 and a reduced mobility student is 3
            student_cost = 1
            if student.red_mobility: student_cost = 0
            # Create a new node with the new state, current cost and state_costs and add it to the list of descendants
            newNode = Node(self.state + [student], self.cost, self.student_costs + [student_cost], self.buffer)
            newNode.update(data, heuristic)
            descendants.append(newNode)
        
        return tuple(descendants)


    def updateCost(self):
        """
        Update the cost of the state, taking into account a new student has been inserted
        """
        current_student = self.state[-1]
        current_student_cost = self.student_costs[-1]

        # we define the cost of a reduced mobility as 0,
        # and the cost of the one behind him his "real" (or "buffered") cost
        if current_student.red_mobility:
            # allocate its real cost to the buffer
            self.buffer = 3
            
        if len(self.state) > 1: 
            
            student_in_front = self.state[-2]
            student_in_front_cost = self.student_costs[-2]

            # A student that is in the queue right behind a student with reduced mobility must help them get on the bus. 
            # Because of this, the time taken by the next student is the time of the reduced mobility student (stored in the buffer)
            if student_in_front.red_mobility:
                # unload buffer
                current_student_cost = self.buffer
                self.buffer = 0
                # if a troublesome student helps a student with reduced mobility enter the bus,
                # the time taken by both of them would be double
                if(current_student.troublesome):
                    current_student_cost *= 2
            
            # A troublesome student will double the time the students behind them take to enter the bus
            if student_in_front.troublesome and not student_in_front.red_mobility:
                current_student_cost *= 2
                self.buffer *= 2

            # A troublesome student will double the time the students in front of them take to enter the bus
            if current_student.troublesome:
                student_in_front_cost *= 2
                self.buffer *= 2

            # A troublesome student will double the time the students behind of them take to enter the bus if their seat is higher
            for student in self.state:
                if current_student == student: continue

                if student.troublesome and not student_in_front.red_mobility and student.seat < current_student.seat:
                    current_student_cost *= 2
                    self.buffer *= 2
            
            # Update the costs of the students
            self.student_costs[-2] = student_in_front_cost

        # Update the costs of the  current student
        self.student_costs[-1] = current_student_cost
            
        # the total cost of the queue is the sum of the costs of each student
        self.cost = sum(self.student_costs)


    def update(self, data, heuristic):
        """
        Update the node, taking into account a new student has been inserted
        """
        self.updateCost()
        self.f = heuristic(data, self) + self.cost


# --------
# HEURISTICS
# --------

def h1(data: tuple, node: Node) -> int:
    """
    Heuristic 1: The cost of getting to the solution is the
    number of students left to position in the queue
    """
    return len(data) - len(node.state)


def h2(data: tuple, node: Node) -> int:
    """
    Heuristic 2: Take reduced mobility and troublesome rules (except double the ones w/ higher seat)
    with worst-case scenario
    """

    heuristic_cost = 0

    # if the last student in the queue is a reduced mobility one, the cost will increase
    # by at least 3
    if node.state[-1].red_mobility:
        heuristic_cost += 3

    # search for future students
    for student in data:
        if student in node.state:
            continue
        
        # each aditional student will add, at least, some extra cost
        if student.troublesome:
            # worst-case: only one troublesome at the end, behind a regular student that is sitting
            # behind a reduced mobility (so we don't double the cost)
            heuristic_cost += 2

        if student.red_mobility:
            # worst-case: student behind is a regular student
            heuristic_cost += 3

        if not student.troublesome and not student.red_mobility:  # regular student
            heuristic_cost += 1

    return heuristic_cost


# --------
# FUNCTIONS
# --------

def parser(input_file: str) -> tuple:
    """
    Parse the input file and create the problem data tuple
    """

    data = []

    with open(input_file, "r") as f:
        input = eval(f.read())  # dict

    for student in input:
        data.append(Student(student[0], student[1], student[2], input[student]))

    return tuple(data)


def printSolution(input_file: str, solution: Node, time: int, expanded_nodes: int, heuristic: int):
    """
    Print the solution and the stats to the files
    """
    # read initial state
    with open(input_file, "r") as f:
        input = eval(f.read())

    # write solution file
    solution_file = ".".join(input_file.split(".")[:-1]) + "-h" + str(heuristic) + ".output"

    with open(solution_file, "w") as f:
        
        # write initial state
        f.write("INITIAL: " + str(input) + "\n")
        if solution is None:
            return

        # parse solution
        parsed_solution = {}
        for student in solution.state:
            parsed_solution[str(student)] = student.seat

        f.write("FINAL:   " + str(parsed_solution))

    # write stats file
    stats_file = ".".join(input_file.split(".")[:-1]) + "-h" + str(heuristic) + ".stat"

    with open(stats_file, "w") as f:
        f.write("Total time: " + str(int(time * 1000)) + "\n")  # ms
        f.write("Total cost: " + str(solution.cost) + "\n")
        f.write("Plan length: " + str(len(solution.state)) + "\n")
        f.write("Expanded nodes: " + str(expanded_nodes) + "\n")

        # print(solution)


def aStar(data: tuple, heuristic):

    open = queue.PriorityQueue()  # list of nodes that have been visited but not expanded

    # set initial node
    start_node = Node()
    open.put(start_node)

    closed = set()  # set of expanded nodes

    while (not open.empty()):
        # get the best node according to f(n)
        node = open.get()

        if node.isGoal(data):
            return node, len(closed)  # solution found
        if node in closed:
            continue
        
        # expand node
        children = node.generateDescendants(data, heuristic)

        for child in children:
            # insert each child in order of f(n)
            open.put(child)
        
        # close node
        closed.add(node)

    return None  # no solution found


# --------
# MAIN
# --------

def main():

    # read and parse arguments
    print("Reading", sys.argv[1], "\b...")
    PATH = sys.argv[1]
    data = parser(PATH)
    h = int(sys.argv[2])
    
    if h == 1: heuristic = h1
    if h == 2: heuristic = h2

    # solve the problem
    print("Finding solution using heuristic", h,"\b...")
    tic = clock.perf_counter()
    solution, expanded_nodes = aStar(data, heuristic)
    toc = clock.perf_counter()

    time = toc - tic

    # print the solution
    if solution is None:
        print("Solution not found!")
    else:
        print("Solution found!")

    printSolution(PATH, solution, time, expanded_nodes, h)



if __name__ == "__main__":
   main()
