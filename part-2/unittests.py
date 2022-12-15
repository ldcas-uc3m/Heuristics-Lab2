from ASTARBusQ import *

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


def test_parsers():
    PATH = sys.argv[1]
    solution = Node()
    solution.state = [Student(69, "C", "R", 420)]
    time = 1
    expanded_nodes = 1

    printSolution(PATH, solution, time, expanded_nodes, sys.argv[2])


if __name__ == "__main__":
    test_node_updateCost()
    test_node_descendants()
    test_parsers()
