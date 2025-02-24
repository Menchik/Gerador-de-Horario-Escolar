import json

from constants import classes, days_of_the_week

def get_data():
    with open("myfile.json", "r") as input_file:
        data = json.load(input_file)
        return data

def get_number_of_grades():
    names = get_grades_names()
    return len(names)

def get_grades_names():
    new_data = get_data()
    return new_data["Turmas"]["Nomes"]

def get_number_of_teachers():
    names = get_teacher_names()
    return len(names)

def get_teacher_names():
    new_data = get_data()
    return new_data["Professores"]["Nomes"]

def save_to_file(new_data):
    new_data = json.dumps(new_data, indent=6)
    with open("myfile.json", "w") as file:
        file.write(new_data)

def get_input():
    dayCount = range(len(days_of_the_week)-1)
    classCount = range(len(classes)-1)
    grades = range(get_number_of_grades())
    teachers = range(get_number_of_teachers())
    data = get_data()
    grades_available_classes = data["Turmas"]["AulaDisponivel"]
    grades_necessary_classes = data["Turmas"]["AulasNecessarias"]
    teachers_available_time = data["Professores"]["HorarioDisponivel"]

    total_aulas = len(dayCount)*len(classCount)

    for grade in grades:
        soma = 0
        for day in dayCount:
            for clas in classCount:
                try:
                    soma += grades_available_classes[day][clas][grade]
                except:
                    print(grades_available_classes)
                    print(day, clas, grade)
        grades_necessary_classes[grade].append(total_aulas-soma)

    return dayCount, classCount, grades, teachers, teachers_available_time, grades_available_classes, grades_necessary_classes

if __name__ == "__main__":
    print("This file can't be executed on its own, try main.py")