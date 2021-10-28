# PySimpleGUI Docs: https://pysimplegui.readthedocs.io/en/latest/
import PySimpleGUI as sg
import json
from datetime import date

# * Main program function
def main():

    with open("lunches.json", "r") as f:
        lunches = json.load(f)

    display_column = [
        [sg.Text(text="Lunch kostnader:")],
        [sg.Text(text="Senaste 30 dagarna:")],
    ]

    layout = create_layout(display_column)

    window = sg.Window(title="Lunch spårare", layout=layout, margins=(100, 50))

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        elif event == "Importera luncher":
            lunches = import_lunches("lunches.json")

        elif event == "Exportera luncher":
            export_lunches(lunches)

        elif event == "Spara":
            lunches = save_lunch(
                lunch_date=window[
                    "-DATE_TEXT-"
                ].get(),  # Getting the value of text elemnts is wierd...
                lunch_type=values["-LUNCH_TYPE-"],
                lunch_dict=lunches,
            )

            print(lunches)

        # redefine column (PySimpleGUI wierdness)
        display_column = [
            [sg.Text(text="Lunch kostnader:")],
            [sg.Text(text="Senaste 30 dagarna:")],
        ]

        # recreating window to update content
        # source: https://github.com/PySimpleGUI/PySimpleGUI/issues/845#issuecomment-443862047
        layout1 = create_layout(display_column)
        window1 = sg.Window(title="Lunch spårare", layout=layout1, margins=(100, 50))
        window.close()
        window = window1

    window.close()


# * Create layout for entire window
def create_layout(display_column):
    date_today = date.today().strftime("%Y-%m-%d")

    # Define column for creating new lunch
    new_lunch_column = [
        [sg.Text(text="Spara ny lunch:")],
        [
            sg.Text(text="Datum för lunch:"),
            sg.Text(text=date_today, key="-DATE_TEXT-"),
            sg.CalendarButton(
                button_text="Byta datum", key="-DATE_INPUT-", format="%Y-%m-%d"
            ),  # button for getting date
        ],
        [
            sg.OptionMenu(
                ["Ingen lunch", "Vanlig lunch (75kr)", "Lyx lunch (125kr)"],
                key="-LUNCH_TYPE-",
                default_value="Välj lunch alternativ",
                expand_x=True,
            ),
            sg.Button("Spara"),
        ],
    ]

    # Define base layout
    layout = [
        # top buttons:
        [sg.Button("Importera luncher"), sg.Button("Exportera luncher")],
        # horizontal separator
        [sg.HSeparator()],
        # main part of the layout:
        [
            # Create column for inputing new lunch
            sg.Column(layout=new_lunch_column),
            sg.VSeparator(),
            # Create column for displaying data on lunches
            sg.Column(layout=display_column),
        ],
    ]

    # Return the layout
    return layout


# * Import salaries from file with GUI window
def import_lunches(default_file):

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
        lunches = None

        # Cancel button event
        if event == "Avbryt" or event == sg.WIN_CLOSED:
            break

        # Done button event
        elif event == "Klar":

            # Set filename to input
            lunches_file = values["-File-"]

            # If no file return None value
            if lunches_file == "":
                break

            # Read from file and set salaries dict to content
            with open(lunches_file, "r") as f:
                lunches = json.load(f)

            break

    # Close import window when done
    import_window.close()

    # Return salaries dict
    return lunches


# * Save dict to file through GUI window
def export_lunches(lunches):

    # Create export window layout
    export_layout = [
        [sg.Input(key="-File-"), sg.FileBrowse(file_types=[("json", "*.json")])],
        [sg.Button("Klar"), sg.Button("Avbryt")],
    ]

    # Create window
    export_window = sg.Window(
        title="Exportera luncher till fil",
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
            lunches_file = values["-File-"]

            # If no file cancel
            if lunches_file == "":
                break

            # save dict to file
            with open(lunches_file, "w") as f:
                json.dump(lunches, f, indent=4)

            break

    # Close window when done
    export_window.close()


# * function for saving lunches from GUI to dict (doesn't save to file)
def save_lunch(lunch_date: str, lunch_type: str, lunch_dict: dict):

    if lunch_type == "Välj lunch alternativ":
        sg.popup("FEL!", "Välj en lunch typ och försök igen!", title="ERROR")
        return lunch_dict

    elif lunch_type == "Ingen lunch":
        lunch_cost = 0

    elif lunch_type == "Vanlig lunch (75kr)":
        lunch_cost = 75

    elif lunch_type == "Lyx lunch (125kr)":
        lunch_cost = 125

    lunch_dict["lunches"][lunch_date] = lunch_cost

    return lunch_dict


# * If this file is run directly, run main function
if __name__ == "__main__":
    main()
