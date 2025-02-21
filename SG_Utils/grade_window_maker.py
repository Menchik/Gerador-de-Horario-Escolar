import PySimpleGUI as sg
import storage as stg

from constants import classes, days_of_the_week

######### TEACHERS WINDOW #########
grades_names = ["Lista de Turmas"]

def get_grades_from_file():
    data = stg.get_data()
    for turma in data["Turmas"]["Nomes"]:
        if turma not in grades_names:
            grades_names.append(turma)

def add(gradeW, name):
    if name not in grades_names:
        grades_names.append(name)
        gradeW.Element("-DROP-").update(values=grades_names, value=name)
        data = stg.get_data()
        for i in range(len(days_of_the_week)-1):
            for j in range(len(classes)-1):
                data["Turmas"]["AulaDisponivel"][i][j].append(0)
        #data["Turmas"][name] = [[False for _ in range(len(days_of_the_week)-1)] for _ in range(len(classes)-1)]
        data["Turmas"]["Nomes"].append(name)
        data["Turmas"]["AulasNecessarias"].append([0 for _ in range(stg.get_number_of_teachers())])
        stg.save_to_file(data)
        access(gradeW, name)
    else:
        sg.popup("O nome escrito já se encontra na lista")
    gradeW.Element("-IN_NAME-").update(value ="Insira o nome aqui")

def remove(gradeW, name):
    if name != "Lista de Turmas":
        if sg.popup_yes_no(f"Certeza que deseja remover {name}?") == "Yes":
            data = stg.get_data()
            names = data["Turmas"]["Nomes"]
            for i in range(len(classes)-1):
                for j in range(len(days_of_the_week)-1):
                    del data["Turmas"]["AulaDisponivel"][i][j][names.index(name)]
            del data["Turmas"]["AulasNecessarias"][names.index(name)]
            data["Turmas"]["Nomes"].remove(name)
            stg.save_to_file(data)
            grades_names.remove(name)
            gradeW.Element("-DROP-").update(values=grades_names, value="Lista de Turmas")
            access(gradeW, "Lista de Turmas")
    else:
        sg.popup("Esse elemento não pode ser removido")

def save(name, classes_data, teachers_data):
    new_data = stg.get_data()
    names = new_data["Turmas"]["Nomes"]
    for i in range(len(days_of_the_week)-1):
        for j in range(len(classes)-1):
            if classes_data[i][j]:
                new_data["Turmas"]["AulaDisponivel"][i][j][names.index(name)] = 1
            else:
                new_data["Turmas"]["AulaDisponivel"][i][j][names.index(name)] = 0
    new_data["Turmas"]["AulasNecessarias"][names.index(name)] = teachers_data
    stg.save_to_file(new_data)

def select(gradeW, true_or_false):
    for i in range(1, len(classes)):
        for j in range(1, len(days_of_the_week)):
                gradeW.Element(f"-CHECK_{i}_{j}-").update(value=true_or_false)

def access(gradeW, name):
    if name == "Lista de Turmas":
        for i in range(1, len(classes)):
            for j in range(1, len(days_of_the_week)):
                    gradeW.Element(f"-CHECK_{i}_{j}-").update(value=False)
        for teacher in range(stg.get_number_of_teachers()):
            gradeW.Element(f"-SPIN_{teacher}-").update(value=0)
    else:
        tdata = stg.get_data()
        names = tdata["Turmas"]["Nomes"]
        for i in range(1, len(classes)):
            for j in range(1, len(days_of_the_week)):
                if tdata["Turmas"]["AulaDisponivel"][j-1][i-1][names.index(name)]:
                    gradeW.Element(f"-CHECK_{i}_{j}-").update(value=True)
                else:
                    gradeW.Element(f"-CHECK_{i}_{j}-").update(value=False)
        for teacher in range(stg.get_number_of_teachers()):
            gradeW.Element(f"-SPIN_{teacher}-").update(value=tdata["Turmas"]["AulasNecessarias"][names.index(name)][teacher])

def make_grades_window():

    checkColumn = [[0 for _ in range(len(days_of_the_week))] for _ in range(len(classes))]
    for i in range(len(classes)):
        for j in range(len(days_of_the_week)):
            if i == 0:
                checkColumn[i][j] = sg.Text(days_of_the_week[j])
            elif j == 0:
                checkColumn[i][j] = sg.Text(classes[i])
            else:
                checkColumn[i][j] = sg.Checkbox("", pad=((3,10), (0,0)), key=f"-CHECK_{i}_{j}-", enable_events=True)

    leftColumn = sg.Column ([   
                                [sg.Text("Especifique os horários\nde cada turma", font="Arial 26 bold")],
                                [sg.Input("Insira o nome aqui", key="-IN_NAME-", enable_events=True), sg.Button("Adicionar", button_color=("white", "green"))],
                                [sg.Combo(grades_names, default_value=grades_names[0], readonly=True, enable_events=True, key="-DROP-"), sg.Button("Salvar", button_color=("white", "royalblue")), sg.Button("Remover", button_color=("white", "red"))],
                                [sg.Button("Selecionar todos", button_color=("white", "gray")), sg.Button("Selecionar nenhum", button_color=("white", "gray"))],
                                [sg.Column(checkColumn)]
                            ], element_justification="c")

    layout = []
    data = stg.get_data()
    for ind, teacher in enumerate(data["Professores"]["Nomes"]):
        layout.append([sg.Text(teacher),sg.Spin([num for num in range(21)], key=f"-SPIN_{ind}-")])

    otherColumn = sg.Column   ([[sg.Text("Número de aulas com\ncada professor", font="Arial 26 bold")],
                                [sg.Frame("Professores:", layout, expand_x=True)]], scrollable=True, vertical_scroll_only=True, size=(450, 500))

    return sg.Window("Gerenciamento de Turmas", [[leftColumn, otherColumn]], finalize=True, element_justification='c')