from getInput import returnInput
from solver import solve
import pulp as plp

days, classes, grades, teachers, available_time, available_classes, necessary_classes = returnInput()

# grid_vars = plp.LpVariable.dicts("grid_value", (days,classes,grades,teachers), cat='Binary')

# for grade in grades:
#         for teacher in teachers:
#             print(plp.lpSum([grid_vars[day][clas][grade][teacher] for clas in classes for day in days]), end="\nFim de um\n")

solution = solve(days, classes, grades, teachers, available_time, available_classes, necessary_classes)