import PySimpleGUI as sg
from sqlalchemy import column
from storage import get_grades_names

days_of_the_week = ["        ","Seg ", "Ter ", "Qua ", "Qui ", "Sex ", "Sab"]
classes = ["","7:00  ", "7:50  ", "8:55  ", "9:40  ", "10:40", "11:25", "13:30", "14:15", "15:15", "16:00", "16:45"]

def get_colum(solution, grade):
    colum = [[0 for _ in range(7)] for _ in range(12)]
    for i in range(12):
        for j in range(7):
            if i == 0:
                colum[i][j] = sg.Text(days_of_the_week[j])
            elif j == 0:
                colum[i][j] = sg.Text(classes[i])
            else:
                colum[i][j] = sg.Text(solution[j-1][i-1][grade], pad=((3,10), (0,0)))
    return colum

#def get_column(solution, grade, num):
#    column = [0 for _ in range 12]

def make_results_window(solution):

    TeacherWindowLayout =   [   [sg.Text("Horario Gerado", font="Arial 26 bold")]]

#    layout = []

    for num, grade in enumerate(get_grades_names()):
        TeacherWindowLayout.append([sg.Text(f"{grade}:")])
        TeacherWindowLayout.append([sg.Column(get_colum(solution, num))])
        #layout.append([sg.Column(get_column(solution, num, i))] for i in range(7))

    #TeacherWindowLayout.append(sg.Column(layout))

    return sg.Window("Gerenciamento de Professores", [[sg.Column(TeacherWindowLayout, scrollable=True, vertical_scroll_only=True, element_justification="c")]], finalize=True, element_justification="c", resizable=True)