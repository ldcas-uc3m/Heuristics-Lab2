import sys
from constraint import *


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



# ---
# AUX FUNCTIONS
# ---

def front_row(seat: int) -> bool:
    '''
    Check if seat is in the front row
    '''
    return seat in range(1, 5)

def back_row(seat: int) -> bool:
    '''
    Check if seat is in the back row
    '''
    return seat in range(29, 33)

def are_adjacent(seat1: int, seat2: int) -> bool:
    '''
    Returns True if seats a and b are adjacent, else False
    '''
    return (abs(seat1 - seat2) == 1) and (((seat1 - 1) // 4) == ((seat2 - 1) // 4)) and ((seat1 % 4) * (seat2 % 4) != 6)


def in_row(seat1: int, seat2: int) -> bool:
    '''
    Returns True if a and b are in the same row, else False
    '''
    return ((seat1 - 1) // 4) == ((seat2 - 1) // 4)

def neighbors(seat) -> list:
    '''
    Returns a list of all neighboring seats of sit a
    '''
    neighboring_seats = []

    if in_row(seat, seat + 1):
        neighboring_seats.append(seat + 1)
    if in_row(seat, seat - 1):
        neighboring_seats.append(seat - 1)
    
    if front_row(seat):
        if in_row(seat-4, seat - 5):
            neighboring_seats.append(seat - 5)
            neighboring_seats.append(seat - 4)
        if in_row(seat-4, seat - 3):
            neighboring_seats.append(seat - 3)

    if back_row(seat):
        if in_row(seat + 4, seat + 3):
            neighboring_seats.append(seat + 3)
            neighboring_seats.append(seat + 4)
        if in_row(seat + 4, seat + 5):
            neighboring_seats.append(seat + 5)

    return neighboring_seats


# ---
# CONSTRAINT FUNCTIONS
# --- 

def in_front(s: int) -> bool:
    '''
    Check if seat s is in the fornt of the bus
    '''
    return s in range(1, 17)


def in_back(s: int) -> bool:
    '''
    Check if seat s is in the back of the bus
    '''
    return s in range(17, 33)


def in_blue(s: int) -> bool:
    '''
    Check if the seat r is a blue seat (for students w/ reduced mobility)
    '''
    return s in range(1, 5) or s in range(13, 17) or s in range(13, 21)


def not_close(s: int, t: int) -> bool:
    '''
    Check if seat s is surrounding seat t
    '''
    return s not in neighbors(t)


def next_seat_free(s: int, r: int) -> bool:
    '''
    Check if seat s is empty next to seat t
    '''
    return not are_adjacent(r, s)



# ---
# MAIN FUNCTIONS
# ---

def parser(path: str) -> tuple:
    '''
    Parses the input file specified in path and returns a tuple
    of Student classes
    '''
    data = []
    with open(path, "r") as f:
        for line in f:
            identity = int(line.split(",")[0])
            year = int(line.split(",")[1])
            troublesome = line.split(",")[2]
            red_mobility = line.split(",")[3]
            id_sibling = int(line.split(",")[4])
            data.append(Student(identity, year, troublesome, red_mobility, id_sibling))
    return tuple(data)


def putVariables(data: tuple, problem: Problem):
    '''
    Adds the variables to the problem, using the data
    '''
    for student in data:
        print(str(student))
        problem.addVariable(str(student), range(1, 33))

def putConstraints(data: tuple, problem: Problem):
    '''
    Adds the constraints to the problem, using the data
    '''
    # Each student has one and only one seat assigned
    problem.addConstraint(AllDifferentConstraint())
    
    for student in data:
        # First year students must use seats in the front of the bus
        if student.year == 1:
            problem.addConstraint(in_front, str(student))

        # Second year students must use seats in the back of the bus
        if student.year == 2:
            problem.addConstraint(in_back, str(student))
        
        # If two students are siblings they must be seated next to each other
        if (student.id_sibling != 0):

            print("Siblings: " + str(student) + " and " + str(data[student.id_sibling - 1]))
            problem.addConstraint(are_adjacent, (str(student), str(data[student.id_sibling - 1])))

            for student2 in data:
                # Troublesome students cannot sit close to other troublesome students or to any student with reduced mobility
                if (student.troublesome or student.red_mobility) and student.troublesome:
                    problem.addConstraint(not_close, (str(student),str(student2)))

                # If there are students with reduced mobility, the seat right next to them has to be empty.
                if student.red_mobility and (student.id != student2.id):
                    problem.addConstraint(next_seat_free, (str(student), str(student2)))



def solver(problem: Problem):
    '''
    Solves the problem and prints out the solutions
    '''
    sol = problem.getSolution()
    sols = problem.getSolutions()

    out_path = sys.argv[1].split("/")[-1] + ".out"
    print("One solution:\n", sol)




# ---
# MAIN
# ---

def main():

    data = parser(sys.argv[1])

    problem = Problem()

    putVariables(data, problem)

    putConstraints(data, problem)

    solver(problem)


if __name__ == "__main__":
    main()