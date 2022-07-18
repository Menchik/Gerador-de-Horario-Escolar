import PySimpleGUI as sg
from sqlalchemy import Column, values
import storage as stg

######### TEACHERS WINDOW #########
grades_names = []
days_of_the_week = ["        ","Seg ", "Ter ", "Qua ", "Qui ", "Sex ", "Sab"]
classes = ["","7:00  ", "7:50  ", "8:55  ", "9:40  ", "10:40", "11:25", "13:30", "14:15", "15:15", "16:00", "16:45"]

def get_grades_from_file():
    data = stg.get_data()
    for key in data["Turmas"].keys():
        if key not in grades_names:
            grades_names.append(key)

def add(gradeW, name):
    if name not in grades_names:
        grades_names.append(name)
        gradeW.Element("-DROP-").update(values=grades_names, value=name)
        data = stg.get_data()
        data["Turmas"][name] = [[False for _ in range(6)] for _ in range(11)]
        stg.save_to_file(data)
        access(gradeW, name)
    else:
        sg.popup("O nome escrito já se encontra na lista")
    gradeW.Element("-IN_NAME-").update(value ="Insira o nome aqui")

def remove(gradeW, name):
    if name != "Lista de Turmas":
        if sg.popup_yes_no(f"Certeza que deseja remover {name}?") == "Yes":
            grades_names.remove(name)
            gradeW.Element("-DROP-").update(values=grades_names, value="Lista de Turmas")
            access(gradeW, "Lista de Turmas")
            data = stg.get_data()
            data["Turmas"].pop(name)
            stg.save_to_file(data)
    else:
        sg.popup("Esse elemento não pode ser removido")

def save(name, classes_data, teachers_data):
    new_data = stg.get_data()
    new_data["Turmas"][name] = classes_data
    stg.save_to_file(new_data)

def get_data(name):
    teacher = stg.get_data()
    return teacher["Turmas"][name]

def select(gradeW, true_or_false):
    for j in range(1, 12):
        for i in range(1, 7):
                gradeW.Element(f"-CHECK_{i}_{j}-").update(value=true_or_false)

def access(gradeW, name):
    if name == "Lista de Turmas":
        for j in range(1, 12):
            for i in range(1, 7):
                    gradeW.Element(f"-CHECK_{i}_{j}-").update(value=False)
    else:
        tdata = get_data(name)
        for j in range(1, 12):
            for i in range(1, 7):
                if tdata[j-1][i-1]:
                    gradeW.Element(f"-CHECK_{i}_{j}-").update(value=True)
                else:
                    gradeW.Element(f"-CHECK_{i}_{j}-").update(value=False)

def make_grades_window():

    checkColumn = [[sg.Text(f"{i}_{j}") for i in range(7)] for j in range(12)]
    for j in range(12):
        for i in range(7):
            if j == 0:
                checkColumn[j][i] = sg.Text(days_of_the_week[i])
            elif i == 0:
                checkColumn[j][i] = sg.Text(classes[j])
            else:
                checkColumn[j][i] = sg.Checkbox("", pad=((3,10), (0,0)), key=f"-CHECK_{i}_{j}-", enable_events=True)

    leftColumn = sg.Column ([   
                                [sg.Text("Especifique os horários\nde cada turma", font="Arial 26 bold")],
                                [sg.Input("Insira o nome aqui", key="-IN_NAME-", enable_events=True), sg.Button("Adicionar", button_color=("white", "green"))],
                                [sg.Combo(grades_names, default_value=grades_names[0], readonly=True, enable_events=True, key="-DROP-"), sg.Button("Salvar", button_color=("white", "royalblue")), sg.Button("Remover", button_color=("white", "red"))],
                                [sg.Button("Selecionar todos", button_color=("white", "gray")), sg.Button("Selecionar nenhum", button_color=("white", "gray"))],
                                [sg.Column(checkColumn)]
                            ])

    layout = []
    data = stg.get_data()
    for teacher in data["Professores"]:
        layout.append([sg.Text(teacher),sg.Spin([1,2,3,4,5], key="-SPIN-")])

    otherColumn = sg.Column   ([[sg.Text("Número de aulas com\ncada professor", font="Arial 26 bold")],
                                [sg.Frame("Professores:", layout, expand_x=True)]])

    GradeWindowLayout = [[leftColumn, otherColumn]]

    return sg.Window("Gerenciamento de Turmas", GradeWindowLayout, finalize=True, element_justification='c')