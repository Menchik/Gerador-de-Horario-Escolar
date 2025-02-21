import PySimpleGUI as sg
from sqlalchemy import column
from storage import get_grades_names

from openpyxl import Workbook

from constants import classes, days_of_the_week

def get_colum(solution, grade):
    colum = [[0 for _ in range(len(days_of_the_week))] for _ in range(len(classes))]
    for i in range(len(classes)):
        for j in range(len(days_of_the_week)):
            if i == 0:
                colum[i][j] = sg.Text(days_of_the_week[j])
            elif j == 0:
                colum[i][j] = sg.Text(classes[i])
            else:
                colum[i][j] = sg.Text(solution[j-1][i-1][grade], pad=((3,10), (0,0)))
    return colum

#def get_column(solution, grade, num):
#    column = [0 for _ in range len(classes)]

def make_results_window(solution):

    TeacherWindowLayout =   [   [sg.Text("Horario Gerado", font="Arial 26 bold")]]

#    layout = []

    workbook = Workbook()
    default_sheet = workbook.active
    default_sheet.title = "Resumo"

    default_sheet.append(['', '']+get_grades_names())

    day_position = int((len(classes))/2)+1

    for i, day in enumerate(days_of_the_week[1:]):
        default_sheet['A'+str(day_position+len(classes)*i)] = day

        for j, class_ in enumerate(classes[1:]):
            default_sheet['B'+str(j+2+len(classes)*i)] = class_

        for grade in range(len(get_grades_names())):
            for j in range(len(classes[1:])):
                letter = chr(grade+1+ord('B'))
                default_sheet[letter+str(j+2+len(classes)*i)] = solution[i][j][grade]

    for num, grades in enumerate(get_grades_names()):

        new_sheet = workbook.create_sheet(title=grades)

        new_sheet.append(days_of_the_week)
        for i in range(len(classes)-1):
            new_sheet.append([classes[i+1]] + [solution[j-1][i][num] for j in range(1, len(days_of_the_week))])
        

    workbook.save('result.xlsx')

    for num, grade in enumerate(get_grades_names()):
        TeacherWindowLayout.append([sg.Text(f"{grade}:")])
        TeacherWindowLayout.append([sg.Column(get_colum(solution, num))])
        #layout.append([sg.Column(get_column(solution, num, i))] for i in range(len(days_of_the_week)))

    #TeacherWindowLayout.append(sg.Column(layout))

    return sg.Window("Gerenciamento de Professores", [[sg.Column(TeacherWindowLayout, scrollable=True, vertical_scroll_only=True, element_justification="c")]], finalize=True, element_justification="c", resizable=True)