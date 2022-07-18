import PySimpleGUI as sg
import SG_Utils.teacher_window_maker as twm
import SG_Utils.grade_window_maker as gwm



######### TEACHER WINDOW FUNCTION #########
def TeacherLoop():

    twm.get_teachers_from_file()
    teacherW = twm.make_teachers_window()
    changed = False
    drop = None
    
    while True:

        event, values = teacherW.read()

        if event == sg.WIN_CLOSED:
            break

        elif event.startswith("-CHECK"):
            changed = True

        elif event == "-DROP-":
            if changed == True and drop != "Lista de Professores":
                answer = sg.popup_yes_no("Suas alterações não foram salvas", "Deseja continuar mesmo assim?")
                if answer == "No":
                    teacherW.Element("-DROP-").update(value=drop)
                else:
                    twm.access(teacherW, values["-DROP-"])
                    drop = values["-DROP-"]
                    changed = True
            else:
                twm.access(teacherW, values["-DROP-"])
                drop = values["-DROP-"]
                changed = False

        elif event == "Adicionar":
            twm.add(teacherW, values["-IN_NAME-"])

        elif event == "Remover":
            twm.remove(teacherW, values["-DROP-"])

        elif event == "Selecionar todos":
            twm.select(teacherW, True)

        elif event == "Selecionar nenhum":
            twm.select(teacherW, False)

        elif event == "Salvar":
            changed = False
            if values["-DROP-"] != "Lista de Professores":
                data = [[values[f"-CHECK_{i}_{j}-"] for i in range(1, 7)] for j in range(1, 12)]
                twm.save(values["-DROP-"], data)
        #print(event, values)

######### GRADE WINDOW FUNCTION #########
def GradeLoop():

    gwm.get_grades_from_file()
    gradeW = gwm.make_grades_window()
    changed = False
    drop = None
    
    while True:

        event, values = gradeW.read()

        if event == sg.WIN_CLOSED:
            break

        elif event.startswith("-CHECK"):
            changed = True

        elif event == "-DROP-":
            if changed == True and drop != "Lista de Turmas":
                answer = sg.popup_yes_no("Suas alterações não foram salvas", "Deseja continuar mesmo assim?")
                if answer == "No":
                    gradeW.Element("-DROP-").update(value=drop)
                else:
                    changed = True
                    gwm.access(gradeW, values["-DROP-"])
                    drop = values["-DROP-"]
            else:
                gwm.access(gradeW, values["-DROP-"])
                drop = values["-DROP-"]
                changed = False

        elif event == "Adicionar":
            gwm.add(gradeW, values["-IN_NAME-"])

        elif event == "Remover":
            gwm.remove(gradeW, values["-DROP-"])

        elif event == "Selecionar todos":
            gwm.select(gradeW, True)

        elif event == "Selecionar nenhum":
            gwm.select(gradeW, False)

        elif event == "Salvar":
            changed = False
            if values["-DROP-"] != "Lista de Turmas":
                classes_data = [[values[f"-CHECK_{i}_{j}-"] for i in range(1, 7)] for j in range(1, 12)]
                teachers_data = [values[f"-SPIN_{i}-"] for i in range(twm.get_number_of_teachers())]
                gwm.save(values["-DROP-"], classes_data, teachers_data)
            else:
                sg.popup("\"Lista de Turmas\" não é uma turma válida")