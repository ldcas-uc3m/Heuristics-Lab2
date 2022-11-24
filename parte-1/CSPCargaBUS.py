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
            line = line.strip('\n')
            #make a tuple of characteristics per student by splitting the line by commas, and if characteristic is a number, convert it to an int
            student_data = [int(x) if x.isdigit() else x for x in line.split(",")]
            data.append(Student(student_data[0], student_data[1], student_data[2], student_data[3], student_data[4]))
    return tuple(data)


def putVariables(data: tuple, problem: Problem):
    '''
    Adds the variables to the problem, using the data
    '''
    domain = [i for i in range(1, 33)]
    domain_front = [i for i in range(1, 17)]
    domain_back = [i for i in range(17, 33)]
    domain_blue = [i for i in range(1, 5)] + [i for i in range(13, 21)]

    for student in data:
        print(str(student))
        if student.id_sibling != 0:
            sibling = data[student.id_sibling - 1]
            print("Student " + str(student.id) + " has sibling " + str(sibling.id))
            if sibling.year != student.year:
                domain = domain_front
            if sibling.red_mobility: 
                match sibling.year:
                    case 1:
                        domain = domain_front
                    case 2:
                        domain = domain_back
        else:
            match student.year:
                case 1:
                    domain = domain_front
                case 2:
                    domain = domain_back
        if student.red_mobility:
            domain = domain_blue
            
        problem.addVariable(str(student), domain)

        

def putConstraints(data: tuple, problem: Problem):
    '''
    Adds the constraints to the problem, using the data         
    '''
    
    # Each student has one and only one seat assigned
    problem.addConstraint(AllDifferentConstraint())
    
    # If two students are siblings they must be seated next to each other
    for student in data:
        sibling = data[student.id_sibling - 1]
        if (student.id_sibling != 0):
                problem.addConstraint(are_adjacent, (str(student),  str(sibling)))
                for student2 in data:
                    # Troublesome students cannot sit close to other troublesome students or to any student with reduced mobility
                    if (student.troublesome or student.red_mobility) and student2.troublesome:
                        problem.addConstraint(not_close, (str(student), str(student2)))

                    # If there are students with reduced mobility, the seat right next to them has to be empty.
                    if (student.red_mobility and (student.id != student2.id)):
                        problem.addConstraint(next_seat_free, (str(student), str(student2)))
                    

def solver(problem: Problem):
    '''
    Solves the problem and prints out the solutions
    '''
    sol = problem.getSolution()

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