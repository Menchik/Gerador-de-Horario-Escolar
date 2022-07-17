import PySimpleGUI as sg

######### TEACHERS WINDOW #########
teachers_names = ["Lista de Professores"]
days_of_the_week = ["        ","Seg ", "Ter ", "Qua ", "Qui ", "Sex ", "Sab"]
classes = ["","7:00  ", "7:50  ", "8:55  ", "9:40  ", "10:40", "11:25", "13:30", "14:15", "15:15", "16:00", "16:45"]

def add_teacher(name):
    teachers_names.append(name)

def remove_teacher(name):
    if name != "Lista de Professores":
        if sg.popup_yes_no(f"Certeza que deseja remover {name}?", sg.Button("talvez")) == "Yes":
            teachers_names.remove(name)
    else:
        sg.popup("Esse elemento não pode ser removido")

def make_teachers_window():

    colum = [[sg.Text(f"{i}_{j}") for i in range(7)] for j in range(12)]
    for j in range(12):
        for i in range(7):
            if j == 0:
                colum[j][i] = sg.Text(days_of_the_week[i])
            elif i == 0:
                colum[j][i] = sg.Text(classes[j])
            else:
                colum[j][i] = sg.Checkbox("", pad=((3,10), (0,0)), key=f"-CHECK_{i}_{j}-")

    TeacherWindow = [   [sg.Text("Gerenciamento de Professores", font="Arial 26 bold")],
                        [sg.Input("Insira o nome aqui", key="-IN_NAME-", enable_events=True), sg.Button("Adicionar", button_color=("white", "green"))],
                        [sg.Combo(teachers_names, default_value=teachers_names[0], readonly=True, enable_events=True, key="-DROP-"), sg.Button("Acessar"), sg.Button("Remover", button_color=("white", "red"))],
                        [sg.Button("Selecionar todos", button_color=("white", "gray")), sg.Button("Selecionar nenhum", button_color=("white", "gray"))],
                        [[sg.Column(colum)]]]

    return sg.Window("Gerenciamento de Professores", TeacherWindow, finalize=True, element_justification='c')