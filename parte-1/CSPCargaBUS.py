from constraint import *
import sys


DOMAIN_SETS = {  # sets of the domain
    "full": [i for i in range(1, 33)],  # all seats
    "front": [i for i in range(1, 17)],  # seats on the front of the bus
    "back": [i for i in range(17, 33)],  # seats on the back of the bus
    "reduced": [i for i in range(1, 5)] + [i for i in range(13, 17)] + [i for i in range(13, 21)]  # seats for reduced mobility students
}


def parser(path) -> list:
    '''
    Parses the input file specified in path and returns a matrix
    with the following format:
    [
        [<possible seats for student 0>],
        [<possible seats for student 1>],
        ...
    ]
    '''


# ---
# CONSTRAINTS
# ---



# ---
# MAIN
# ---

def main():

    domains = parser(sys.argv[1])

    problem = Problem()

    # constraints
    problem.addConstraint(AllDifferentConstraint())  # each student seats in a different seat
    


if __name__ == "__main__":
    main()