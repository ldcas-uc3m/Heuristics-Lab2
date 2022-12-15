from ASTARBusQ import *

def test_Node_updateCost():

    # test 1
    print("Node.updateCost() test 1")
    node = Node()

    student1 = Student(1, "C", "X", 1)
    student2 = Student(2, "X", "R", 2) 
    student3 = Student(3, "X", "X", 3)
    student4 = Student(4, "C", "X", 4)


    node.state = [student1]
    node.student_costs = [1]
    
    node.updateCost()
    print(str(node))
    
    assert node.student_costs == [1]
    assert node.cost == 1


    node.state = [student1, student2]
    node.student_costs = [1, 0]
    
    node.updateCost()
    print(str(node))
    
    assert node.student_costs == [1, 0]
    assert node.cost == 1


    node.state = [student1, student2, student3]
    node.student_costs = [1, 0, 1]
    
    node.updateCost()
    print(str(node))
    
    assert node.student_costs == [1, 0, 12]
    assert node.cost == 13


    node.state = [student1, student2, student3, student4]
    node.student_costs = [1, 0, 12, 1]
    
    node.updateCost()
    print(str(node))

    assert node.student_costs == [1, 0, 24, 2]
    assert node.cost == 27
    

    # test 2
    print("Node.updateCost() test 2")
    node = Node()


    student1 = Student(1, "C", "R", 20)
    student2 = Student(2, "C", "X", 32) 
    student3 = Student(3, "X", "X", 11)

    node.state = [student1]
    node.student_costs = [0]
    
    node.updateCost()
    print(str(node))
    
    assert node.student_costs == [0]
    assert node.cost == 0


    node.state = [student1, student2]
    node.student_costs = [0, 1]
    
    node.updateCost()
    print(str(node))
    
    assert node.student_costs == [0, 6]
    assert node.cost == 6


    node.state = [student1, student2, student3]
    node.student_costs = [0, 6, 1]
    
    node.updateCost()
    print(str(node))
    
    assert node.student_costs == [0, 6, 2]
    assert node.cost == 8



def test_Node_generateDescendants():
    print("Node.generateDescendants() test")
    
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
    descendants = first_node.generateDescendants(data)

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


def test_printSolution():
    print("printSolution() test")

    PATH = "ASTAR-tests/students1.prob"
    solution = Node()
    solution.state = [Student(69, "C", "R", 420)]
    heuristic = 1
    time = 1
    expanded_nodes = 1

    printSolution(PATH, solution, time, time, expanded_nodes, heuristic)


if __name__ == "__main__":
    test_Node_updateCost()
    test_Node_generateDescendants()
    test_printSolution()
