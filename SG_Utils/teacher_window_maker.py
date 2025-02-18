import PySimpleGUI as sg
import storage as stg

from constants import classes, days_of_the_week

######### TEACHERS WINDOW #########
teachers_names = ["Lista de Professores"]

def get_teachers_from_file():
    for name in stg.get_teacher_names():
        if name not in teachers_names:
            teachers_names.append(name)

def add(teacherW, name):
    if name not in teachers_names:
        teachers_names.append(name)
        teacherW.Element("-DROP-").update(values=teachers_names, value=name)
        data = stg.get_data()
        for i in range(len(days_of_the_week)-1):
            for j in range(len(classes)-1):
                data["Professores"]["HorarioDisponivel"][i][j].append(0)
        #data["Professores"][name] = [[False for _ in range(len(days_of_the_week)-1)] for _ in range(len(classes)-1)]
        data["Professores"]["Nomes"].append(name)
        for grade in range(stg.get_number_of_grades()):
            data["Turmas"]["AulasNecessarias"][grade].append(0)
        stg.save_to_file(data)
        access(teacherW, name)
    else:
        sg.popup("O nome escrito já se encontra na lista")
    teacherW.Element("-IN_NAME-").update(value ="Insira o nome aqui")

def remove(teacherW, name):
    if name != "Lista de Professores":
        if sg.popup_yes_no(f"Certeza que deseja remover {name}?") == "Yes":
            data = stg.get_data()
            names = data["Professores"]["Nomes"]
            for i in range(len(days_of_the_week)-1):
                for j in range(len(classes)-1):
                    del data["Professores"]["HorarioDisponivel"][i][j][names.index(name)]
            data["Professores"]["Nomes"].remove(name)
            for grade in range(stg.get_number_of_grades()):
                del data["Turmas"]["AulasNecessarias"][grade][teachers_names.index(name)-1]
            stg.save_to_file(data)
            teachers_names.remove(name)
            teacherW.Element("-DROP-").update(values=teachers_names, value="Lista de Professores")
            access(teacherW, "Lista de Professores")
    else:
        sg.popup("Esse elemento não pode ser removido")

def save(name, data):
    new_data = stg.get_data()
    names = new_data["Professores"]["Nomes"]
    for i in range(len(days_of_the_week)-1):
        for j in range(len(classes)-1):
            if data[i][j]:
                new_data["Professores"]["HorarioDisponivel"][i][j][names.index(name)] = 1
            else:
                new_data["Professores"]["HorarioDisponivel"][i][j][names.index(name)] = 0
    #new_data["Professores"][name] = data
    stg.save_to_file(new_data)

def select(teacherW, true_or_false):
    for i in range(1, len(classes)):
        for j in range(1, len(days_of_the_week)):
                teacherW.Element(f"-CHECK_{i}_{j}-").update(value=true_or_false)

def access(teacherW, name):
    if name == "Lista de Professores":
        for i in range(1, len(classes)):
            for j in range(1, len(days_of_the_week)):
                    teacherW.Element(f"-CHECK_{i}_{j}-").update(value=False)
    else:
        tdata = stg.get_data()
        names = tdata["Professores"]["Nomes"]
        for i in range(1, len(classes)):
            for j in range(1, len(days_of_the_week)):
                if tdata["Professores"]["HorarioDisponivel"][j-1][i-1][names.index(name)]:
                    teacherW.Element(f"-CHECK_{i}_{j}-").update(value=True)
                else:
                    teacherW.Element(f"-CHECK_{i}_{j}-").update(value=False)

def make_teachers_window():

    colum = [[0 for _ in range(len(days_of_the_week))] for _ in range(len(classes))]
    for i in range(len(classes)):
        for j in range(len(days_of_the_week)):
            if i == 0:
                colum[i][j] = sg.Text(days_of_the_week[j])
            elif j == 0:
                colum[i][j] = sg.Text(classes[i])
            else:
                colum[i][j] = sg.Checkbox("", pad=((3,10), (0,0)), key=f"-CHECK_{i}_{j}-", enable_events=True)

    TeacherWindowLayout =   [   [sg.Text("Especifique os horários de cada professor", font="Arial 26 bold")],
                                [sg.Input("Insira o nome aqui", key="-IN_NAME-", enable_events=True), sg.Button("Adicionar", button_color=("white", "green"))],
                                [sg.Combo(teachers_names, default_value=teachers_names[0], readonly=True, enable_events=True, key="-DROP-"), sg.Button("Salvar", button_color=("white", "royalblue")), sg.Button("Remover", button_color=("white", "red"))],
                                [sg.Button("Selecionar todos", button_color=("white", "gray")), sg.Button("Selecionar nenhum", button_color=("white", "gray"))],
                                [[sg.Column(colum)]]
                            ]

    return sg.Window("Gerenciamento de Professores", TeacherWindowLayout, finalize=True, element_justification='c')