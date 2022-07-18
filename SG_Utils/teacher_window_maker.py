import PySimpleGUI as sg
import storage as stg

######### TEACHERS WINDOW #########
teachers_names = ["Lista de Professores"]
days_of_the_week = ["        ","Seg ", "Ter ", "Qua ", "Qui ", "Sex ", "Sab"]
classes = ["","7:00  ", "7:50  ", "8:55  ", "9:40  ", "10:40", "11:25", "13:30", "14:15", "15:15", "16:00", "16:45"]

def get_number_of_teachers():
    return len(teachers_names)

def get_teachers_from_file():
    data = stg.get_data()
    for key in data["Professores"].keys():
        if key not in teachers_names:
            teachers_names.append(key)

def add(teacherW, name):
    if name not in teachers_names:
        teachers_names.append(name)
        teacherW.Element("-DROP-").update(values=teachers_names, value=name)
        data = stg.get_data()
        for i in range(6):
            for j in range(11):
                data["Professores"]["Teste"][i][j].append(0)
        #data["Professores"][name] = [[False for _ in range(6)] for _ in range(11)]
        stg.save_to_file(data)
        access(teacherW, name)
    else:
        sg.popup("O nome escrito já se encontra na lista")
    teacherW.Element("-IN_NAME-").update(value ="Insira o nome aqui")

def remove(teacherW, name):
    if name != "Lista de Professores":
        if sg.popup_yes_no(f"Certeza que deseja remover {name}?") == "Yes":
            data = stg.get_data()
            for i in range(6):
                for j in range(11):
                    del data["Professores"]["Teste"][i][j][teachers_names.index(name)-1]
            #data["Professores"].pop(name)
            stg.save_to_file(data)
            teachers_names.remove(name)
            teacherW.Element("-DROP-").update(values=teachers_names, value="Lista de Professores")
            access(teacherW, "Lista de Professores")
    else:
        sg.popup("Esse elemento não pode ser removido")

def save(name, data):
    new_data = stg.get_data()    
    for i in range(6):
        for j in range(11):
            data["Professores"]["Teste"][i][j][teachers_names.index(name)-1] = data[i][j]
    #new_data["Professores"][name] = data
    stg.save_to_file(new_data)

def select(teacherW, true_or_false):
    for j in range(1, 12):
        for i in range(1, 7):
                teacherW.Element(f"-CHECK_{i}_{j}-").update(value=true_or_false)

def access(teacherW, name):
    if name == "Lista de Professores":
        for j in range(1, 12):
            for i in range(1, 7):
                    teacherW.Element(f"-CHECK_{i}_{j}-").update(value=False)
    else:
        tdata = stg.get_data()
        tdata = tdata["Professores"][name]
        for j in range(1, 12):
            for i in range(1, 7):
                if tdata[j-1][i-1]:
                    teacherW.Element(f"-CHECK_{i}_{j}-").update(value=True)
                else:
                    teacherW.Element(f"-CHECK_{i}_{j}-").update(value=False)

def make_teachers_window():

    colum = [[0 for i in range(7)] for j in range(12)]
    for j in range(12):
        for i in range(7):
            if j == 0:
                colum[j][i] = sg.Text(days_of_the_week[i])
            elif i == 0:
                colum[j][i] = sg.Text(classes[j])
            else:
                colum[j][i] = sg.Checkbox("", pad=((3,10), (0,0)), key=f"-CHECK_{i}_{j}-", enable_events=True)

    TeacherWindowLayout =   [   [sg.Text("Especifique os horários de cada professor", font="Arial 26 bold")],
                                [sg.Input("Insira o nome aqui", key="-IN_NAME-", enable_events=True), sg.Button("Adicionar", button_color=("white", "green"))],
                                [sg.Combo(teachers_names, default_value=teachers_names[0], readonly=True, enable_events=True, key="-DROP-"), sg.Button("Salvar", button_color=("white", "royalblue")), sg.Button("Remover", button_color=("white", "red"))],
                                [sg.Button("Selecionar todos", button_color=("white", "gray")), sg.Button("Selecionar nenhum", button_color=("white", "gray"))],
                                [[sg.Column(colum)]]
                            ]

    return sg.Window("Gerenciamento de Professores", TeacherWindowLayout, finalize=True, element_justification='c')