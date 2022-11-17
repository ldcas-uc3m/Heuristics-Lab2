from constraint import *
import sys


DOMAIN = (i for i in range(1, 33))


class Student(id, year, troublesome, red_mobility, id_sibling):
    '''
    Student definition
    '''

    def __init__(self):
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
        string = str(id)

        if self.troublesome: string += "C"
        else: string += "X"

        if self.red_mobility: string += "R"
        else: string += "X"

        return string


# ---
# AUX FUNCTIONS
# ---

def parser(path: str) -> tuple:
    '''
    Parses the input file specified in path and returns a tuple
    of Student classes
    '''
    data = []

    # TODO: parser

    pass

    return tuple(data)


def are_adjacent(a: int, b: int) -> bool:
    '''
    Returns True if seats a and b are adjacent, else False
    '''
    # TODO: double check the math
    return (abs(a - b) == 1) and (((a - 1) // 4) == ((b - 1) // 4)) and ((a % 4) * (b % 4) != 6)


def in_row(a: int, b: int) -> bool:
    '''
    Returns True if a and b are in the same row, else False
    '''
    # TODO: double check the math
    return ((a - 1) // 4) == ((b - 1) // 4)


def surroundings(s) -> list:
    '''
    Returns a list of all seats surrounding seat s
    '''
    seats = []

    # TODO: surroundings

    pass

    return seats


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


def in_blue(r: int) -> bool:
    '''
    Check if the seat r is a blue seat (for students w/ reduced mobility)
    '''
    return s in range(1, 5) or s in range(13, 17) or s in range(13, 21)


def not_close(s: int, t: int) -> bool:
    '''
    Check if seat s is surrounding seat t
    '''
    return s not in surroundings(t)


def next_seat_free(s: int, r: int) -> bool:
    '''
    Check if seat s is empty next to seat t
    '''
    return not are_adjacent(r, s)


# ---
# MAIN
# ---

def main():

    data = parser(sys.argv[1])

    problem = Problem()

    # VARIABLES

    # TODO: variables


    # CONSTRAINTS

    # Each student has one and only one seat assigned
    problem.addConstraint(AllDifferentConstraint())
    
    # Troublesome students cannot sit close to other troublesome students or to any student with reduced mobility
    for i in data:
        if i.troublesome or i.red_mobility:
            for j in data:
                if j.troublesome:
                    problem.addConstraint(not_close, (str(i), str(j)))

    # If there are students with reduced mobility, they will have to sit on seats designated for this purpose
    for i in data:
        if i.red_mobility:
            problem.addConstraint(in_blue, (str(i)))

    # If there are students with reduced mobility, the seat right next to them has to be empty.
    for i in data:
        if i.red_mobility:
            for j in data:
                if i != j:
                    problem.addConstraint(next_seat_free, (str(i), str(j)))

    # First year students must use seats in the front of the bus
    for i in data:
        if i.year == 1:
            problem.addConstraint(in_front, )

    # If two students are siblings they must be seated next to each other
    for i in data:
        if i.id_sibling != 0:
            for j in data:
                if i.id_sibling == j.id:
                    problem.addConstraint(are_adjacent, (str(i), str(j)))


    # SOLUTIONS

    sols = problem.getSolutions()
    print("Number of solutions:", len(sols))
    sol = problem.getSolution()
    print("One solution:\n", sol)


if __name__ == "__main__":
    main()