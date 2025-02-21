#################################################################################
# Inspired by https://coin-or.github.io/pulp/CaseStudies/a_sudoku_problem.html  #
# Highly recommend reading it as the code is not intuitive at all               #
#################################################################################

import pulp as plp
import storage

def solve(days, classes, grades, teachers, available_time, available_classes, necessary_classes):
    
    # Create the linear programming problem
    prob = plp.LpProblem("School_Scheduler", plp.LpMaximize) 

    # Decision Variable/Target variable
    grid_vars = plp.LpVariable.dicts("grid_value", (days,classes,grades,teachers), cat='Binary') 

    afternoon_classes = plp.LpVariable.dicts("afternoon_classes", (days, grades), cat='Binary')

    weights = {}
    for index in range(len(classes)):
        if 1 <= index <= 4:
            weights[classes[index]] = 10
        elif index == 0:
            weights[classes[index]] = 5
        elif index == 5:
            weights[classes[index]] = 2
        else: # 6 or more
            weights[classes[index]] = 1

    # Classes weighted by their time
    weighted_classes = [grid_vars[day][clas][grade][teacher]*
        (weights[clas])
        for day in days
        for clas in classes
        for grade in grades
        for teacher in teachers]



    # Create Objective function
    prob += plp.lpSum(  [weighted_classes] 
                      + [afternoon_classes[day][grade]*(-1) for day in days for grade in grades]
                      ), "Objective Function"


    add_constraints(prob, grid_vars, days, classes, grades, teachers, available_time, available_classes, necessary_classes, afternoon_classes) # Create all of the constraints needed for the problem

    # Creates a file with all contraints so it's possible to see errors
    # prob.writeLP("filename.txt", writeSOS=1, mip=1, max_length=100) 
    


    prob.solve() # Solve the problem given all constraints
    
    solution_status = plp.LpStatus[prob.status] # Gets the solution status
    print(f'Solution Status = {solution_status}') # Print the status of the solution

    # Prints and returns the solution if an optimal one has been found
    if solution_status == 'Optimal':
        solution = extract_solution(grid_vars, days, classes, grades, teachers)
        return solution
    return None

def add_constraints(prob, grid_vars, days, classes, grades, teachers, available_time, available_classes, necessary_classes, afternoon_classes): # Adds each of the different types of contraints to the problem

    add_scheduler_constraints(prob, grid_vars, days, classes, grades, teachers, afternoon_classes)
    add_teachers_constraints(prob, grid_vars, days, classes, grades, teachers, available_time)
    add_grades_constraints(prob, grid_vars, days, classes, grades, teachers, available_classes, necessary_classes)

def add_scheduler_constraints(prob, grid_vars, days, classes, grades, teachers, afternoon_classes): # Adds the default constraints of a scheduler to the LP problem

    # Constraint to ensure only one teacher is assigned a especific class
    for day in days:
        for clas in classes:
            for grade in grades:
                prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher] for teacher in teachers]),
                                                    sense= plp.LpConstraintLE,
                                                    rhs= 1,
                                                    name= f"constraint_sum_{day}_{clas}_{grade}"))

    # Constraint to ensure a teacher will not be assigned two classes at the same time
    for day in days:
        for clas in classes:
            for teacher in teachers:
                prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher] for grade in grades]),
                                                    sense= plp.LpConstraintLE,
                                                    rhs= 1,
                                                    name= f"constraint_unique_grade_{day}_{clas}_{teacher}"))

    # Ensure new_var is 1 if any of var1, var2, or var3 are 1
    # prob += new_var >= var1
    # prob += new_var >= var2
    # prob += new_var >= var3
    for day in days:
        for grade in grades:
            for clas in classes[6:]:
                prob.addConstraint(plp.LpConstraint(e= plp.lpSum([afternoon_classes[day][grade]]+[grid_vars[day][clas][grade][teacher]*(-1) for teacher in teachers]),
                                                    sense= plp.LpConstraintGE,
                                                    rhs= 0,
                                                    name= f"constraint_afternoon_up_{day}_{grade}_{clas}"))

    # Ensure new_var is 0 if all of var1, var2, and var3 are 0
    # prob += new_var <= var1 + var2 + var3
    for day in days:
        for grade in grades:
            prob.addConstraint(plp.LpConstraint(e= plp.lpSum([afternoon_classes[day][grade]]+[grid_vars[day][clas][grade][teacher]*(-1) for clas in classes[6:] for teacher in teachers]) ,
                                                sense= plp.LpConstraintLE,
                                                rhs= 0,
                                                name= f"constraint_afternoon_lb_{day}_{grade}"))

def add_grades_constraints(prob, grid_vars, days, classes, grades, teachers, available_classes, necessary_classes): # Adds the grades constraints to the problem

    # Constraint to ensure only classes available to the grade are used
    for day in days:
        for clas in classes:
            for grade in grades:
                prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher] for teacher in teachers]),
                                                    sense= plp.LpConstraintLE,
                                                    rhs= available_classes[day][clas][grade],
                                                    name= f"constraint_not_available_{day}_{clas}_{grade}"))

    # Constraint to ensure the grades has the necessary amount of classes from every teacher
    for grade in grades:
        for teacher in teachers:
            prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher] for clas in classes for day in days]),
                                                sense= plp.LpConstraintEQ,
                                                rhs= necessary_classes[grade][teacher],
                                                name= f"constraint_necessary_amount_of_classes_{teacher}_{grade}"))

def add_teachers_constraints(prob, grid_vars, days, classes, grades, teachers, available_time): #Adds the teachers constraints to the problem

    # Constraint to ensure only classes available by the teacher are considered
    for day in days:
        for clas in classes:
            for teacher in teachers:
                prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas][grade][teacher] for grade in grades]),
                                                    sense= plp.LpConstraintLE,
                                                    rhs = available_time[day][clas][teacher],
                                                    name= f"constraint_teacher_available_classes_{day}_{clas}_{teacher}"))
                
        # Constraint that makes so that no teacher has more then 2 classes in a row with the same grade
        for teacher in teachers:
            for grade in grades:
                for clas in classes[2:]:
                    prob.addConstraint(plp.LpConstraint(e= plp.lpSum([grid_vars[day][clas-i][grade][teacher] for i in range(3)]),
                                                        sense= plp.LpConstraintLE,
                                                        rhs = 2,
                                                        name= f"constraint_teacher_classes_in_a_row_{day}_{clas}_{grade}_{teacher}"))


def extract_solution(grid_vars, days, classes, grades, teachers):
    solution = [[[0 for _ in grades] for _ in classes] for _ in days]
    names = storage.get_teacher_names()

    max_length = max([len(name) for name in names])
    for t in teachers:
        while len(names[t]) < max_length:
            names[t] += ' '

    no_teacher = ''
    for _ in range(max_length):
        no_teacher += '-'

    for day in days:
        for clas in classes:
            for grade in grades:
                for teacher in teachers:
                    if plp.value(grid_vars[day][clas][grade][teacher]):
                        solution[day][clas][grade] = names[teacher]
                if solution[day][clas][grade] == 0:
                    solution[day][clas][grade] = no_teacher
    return solution

def printSolution(solution, days, classes, grades):

    # Print the final result
    print(f"Final result:")
    for grade in grades:
        for day in days:
            print(f"\nDIA {day}:", end="")
            for clas in classes:
                print(f"\n    AULA {clas}:", end="\n        | ")
                print(solution[day][clas][grade],end=" | ")


if __name__ == "__main__":
    print("This file can't be executed on its own, try main.py")