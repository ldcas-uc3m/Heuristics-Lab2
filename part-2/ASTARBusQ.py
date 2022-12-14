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
    def __init__(self, current_state: list = [], current_cost: int = 0, current_state_costs =[]):
        self.state = current_state
        self.cost = current_cost
        self.student_costs = current_state_costs

    def __str__(self) -> str:
        return str({
            "state": self.state,
            "cost": self.cost,
            "student costs": self.student_costs
        })

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        return self.state == other.state

    def __lt__(self, other: object) -> bool:
        return self.cost < other.cost


    def updateCost(self):
        """
        Update the cost of the node
        """
        if len(self.state) > 1: 
            current_student = self.state[-1]
            current_student_cost = self.student_costs[-1]

            student_in_front = self.state[-2]
            student_in_front_cost = self.student_costs[-2]

            # A student that is in the queue right behind a student with reduced mobility must help them get on the bus. Because of this, the time taken by the next student is the time of the reduced mobility student
            if student_in_front.red_mobility:
                current_student_cost = student_in_front_cost
                student_in_front_cost = 0
                # if a troublesome student helps a student with reduced mobility enter the bus, the time taken by both of them would be double
                if(current_student.troublesome):
                    current_student_cost *= 2
            
            # A troublesome student will double the time the students behind them take to enter the bus.
            if student_in_front.troublesome:
                current_student_cost *= 2

            # A troublesome student will double the time the students in front of them take to enter the bus.
            if current_student.troublesome:
                student_in_front_cost *= 2
        
            # A troublesome student will double the time the students behind of them take to enter the bus if their seat is higher
            for student in self.state:
                if student.troublesome and not student_in_front.red_mobility and student.seat < current_student.seat:
                    if student_in_front != student:
                        current_student_cost *= 2

            #Update the costs of the students
            self.student_costs[-1] = current_student_cost
            self.student_costs[-2] = student_in_front_cost
            
        # the total cost of the queue is the sum of the costs of each student
        self.cost = sum(self.student_costs)

    def isGoal(self, data: dict):
        # the goal is reached when the queue is full and the last student in the queue is not a student with reduced mobility
        return len(self.state) == len(data) and not self.state[-1].red_mobility

    def descendants(self, data: tuple) -> tuple:
        descendant = []
        for student in data:
            # a student can be added to the queue if he is not already in the queue
            if student in self.state: continue
            # a student with reduced mobility can only be added to the queue if the last student in the queue is not a student with reduced mobility
            if len(self.state) > 0 and self.state[-1].red_mobility and student.red_mobility: continue
            # the cost of a regual student is 1 and a reduced mobility student is 3
            student_cost = 1
            if student.red_mobility: student_cost = 3
            # Create a new node with the new state, cost and state_costs and add it to the list of descendants
            newNode = Node(self.state + [student], self.cost, self.student_costs + [student_cost])
            newNode.updateCost()
            descendant.append(newNode)
        
        return tuple(descendant)
        

def test_node_updateCost():
    first_node = Node()

    student1 = Student(1, "C", "X", 1)
    student2 = Student(2, "X", "R", 2) 
    student3 = Student(3, "X", "X", 3)
    student4 = Student(4, "C", "X", 4)

    state = [student1]
    student_costs = [1]
    first_node.state = state
    first_node.student_costs = student_costs
    first_node.updateCost()
    assert first_node.cost == 1
    assert first_node.student_costs == [1]
    print(str(first_node))

    state = [student1, student2]
    student_costs = [1, 3]
    first_node.state = state
    first_node.student_costs = student_costs
    first_node.updateCost()
    assert first_node.cost == 7
    assert first_node.student_costs == [1, 6]
    print(str(first_node))

    state = [student1, student2, student3]
    student_costs = [1, 6, 1]
    first_node.state = state
    first_node.student_costs = student_costs
    first_node.updateCost()
    assert first_node.cost == 7
    assert first_node.student_costs == [1, 0, 6]
    print(str(first_node))


    state = [student1, student2, student3, student4]
    student_costs = [1, 0, 6, 1]
    first_node.state = state
    first_node.student_costs = student_costs
    first_node.updateCost()
    assert first_node.cost == 15
    assert first_node.student_costs == [1, 0, 12, 2]
    print(str(first_node))

def test_node_descendants():
    first_node = Node()

    student1 = Student(1, "C", "X", 1)
    student2 = Student(2, "X", "R", 2) 
    student3 = Student(3, "X", "X", 3)
    student4 = Student(4, "X", "R", 4)

    student5 = Student(5, "X", "R", 5)
    student6 = Student(6, "X", "X", 6)
    student7 = Student(7, "C", "X", 7)
    student8 = Student(8, "X", "X", 8)

    state = [student1, student2, student3, student4]
    student_costs = [1, 0, 6, 6]
    first_node.state = state
    first_node.student_costs = student_costs

    data= (student5, student6, student7, student8)
    descendants = first_node.descendants(data)

    assert descendants[0].state == [student1, student2, student3, student4, student6]
    assert descendants[0].student_costs == [1, 0, 6, 0, 6]
    assert descendants[0].cost == 13

    assert descendants[1].state == [student1, student2, student3, student4, student7]
    assert descendants[1].student_costs == [1, 0, 6, 0, 12]
    assert descendants[1].cost == 19

    assert descendants[2].state == [student1, student2, student3, student4, student8]
    assert descendants[2].student_costs == [1, 0, 6, 0, 6]
    assert descendants[2].cost == 13
    
    print(descendants)


   


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
    test_node_updateCost()
    test_node_descendants()
   # main()
