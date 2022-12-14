import sys
import json
import queue


class Student(object):
    '''
    Student definition
    '''
    def __init__(self, id, year, troublesome, red_mobility, id_sibling, seat):
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

        self.seat = seat


    def __str__(self):
        string = str(self.id)

        if self.troublesome: string += "C"
        else: string += "X"

        if self.red_mobility: string += "R"
        else: string += "X"

        return string


class Node():

    def __init__(self, current_state: list = [], current_cost: int = 0, current_state_costs =[]):
        self.state = current_state
        self.cost = current_cost
        self.student_costs = current_state_costs

    def __str__(self) -> str:
        return str(self.state) 

    def __eq__(self, other: object) -> bool:
        return self.state == other.state

    def __lt__(self, other: object) -> bool:
        return self.cost < other.cost

    def calculateCost(self):
        new_cost = self.student_costs
        for i in range(len(new_cost)):
            # A student that is in the queue right behind a student with reduced mobility must help them get on the bus. Because of this, the time taken by the next student is the time of the reduced mobility student
            if self.state[i].red_mobility:
                new_cost[i+1] = new_cost[i]
                new_cost[i] = 0
                # if a troublesome student helps a student with reduced mobility enter the bus, the time taken by both of them would be double
                if(self.state[i+1].troublesome):
                    new_cost[i+1] *= 2
            if new_cost[i].troublesome:
                # A troublesome student will double the time the students in front and behind them take to enter the bus.
                new_cost[i+1] *= 2
                new_cost[i-1] *= 2
                #A troublesome student will double the needed to enter the bus for ALL students that are behind him in the queue and have an assigned seat that is higher than his
                for j in range(i+1, len(new_cost)):
                    if self.state[j].seat > self.state[i].seat:
                        new_cost[j] *= 2
        total_cost = 0
        for cost in new_cost:
            #the total cost of the queue is the sum of the costs of each student
            total_cost += cost
        return total_cost

    def isGoal(self, data: dict):
        # the goal is reached when the queue is full and the last student in the queue is not a student with reduced mobility
        return len(self.state) == len(data) and not self.state[-1].red_mobility

    def descendants(self, data: tuple) -> tuple:
        descendant = []
        for student in data:
            # a student can be added to the queue if he is not already in the queue
            if student in self.state: continue
            # a student with reduced mobility can only be added to the queue if the last student in the queue is not a student with reduced mobility
            if self.state[-1].red_mobility and student.red_mobility: continue
            # the cost of a regual student is 1 and a reduced mobility student is 3
            student_cost = 1
            if student.red_mobility: student_cost = 3
            # Create a new node with the new state, cost and state_costs and add it to the list of descendants
            descendant.append(Node(self.state + [student], self.calculateCost(), self.student_costs + [student_cost]))
        
        return tuple(descendant)

def test_node_descendants():
    first_node = Node()
    data = (Student(1, 1, "C", "X", 0, 1), Student(2, 1, "X", "X", 0, 2), Student(3, 1, "X", "R", 0, 3))


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
