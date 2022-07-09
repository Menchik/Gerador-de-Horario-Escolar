from gui import openGUI
from getInput import returnInput
from solver import solve

def main():
    openGUI()
    solution = solve(returnInput())
    if solution:
        printSolution(solution)
    else:
        print("No solution was found, try changing the input")


def printSolution(solution):
    print(solution)

if __name__ == "__main__":
    main()