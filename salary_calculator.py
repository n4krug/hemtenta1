from tkinter import Event

# * PySimpleGUI Docs: https://pysimplegui.readthedocs.io/en/latest/
import PySimpleGUI as sg
import json


def main():
    salaries = import_default_salaries()

    print(salaries)

    layout = [[sg.Button("Importera Löner")]]

    window = sg.Window(title="Test", layout=layout, margins=(100, 50))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Importera Löner":
            salaries = import_salaries()

    window.close()


def import_default_salaries():
    with open("salaries.json", "r") as f:
        salaries = json.load(f)

    return salaries


def import_salaries():
    import_layout = [
        [sg.Input(key="-File-"), sg.FileBrowse(file_types=[("json", "*.json")])],
        [sg.Button("Klar"), sg.Button("Avbryt")],
    ]

    import_window = sg.Window(
        title="Importera löner från fil", layout=import_layout, margins=(50, 25)
    )

    while True:
        event, values = import_window.read()

        salaries = None

        if event == "Avbryt" or event == sg.WIN_CLOSED:
            break
        elif event == "Klar":
            salaries_file = values["-File-"]

            if salaries_file == "":
                break

            with open(salaries_file, "r") as f:
                salaries = json.load(f)

            break

    import_window.close()

    return salaries


if __name__ == "__main__":
    main()
