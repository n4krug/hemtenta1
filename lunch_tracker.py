# PySimpleGUI Docs: https://pysimplegui.readthedocs.io/en/latest/
import PySimpleGUI as sg

# * Main program function
def main():

    layout = create_layout()

    window = sg.Window(title="Lunch spårare", layout=layout, margins=(100, 50))

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

    window.close()


# * Create layout for entire window
def create_layout():

    # Define column for creating new lunch
    new_lunch_column = [
        [sg.Text(text="Spara ny lunch:")],
        [
            sg.Text(text="Datum för lunch:"),
            sg.Text(text="MM-DD-YY", key="-DATE_TEXT-"),
            sg.CalendarButton(
                button_text="Choose date", target=(1, 0), key="-DATE_INPUT-"
            ),  # button for getting date
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
        ],
    ]

    # Return the layout
    return layout


# * If this file is run directly, run main function
if __name__ == "__main__":
    main()
