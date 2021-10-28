# PySimpleGUI Docs: https://pysimplegui.readthedocs.io/en/latest/
import PySimpleGUI as sg
import json


# * Main window function
def main():

    # Innitial layout for employe name column:
    name_column = [[sg.Text(text="Anställd:")]]

    # Innitial layout for employe salary column:
    salary_column = [[sg.Text(text="Lön (1 månad):")]]

    # create the main window
    layout = create_layout(name_column, salary_column, None)
    window = sg.Window(title="Löne räknare", layout=layout, margins=(100, 50))

    # Event Loop
    while True:

        # Get events from window
        event, values = window.read()

        # Close button and X button
        if event == sg.WIN_CLOSED:
            break

        # Import button (run function to import dict from file through GUI)
        elif event == "Importera Löner":
            salaries = import_salaries("salaries.json")

        # Export button (run function to save dict to file through GUI)
        elif event == "Exportera Löner":
            export_salaries(salaries)

        # Calculate Salaries event:
        elif event == "Räkna ut tomma löner":
            # Update dict with GUI values
            salaries = update_dict(values, salaries)

            # Update lists from dict
            workers_list = list(salaries["salaries-monthly"].keys())
            salaries_list = list(salaries["salaries-monthly"].values())

            # Set yearly total salary from dict
            yearly_salary_total = int(salaries["company-yearly"])

            # Get monthly salary total from yearly by dividing by 12
            monthly_salary_total = yearly_salary_total / 12

            # Initialize total_salaries var with 0 value
            total_salaries = 0

            # Loop through salaries and add them up to the total_salaries var
            for salary in salaries_list:
                if salary != None and salary != "":
                    total_salaries += int(salary)

            # Check if inputed salaries excede the yearly total entered and warn the user
            if total_salaries > monthly_salary_total:
                sg.popup(
                    "Angivna löner överskrider företagets års budget!",
                    title="För mycket lön!",
                )
            # Otherwise calculate the empty salaries
            else:
                # Count number of missing salaries
                # https://stackoverflow.com/questions/16455777/python-count-elements-in-a-list-of-objects-with-matching-attributes
                number_of_missing_salaries = sum(
                    1 for s in salaries_list if s == "" or s == None
                )

                # If there is no empty salary boxes, tell the user
                if number_of_missing_salaries <= 0:
                    sg.popup(
                        "Inga tomma lönerutor att räkna ut",
                        title="Inga tomma rutor",
                    )

                # Otherwise calculate the value of each salary
                else:
                    # Calculate the empty salaries value.
                    empty_salaries = int(
                        (monthly_salary_total - total_salaries)
                        / number_of_missing_salaries
                    )

                # Set the values in the dict
                for key in salaries["salaries-monthly"]:
                    if (
                        salaries["salaries-monthly"][key] == None
                        or salaries["salaries-monthly"][key] == ""
                    ):
                        salaries["salaries-monthly"][key] = empty_salaries

        # Create lists from dict (helps for printing to GUI)
        workers_list = list(salaries["salaries-monthly"].keys())
        salaries_list = list(salaries["salaries-monthly"].values())

        # Set yearly total salary from dict
        yearly_salary_total = salaries["company-yearly"]

        # redefine columns (PySimpleGUI wierdness)
        name_column = [[sg.Text(text="Anställd:")]]
        salary_column = [[sg.Text(text="Lön (1 månad):")]]

        # update names list on GUI
        for i in range(len(workers_list)):
            name_column.append([sg.Text(text=workers_list[i], key=f"-NAME_{i}-")])

        # update salaries list on GUI
        for i in range(len(salaries_list)):
            salary_column.append(
                [sg.Input(default_text=salaries_list[i], key=f"-SALARY_{i}-")]
            )

        # recreating window to update content
        # source: https://github.com/PySimpleGUI/PySimpleGUI/issues/845#issuecomment-443862047
        layout1 = create_layout(name_column, salary_column, yearly_salary_total)
        window1 = sg.Window(title="Löne räknare", layout=layout1, margins=(100, 50))
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
            sg.Input(
                key="-YEARLY_SALARY_TOTAL-",
                default_text=yearly_salary_total,
                size=(10, 1),
            ),
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
def import_salaries(default_file):

    # Create layout for import window
    import_layout = [
        [
            sg.Input(key="-File-", default_text=default_file),
            sg.FileBrowse(file_types=[("json", "*.json")]),
        ],
        [sg.Button("Klar"), sg.Button("Avbryt")],
    ]

    # create the window
    import_window = sg.Window(
        title="Importera löner från fil",
        layout=import_layout,
        margins=(50, 25),
        modal=True,
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
        title="Exportera löner till fil",
        layout=export_layout,
        margins=(50, 25),
        modal=True,
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


# * Update dict with GUI values
def update_dict(values, dict):

    # Update the company yearly value from GUI
    dict["company-yearly"] = values["-YEARLY_SALARY_TOTAL-"]

    # Loop through monthly salaries and update their
    for i in range(len(dict["salaries-monthly"])):
        key = list(dict["salaries-monthly"].keys())[i]

        dict["salaries-monthly"][key] = values[f"-SALARY_{i}-"]

    # Return updated dict
    return dict


# * If this file is run directly, run main function
if __name__ == "__main__":
    main()
