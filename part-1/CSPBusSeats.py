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
    Returns True if seat1 and seat2 are adjacent, else False
    '''
    return (abs(seat1 - seat2) == 1) and (((seat1 - 1) // 4) == ((seat2 - 1) // 4)) and ((seat1 % 4) * (seat2 % 4) != 6)


def in_row(seat1: int, seat2: int) -> bool:
    '''
    Returns True if seat1 and seat2 are in the same row, else False
    '''
    return ((seat1 - 1) // 4) == ((seat2 - 1) // 4)


def neighbors(seat: int) -> tuple:
    '''
    Returns a list of all neighboring seats of seat
    '''

    neighboring_seats = []

    # add front row seats
    if (seat - 1) // 4 > 0:  # seat is not on the first row
        # add seat in front
        neighboring_seats.append(seat - 4)
        # add the top-left seat, if there is one
        if in_row(seat - 4, seat - 5):
            neighboring_seats.append(seat - 5)
        # add the top-right seat, if there is one
        if in_row(seat - 4, seat - 3):
            neighboring_seats.append(seat - 3)
    
    # add same left seat, if there is one
    if in_row(seat, seat - 1):
        neighboring_seats.append(seat - 1)
        
    # add same right seat, if there is one
    if in_row(seat, seat + 1):
        neighboring_seats.append(seat + 1)

    # add back row seats
    if (seat - 1) // 4 < 7:  # seat is not on the last row
        # add seat in back
        neighboring_seats.append(seat + 4)
        # add the bottom-left seat, if there is one
        if in_row(seat + 4, seat + 3):
            neighboring_seats.append(seat + 3)
        # add the bottom-right seat, if there is one
        if in_row(seat + 4, seat + 5):
            neighboring_seats.append(seat + 5)
    

    return tuple(neighboring_seats)


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


def in_aisle(s: int, t: int) -> bool:
    '''
    Check if seat s is in the aisle
    '''
    # For some weird f*ing reason, if it doesn't have two parameters,
    #  it doesn't work when adding constraints
    return (s - 1) % 4 in (1, 2)



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
            # make a tuple of characteristics per student by splitting the line by commas, and if characteristic is a number, convert it to an int
            student_data = [int(x) if x.isdigit() else x for x in line.split(",")]
            data.append(Student(student_data[0], student_data[1], student_data[2], student_data[3], student_data[4]))

    return tuple(data)


def putVariables(data: tuple, problem: Problem):
    '''
    Adds the variables to the problem, using the data.
    We constraint the domain (possible seats) depending on the
    student's data.
    '''

    domain = [i for i in range(1, 33)]
    domain_front = [i for i in range(1, 17)]
    domain_back = [i for i in range(17, 33)]
    domain_blue = [i for i in range(1, 5)] + [i for i in range(13, 21)]

    for student in data:
        # siblings
        if student.id_sibling != 0: 
            sibling = data[student.id_sibling - 1]
            if sibling.year != student.year:  # siblings in different years
                domain = domain_front
            if sibling.red_mobility:
                # the other sibling must seat in the same area (front or back)
                match sibling.year:
                    case 1:
                        domain = domain_front
                    case 2:
                        domain = domain_back
        # years
        else:
            match student.year:
                case 1:
                    domain = domain_front
                case 2:
                    domain = domain_back

        # reduced mobility
        if student.red_mobility:
            # must seat in the corresponding area (front or back), in the blue seats
            domain = [seat for seat in domain if seat in domain_blue]
        
        problem.addVariable(str(student), domain)


def putConstraints(data: tuple, problem: Problem):
    '''
    Adds the constraints to the problem, using the data         
    '''
    
    # Each student has one and only one seat assigned
    problem.addConstraint(AllDifferentConstraint())
    
    counted_siblings = set()  # to prevent counting siblings twice

    for student in data:
        # If two students are siblings they must be seated next to each other
        if (student.id_sibling != 0):
            sibling = data[student.id_sibling - 1]
            if str(sibling) not in counted_siblings:
                problem.addConstraint(are_adjacent, (str(student), str(sibling)))

                # If siblings are on different years, the older brother has to be assigned the seat closer to the aisle.
                if student.year > sibling.year:
                    problem.addConstraint(in_aisle, (str(student), str(sibling)))
                elif student.year < sibling.year:
                    problem.addConstraint(in_aisle, (str(sibling), str(student)))
                
                counted_siblings.add(str(sibling))

        for student2 in data:
            # Troublesome students cannot sit close to other troublesome students or to any student with reduced mobility
            if (student.troublesome or student.red_mobility) and student2.troublesome:
                problem.addConstraint(not_close, (str(student), str(student2)))

            # If there are students with reduced mobility, the seat right next to them has to be empty.
            if (student.red_mobility and (student.id != student2.id)):
                problem.addConstraint(next_seat_free, (str(student), str(student2)))
                

def solver(problem: Problem, output_file_name: str):
    '''
    Solves the problem and writes out the solutions
    '''
    sols = problem.getSolutions()

    with open(output_file_name, "w") as f:
        f.write("Number of solutions: " + str(len(sols)) + "\n")
        for i in range(0,3):
            f.write(str(sols[i]) + "\n")
        f.close()


# ---
# MAIN
# ---

def main():

    print("Reading", sys.argv[1], "\b...")
    data = parser(sys.argv[1])

    problem = Problem()

    print("Adding variables...")
    putVariables(data, problem)

    print("Adding constraints...")
    putConstraints(data, problem)

    output_file_name = sys.argv[1] + ".out"

    print("Getting solutions...")
    solver(problem, output_file_name)


if __name__ == "__main__":
    main()