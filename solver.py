#################################################################################
# Inspired by https://coin-or.github.io/pulp/CaseStudies/a_sudoku_problem.html  #
# Highly recommend reading it as the code is not intuitive at all               #
#################################################################################

import pulp as plp

def solve(days, classes, grades, teachers, available_classes, necessary_classes):
    # Create the linear programming problem
    prob = plp.LpProblem("School_Scheduler")

    # Decision Variable/Target variable
    grid_vars = plp.LpVariable.dicts("grid_value", (days,classes,grades,teachers), cat='Binary')

    # There is no objetive function since every solution is equally valid (for now)

    # Create all of the constraints needed for the problem
    add_constraints(prob, grid_vars, days, classes, grades, teachers, available_classes, necessary_classes)

    # Solve the problem given all constraints
    prob.solve()

    # Print the status of the solution
    solution_status = plp.LpStatus[prob.status]
    print(f'Solution Status = {solution_status}')

    # Print the solution if an optimal one has been identified
    if solution_status == 'Optimal':
        return prob.extract_solution(grid_vars, days, classes, grades, teachers)
    return None

# Adds each of the different types of contraints to the problem
def add_constraints(prob, grid_vars, days, classes, grades, teachers, available_classes, necessary_classes):

    add_scheduler_constraints(prob, grid_vars, days, classes, grades, teachers)
    add_teachers_constraints()
    add_grades_constraints(prob, grid_vars, days, classes, grades, teachers, available_classes, necessary_classes)

# Adds the default constraints of a scheduler to the problem
def add_scheduler_constraints(prob, grid_vars, days, classes, grades, teachers):

    # Constraint to ensure only one teacher is assigned a especific class of a grade in a day
    for day in days:
        for clas in classes:
            for grade in grades:
                prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher] for teacher in teachers]),
                                                    sense= plp.LpConstraintEQ,
                                                    name= f"constraint_sum_{day}_{clas}_{grade}",
                                                    rhs= 1))

    # Constraint to ensure a teacher will not be assigned two classes at the same time
    for day in days:
        for clas in classes:
            for teacher in teachers:
                prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher]*teacher for grade in grades]),
                                                    sense= plp.LpConstraintEQ,
                                                    name= f"constraint_uniq_grade_{day}_{clas}_{grade}",
                                                    rhs= teacher))

# Adds the grades constraints to the problem
def add_grades_constraints(prob, grid_vars, days, classes, grades, teachers, available_classes, necessary_classes):

    # Constraint to ensure only classes available to the grade are used
    for day in days:
        for clas in classes:
            for grade in grades:
                if (available_classes[day][clas][grade]):
                    prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher]*teacher for teacher in teachers]),
                                                        sense= plp.LpConstraitEQ,
                                                        name= f"constraint_not_available_{day}_{clas}_{grade}",
                                                        rhs= available_classes[day][clas][grade]))

    # Constraint to ensure the grades has the necessary amount of classes from every teacher
    for teacher in teachers:
        for grade in grades:
            prob.addConstraint(plp.LpConstraint(e= plp.lpSum([sum(grid_vars[day][clas][grade][teacher]) for clas in classes for day in days]),
                                                sense= plp.LpConstraitEQ,
                                                name= f"constraint_necessary_amouny_of_classes_{day}_{clas}_{grade}",
                                                rhs= necessary_classes[grade][teacher]))


# Adds the teachers constraints to the problem
def add_teachers_constraints(prob, grid_vars, days, classes, grades, teachers, available_time):

    # Constraint to ensure only classes available to the grade are used
    for teacher in teachers:
        for day in days:
            for clas in classes:
                prob.addConstraint(plp.LpConstraint(e= plp.lpSum([sum(grid_vars[day][clas][grade][teacher]) for grade in grades]),
                                                    serve= plp.LpConstraitEQ,
                                                    name= f"constraint_teacher_available_classes_{teacher}_{day}_{clas}",
                                                    rhs = available_time[teacher][day][clas]))

if __name__ == "__main__":
    print("This file can't be executed on its own, try main.py")