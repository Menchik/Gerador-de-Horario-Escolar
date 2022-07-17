import PySimpleGUI as sg
import SG_Utils.main_window as mw
from solver import solve

def MainLoop():
    sg.theme("DarkAmber")   # Add a touch of color

    # Create the Window
    mainWindow = sg.Window("Gerador de Horário Escolar", mw.MainWindowLayout, element_justification='c')

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = mainWindow.read()
        #print(event, values)
        if event == sg.WIN_CLOSED:
            break
        # elif event == "Configurações":
        #     print("Abrindo Configurações")
        elif event == "Professores":
            mainWindow.Disable()
            mw.TeacherLoop()
            mainWindow.Enable()
            mainWindow.bring_to_front()
        elif event == "Turmas":
            mainWindow.Disable()
            mw.GradeLoop()
            mainWindow.Enable()
            mainWindow.bring_to_front()
        elif event == "Gerar Horario":
            print("Gerando")
            #solve()

    mainWindow.close()

if __name__ == "__main__":
    MainLoop()