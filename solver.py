#################################################################################
# Inspired by https://coin-or.github.io/pulp/CaseStudies/a_sudoku_problem.html  #
# Highly recommend reading it as the code is not intuitive at all               #
#################################################################################

import pulp as plp

nomes=["maria", "joao", "####"]

def printSolution(solution, days, classes, grades):

    # Print the final result
    print(f"Final result:")
    
    for day in days:
        print(f"\nDIA {day}:", end="")
        for clas in classes:
            print(f"\n    AULA {clas}:\n        |   T1  |  T2  |", end="\n        | ")
            for grade in grades:
                print(solution[day][clas][grade],end=" | ")

def extract_solution(grid_vars, days, classes, grades, teachers):
    solution = [[[0 for grade in grades] for clas in classes] for day in days]
    for day in days:
        for clas in classes:
            for grade in grades:
                for teacher in teachers:
                    if plp.value(grid_vars[day][clas][grade][teacher]):
                        solution[day][clas][grade] = nomes[teacher]
    return solution

def solve(days, classes, grades, teachers, available_time, available_classes, necessary_classes):
    # Create the linear programming problem
    prob = plp.LpProblem("School_Scheduler")

    # Decision Variable/Target variable
    grid_vars = plp.LpVariable.dicts("grid_value", (days,classes,grades,teachers), cat='Binary')

    # There is no objetive function since every solution is equally valid (for now)

    # Create all of the constraints needed for the problem
    add_constraints(prob, grid_vars, days, classes, grades, teachers, available_time, available_classes, necessary_classes)

    prob.writeLP("filename.txt", writeSOS=1, mip=1, max_length=100)

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
    add_teachers_constraints(prob, grid_vars, days, classes, grades, teachers, available_time)
    add_grades_constraints(prob, grid_vars, days, classes, grades, teachers, available_classes, necessary_classes)

# Adds the default constraints of a scheduler to the LP problem
def add_scheduler_constraints(prob, grid_vars, days, classes, grades, teachers):

    # Constraint to ensure only one teacher is assigned a especific class of a grade in a day
    ############### WORKING ###############
    for day in days:
        for clas in classes:
            for grade in grades:
                prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher] for teacher in teachers]),
                                                    sense= plp.LpConstraintEQ,
                                                    rhs= 1,
                                                    name= f"constraint_sum_{day}_{clas}_{grade}"))

    # Constraint to ensure a teacher will not be assigned two classes at the same time
    ############### WORKING ###############
    for day in days:
        for clas in classes:
            for teacher in teachers[:-1]:
                prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher] for grade in grades]),
                                                    sense= plp.LpConstraintLE,
                                                    rhs= 1,
                                                    name= f"constraint_uniq_grade_{day}_{clas}_{teacher}"))

# Adds the grades constraints to the problem
def add_grades_constraints(prob, grid_vars, days, classes, grades, teachers, available_classes, necessary_classes):

    # Constraint to ensure only classes available to the grade are used
    ############### WORKING ###############
    for day in days:
        for clas in classes:
            for grade in grades:
                if (not available_classes[day][clas][grade]):
                    prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher]*teacher for teacher in teachers]),
                                                        sense= plp.LpConstraintEQ,
                                                        rhs= teachers[-1],
                                                        name= f"constraint_not_available_{day}_{clas}_{grade}"))

    # Constraint to ensure the grades has the necessary amount of classes from every teacher
    ############### WORKING ###############
    for grade in grades:
        for teacher in teachers[:-1]:
            prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher] for clas in classes for day in days]),
                                                sense= plp.LpConstraintEQ,
                                                rhs= necessary_classes[grade][teacher],
                                                name= f"constraint_necessary_amount_of_classes_{teacher}_{grade}"))
        # Constraint to enable None as an available teacher
        prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teachers[-1]]for clas in classes for day in days]),
                                            sense= plp.LpConstraintLE,
                                            rhs= len(days)*len(classes),
                                            name= f"constraint_necessary_amount_of_classes_{teachers[-1]}_{grade}"))


#Adds the teachers constraints to the problem
def add_teachers_constraints(prob, grid_vars, days, classes, grades, teachers, available_time):

    # Constraint to ensure only classes available by the teacher are considered
    ############### WORKING ###############
    for day in days:
        for clas in classes:
            for teacher in teachers[:-1]:
                prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher] for grade in grades]),
                                                    sense= plp.LpConstraintLE,
                                                    rhs = available_time[teacher][day][clas],
                                                    name= f"constraint_teacher_available_classes_{teacher}_{day}_{clas}"))


if __name__ == "__main__":
    print("This file can't be executed on its own, try main.py")