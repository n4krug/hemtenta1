import json

# * PySimpleGUI Docs: https://pysimplegui.readthedocs.io/en/latest/
import PySimpleGUI as sg


def main():
    salaries = import_default_salaries()

    print(salaries)

    name_column = [
        [sg.Text(text="Anställd:")],
        [sg.Listbox(values=[], enable_events=True, key="-WORKER_LIST-")],
    ]

    salary_column = [
        [sg.Text(text="Lön:")],
        [sg.Listbox(values=[], enable_events=True, key="-SALARY_LIST-")],
    ]

    layout = [
        [sg.Button("Importera Löner"), sg.Button("Exportera Löner")],
        [
            sg.Column(name_column, background_color="#333333"),
            sg.VSeparator(),
            sg.Column(salary_column, background_color="#333333"),
        ],
    ]

    window = sg.Window(title="Test", layout=layout, margins=(100, 50))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Importera Löner":
            salaries = import_salaries()
        elif event == "Exportera Löner":
            export_salaries(salaries)

        workers_list = list(salaries["salaries-monthly"].keys())
        salaries_list = list(salaries["salaries-monthly"].values())

        window["-WORKER_LIST-"].update(workers_list)

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


def export_salaries(salaries):
    export_layout = [
        [sg.Input(key="-File-"), sg.FileBrowse(file_types=[("json", "*.json")])],
        [sg.Button("Klar"), sg.Button("Avbryt")],
    ]

    export_window = sg.Window(
        title="Exportera löner till fil", layout=export_layout, margins=(50, 25)
    )

    while True:
        event, values = export_window.read()

        if event == "Avbryt" or event == sg.WIN_CLOSED:
            break
        elif event == "Klar":
            salaries_file = values["-File-"]

            if salaries_file == "":
                break

            with open(salaries_file, "w") as f:
                json.dump(salaries, f, indent=4)

            break

    export_window.close()


if __name__ == "__main__":
    main()
