import PySimpleGUI as sg
import os
from createDB import createDB

from SG_Utils.subwindows import TeacherLoop, GradeLoop, ResultLoop
from solver import solve
from storage import get_input
from constants import classes, days_of_the_week

def MainLoop():

    ######### MAIN WINDOW LAYOUT #########
    MainWindowLayout = [  [sg.Text("Gerador de Horario Escolar", font="Arial 30 bold", background_color=None)],
                #[sg.Button("Configurações")],
                [sg.Button("Professores")],
                [sg.Button("Turmas")],
                [sg.Button("Gerar Horario")]]
    sg.theme("DarkGrey")   # Add a touch of color

    if not os.path.exists("myfile.json"):
        createDB(len(classes)-1, len(days_of_the_week)-1)

    # Create the Window
    mainWindow = sg.Window("Gerador de Horário Escolar", MainWindowLayout, element_justification='c')

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = mainWindow.read()
        #print(event, values)
        if event == sg.WIN_CLOSED:
            break

        # elif event == "Configurações":
        #     print("Abrindo Configurações")

        elif event == "Professores":
            # mainWindow.Disable()
            TeacherLoop()
            # mainWindow.Enable()
            mainWindow.bring_to_front()

        elif event == "Turmas":
            # mainWindow.Disable()
            GradeLoop()
            # mainWindow.Enable()
            mainWindow.bring_to_front()

        elif event == "Gerar Horario":
            days, clas, grades, teachers, teachers_available_time, grades_available_classes, grades_necessary_classes = get_input()
            solution = solve(days, clas, grades, teachers, teachers_available_time, grades_available_classes, grades_necessary_classes)
            if solution:
                ResultLoop(solution)
            else:
                sg.popup("Nenhuma solução foi encontrada")
            
    mainWindow.close()

if __name__ == "__main__":
    MainLoop()