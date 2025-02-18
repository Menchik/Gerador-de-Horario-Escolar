import json

def createDB(classes, days):
    template = {
        "Professores": {
            "Nomes": [],
            "HorarioDisponivel": []
        },
        "Turmas": {
            "Nomes": [],
            "AulaDisponivel": [],
            "AulasNecessarias": []
        }
    }

    semana = [[] for _ in range(days)]
    for i in range(days):
        semana[i] = [[] for _ in range(classes)]

    template["Professores"]["HorarioDisponivel"] = semana
    template["Turmas"]["AulaDisponivel"] = semana

    with open("myfile.json", "w") as file:
        json.dump(template, file, indent=6)