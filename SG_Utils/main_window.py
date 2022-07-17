import PySimpleGUI as sg
import SG_Utils.teacher_window as tw
import SG_Utils.grade_window as gw

######### MAIN WINDOW LAYOUT #########
MainWindowLayout = [  [sg.Text("Gerador de Horario Escolar", font="Arial 30 bold")],
                #[sg.Button("Configurações")],
                [sg.Button("Professores")],
                [sg.Button("Turmas")],
                [sg.Button("Gerar Horario")]]

######### TEACHER WINDOW FUNCTION #########
def TeacherLoop():

    teacherW = tw.make_teachers_window()
    num_teacher = 0
    
    while True:

        event, values = teacherW.read()

        if event == sg.WIN_CLOSED:
            break

        elif event == "Adicionar":
            tw.add_teacher(values["-IN_NAME-"])
            num_teacher += 1
            teacherW.close()
            teacherW = tw.make_teachers_window()

        elif event == "Remover":
            tw.remove_teacher(values["-DROP-"])
            num_teacher -= 1
            teacherW.close()
            teacherW = tw.make_teachers_window()

        elif event == "Acessar":
            if values["-DROP-"] != "Lista de Professores":
                tw.access_teacher(values["-DROP-"])

        elif event == "Selecionar todos":
            tw.select_all()

        elif event == "Selecionar nenhum":
            tw.select_none()
        print(event, values)

######### GRADE WINDOW FUNCTION #########
def GradeLoop():
    teacherW = tw.make_teachers_window()
    num_tab = 0
    while True:
        event, values = teacherW.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "Adicionar professor(a)":
            tw.add_teacher(values["nome"])
            num_tab+=1
            teacherW.close()
            teacherW = tw.make_teachers_window()
        #print(event, values)