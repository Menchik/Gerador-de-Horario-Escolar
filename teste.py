from getInput import returnInput
from solver import solve

days, classes, grades, teachers, available_time, available_classes, necessary_classes = returnInput()

solution = solve(days, classes, grades, teachers, available_time, available_classes, necessary_classes)