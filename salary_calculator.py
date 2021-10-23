# PySimpleGUI Docs: https://pysimplegui.readthedocs.io/en/latest/
import PySimpleGUI as sg
import json


# * Main window function
def main():

    # Innitial layout for employe name column:
    name_column = [[sg.Text(text="Anställd:")]]

    # Innitial layout for employe salary column:
    salary_column = [[sg.Text(text="Lön:")]]

    # create the main window
    layout = create_layout(name_column, salary_column, None)
    window = sg.Window(title="Test", layout=layout, margins=(100, 50))

    # Event Loop
    while True:

        # Get events from window
        event, values = window.read()

        # Close button and X button
        if event == sg.WIN_CLOSED:
            break

        # Import button (run function to import dict from file through GUI)
        elif event == "Importera Löner":
            salaries = import_salaries()

        # Export button (run function to save dict to file through GUI)
        elif event == "Exportera Löner":
            export_salaries(salaries)

        # Calculate Salaries event:
        elif event == "Räkna ut tomma löner":
            salaries = update_dict(values, salaries)

        # Create lists from dict (helps for printing to GUI)
        workers_list = list(salaries["salaries-monthly"].keys())
        salaries_list = list(salaries["salaries-monthly"].values())

        # Set yearly total salary from dict
        yearly_salary_total = salaries["company-yearly"]

        # redefine columns (PySimpleGUI wierdness)
        name_column = [[sg.Text(text="Anställd:")]]
        salary_column = [[sg.Text(text="Lön:")]]

        # update names list on GUI
        for i in range(len(workers_list)):
            name_column.append(
                [sg.Input(default_text=workers_list[i], key=f"-NAME_{i}-")]
            )

        # update salaries list on GUI
        for i in range(len(salaries_list)):
            salary_column.append(
                [sg.Input(default_text=salaries_list[i], key=f"-SALARY_{i}-")]
            )

        # recreating window to update content
        # source: https://github.com/PySimpleGUI/PySimpleGUI/issues/845#issuecomment-443862047
        layout1 = create_layout(name_column, salary_column, yearly_salary_total)
        window1 = sg.Window(title="Test", layout=layout1, margins=(100, 50))
        window.close()
        window = window1

    # close window when done (on exit)
    window.close()


# * Create layout for entire window
def create_layout(name_column, salary_column, yearly_salary_total):
    layout = [
        # top buttons:
        [sg.Button("Importera Löner"), sg.Button("Exportera Löner")],
        # horizontal separator
        [sg.HSeparator()],
        # main part of the layout:
        [
            sg.Text("Total lön (1 år)"),
            sg.Input(key="-YEARLY_SALARY_TOTAL-", default_text=yearly_salary_total),
        ],
        [
            # add name column to main layout
            sg.Column(name_column),
            sg.VSeparator(),  # vertical separator line
            # add salary column to main layout
            sg.Column(salary_column),
        ],
        [sg.Button("Räkna ut tomma löner")],
    ]

    return layout


# * Import salaries from file with GUI window
def import_salaries():

    # Create layout for import window
    import_layout = [
        [
            sg.Input(key="-File-", default_text="salaries.json"),
            sg.FileBrowse(file_types=[("json", "*.json")]),
        ],
        [sg.Button("Klar"), sg.Button("Avbryt")],
    ]

    # create the window
    import_window = sg.Window(
        title="Importera löner från fil", layout=import_layout, margins=(50, 25)
    )

    # Event Loop
    while True:
        # Get events from window
        event, values = import_window.read()

        # Set default salary dict to None value
        salaries = None

        # Cancel button event
        if event == "Avbryt" or event == sg.WIN_CLOSED:
            break

        # Done button event
        elif event == "Klar":

            # Set filename to input
            salaries_file = values["-File-"]

            # If no file return None value
            if salaries_file == "":
                break

            # Read from file and set salaries dict to content
            with open(salaries_file, "r") as f:
                salaries = json.load(f)

            break

    # Close import window when done
    import_window.close()

    # Return salaries dict
    return salaries


# * Save dict to file through GUI window
def export_salaries(salaries):

    # Create export window layout
    export_layout = [
        [sg.Input(key="-File-"), sg.FileBrowse(file_types=[("json", "*.json")])],
        [sg.Button("Klar"), sg.Button("Avbryt")],
    ]

    # Create window
    export_window = sg.Window(
        title="Exportera löner till fil", layout=export_layout, margins=(50, 25)
    )

    # Event loop
    while True:

        # Get events from window
        event, values = export_window.read()

        # Cancel button and X button event
        if event == "Avbryt" or event == sg.WIN_CLOSED:
            break

        # Done button event
        elif event == "Klar":

            # Get filename from input
            salaries_file = values["-File-"]

            # If no file cancel
            if salaries_file == "":
                break

            # save dict to file
            with open(salaries_file, "w") as f:
                json.dump(salaries, f, indent=4)

            break

    # Close window when done
    export_window.close()


def update_dict(values, dict):
    dict["company-yearly"] = values["-YEARLY_SALARY_TOTAL-"]

    for i in range(len(dict["salaries-monthly"])):
        key = list(dict["salaries-monthly"].keys())[i]

        dict["salaries-monthly"][key] = values[f"-SALARY_{i}-"]

    return dict


if __name__ == "__main__":
    main()
