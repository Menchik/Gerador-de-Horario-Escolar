#################################################################################
# Inspired by https://coin-or.github.io/pulp/CaseStudies/a_sudoku_problem.html  #
# Highly recommend reading it as the code is not intuitive at all               #
#################################################################################

import pulp as plp

def printSolution(solution, days, classes, grades):

    # Print the final result
    print(f"Final result:")
    
    for grade in grades:
        print(f"GRADE {grade}:\n+ ------- + ------- + ------- +",end="\n")
        for day in days:
            print
            print(f"DAY {day}:")
            for clas in classes:
                print(solution[day][clas][grade],end=" | ")
            print("\n+ ------- ",end="\n")

def extract_solution(grid_vars, days, classes, grades, teachers):
    solution = [[[0 for grade in grades] for clas in classes] for day in days]
    for day in days:
        for clas in classes:
            for grade in grades:
                for teacher in teachers:
                    if plp.value(grid_vars[day][clas][grade][teacher]):
                        solution[day][clas][grade] = teacher 
    return solution

def solve(days, classes, grades, teachers, available_time, available_classes, necessary_classes):
    # Create the linear programming problem
    prob = plp.LpProblem("School_Scheduler")

    # Decision Variable/Target variable
    grid_vars = plp.LpVariable.dicts("grid_value", (days,classes,grades,teachers), cat='Binary')

    # There is no objetive function since every solution is equally valid (for now)

    # Create all of the constraints needed for the problem
    add_constraints(prob, grid_vars, days, classes, grades, teachers, available_time, available_classes, necessary_classes)

    # Solve the problem given all constraints
    prob.solve()

    # Print the status of the solution
    solution_status = plp.LpStatus[prob.status]
    print(f'Solution Status = {solution_status}')

    # Print the solution if an optimal one has been identified
    if solution_status == 'Optimal':
        solution = extract_solution(grid_vars, days, classes, grades, teachers)
        printSolution(solution, days, classes, grades)
        return solution
    return None

# Adds each of the different types of contraints to the problem
def add_constraints(prob, grid_vars, days, classes, grades, teachers, available_time, available_classes, necessary_classes):

    add_scheduler_constraints(prob, grid_vars, days, classes, grades, teachers)
    #add_teachers_constraints(prob, grid_vars, days, classes, grades, teachers, available_time)
    add_grades_constraints(prob, grid_vars, days, classes, grades, teachers, available_classes, necessary_classes)

# Adds the default constraints of a scheduler to the LP problem
def add_scheduler_constraints(prob, grid_vars, days, classes, grades, teachers):

    # Constraint to ensure only one teacher is assigned a especific class of a grade in a day
    for day in days:
        for clas in classes:
            for grade in grades:
                prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher] for teacher in teachers]),
                                                    sense= plp.LpConstraintEQ,
                                                    rhs= 1,
                                                    name= f"constraint_sum_{day}_{clas}_{grade}"))

    # Constraint to ensure a teacher will not be assigned two classes at the same time
    for day in days:
        for clas in classes:
            for teacher in teachers:
                prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher]*teacher for grade in grades]),
                                                    sense= plp.LpConstraintEQ,
                                                    rhs= teacher,
                                                    name= f"constraint_uniq_grade_{day}_{clas}_{grade}_{teacher}"))

# Adds the grades constraints to the problem
def add_grades_constraints(prob, grid_vars, days, classes, grades, teachers, available_classes, necessary_classes):

    # Constraint to ensure only classes available to the grade are used
    for day in days:
        for clas in classes:
            for grade in grades:
                if (available_classes[day][clas][grade]):
                    prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher] for teacher in teachers]),
                                                        sense= plp.LpConstraintEQ,
                                                        rhs= available_classes[day][clas][grade],
                                                        name= f"constraint_not_available_{day}_{clas}_{grade}"))

    # Constraint to ensure the grades has the necessary amount of classes from every teacher
    # for teacher in teachers:
    #     for grade in grades:
    #         prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher] for clas in classes for day in days]),
    #                                             sense= plp.LpConstraintEQ,
    #                                             rhs= necessary_classes[teacher][grade],
    #                                             name= f"constraint_necessary_amount_of_classes_{teacher}_{grade}"))


#Adds the teachers constraints to the problem
def add_teachers_constraints(prob, grid_vars, days, classes, grades, teachers, available_time):

    # Constraint to ensure only classes available by the teacher are considered
    for teacher in teachers:
        for day in days:
            for clas in classes:
                prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher] for grade in grades]),
                                                    sense= plp.LpConstraintLE,
                                                    rhs = available_time[teacher][day][clas],
                                                    name= f"constraint_teacher_available_classes_{teacher}_{day}_{clas}"))


if __name__ == "__main__":
    print("This file can't be executed on its own, try main.py")