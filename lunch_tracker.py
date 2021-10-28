# PySimpleGUI Docs: https://pysimplegui.readthedocs.io/en/latest/
import PySimpleGUI as sg
import json

# python datetime Docs: https://docs.python.org/3/library/datetime.html
from datetime import date

# * Main program function
def main():

    # load lunches from default file (lunches.json)
    with open("lunches.json", "r") as f:
        lunches = json.load(f)

    employe = "Anna"  # set default employe

    layout = create_layout(lunches, employe)  # create the screen layout

    window = sg.Window(
        title="Lunch spårare", layout=layout, margins=(100, 50)
    )  # create a window with layout

    # * Event loop
    while True:
        (
            event,
            values,
        ) = window.read()  # Get events (button presses etc.) and values from GUI

        employe = values["-EMPLOYE_SELECT-"]  # set var employe to the selected employe

        # window close event
        if event == sg.WINDOW_CLOSED:
            break

        # import event
        elif event == "Importera luncher":
            lunches = import_lunches("lunches.json")

        # export event
        elif event == "Exportera luncher":
            export_lunches(lunches)

        # save/report new lunch event
        elif event == "Spara":
            lunches = save_lunch(
                lunch_date=window[
                    "-DATE_TEXT-"
                ].get(),  # Getting the value of text elemnts is wierd...
                lunch_type=values["-LUNCH_TYPE-"],
                lunch_dict=lunches,
                employe=employe,
            )

        # recreating window to update content
        # source: https://github.com/PySimpleGUI/PySimpleGUI/issues/845#issuecomment-443862047
        layout1 = create_layout(lunches, employe)
        window1 = sg.Window(title="Lunch spårare", layout=layout1, margins=(100, 50))
        window.close()
        window = window1

    window.close()


# * Create layout for entire window
def create_layout(lunch_dict, employe):
    date_today = date.today().strftime("%Y-%m-%d")  # get the current date

    # Define column for creating new lunch
    new_lunch_column = [
        [sg.Text(text="Spara ny lunch:")],
        [
            sg.Text(text="Datum för lunch:"),
            sg.Text(
                text=date_today, key="-DATE_TEXT-"
            ),  # display the chosen date (innitialises to todays date)
            sg.CalendarButton(
                button_text="Byta datum", key="-DATE_INPUT-", format="%Y-%m-%d"
            ),  # button for getting date
        ],
        [
            sg.OptionMenu(  # dropdown menu for chosing type of lunch to save/report
                ["Ingen lunch", "Vanlig lunch (75kr)", "Lyx lunch (125kr)"],
                key="-LUNCH_TYPE-",
                default_value="Välj lunch alternativ",
                expand_x=True,
            ),
            sg.Button("Spara"),  # button for saving the lunch
        ],
    ]

    # * create last 7 days column
    lunches_7days = get_lunches(
        lunch_dict, 7, employe
    )  # get the lunches from the last 7 days
    sum_lunches_7days = sum(lunches_7days.values())  # add upp the cost of the lunches

    lunches_7days_page = [  # create the layout for the last 7 days page
        [sg.Text("Senaste 7 dagarna")],
        [
            sg.Text("Totalt:"),
            sg.Text(f"{sum_lunches_7days} kr"),
        ],  # display the total amount spent in the last 7 days
    ]

    # * create last 30 days column
    lunches_30days = get_lunches(
        lunch_dict, 30, employe
    )  # get the lunches from the last 30 days
    sum_lunches_30days = sum(lunches_30days.values())  # add upp the cost of the lunches

    lunches_30days_page = [  # create the layout for the last 30 days page
        [sg.Text("Senaste 30 dagarna")],
        [
            sg.Text("Totalt:"),
            sg.Text(f"{sum_lunches_30days} kr"),
        ],  # display the total amount spent in the last 30 days
    ]

    # * create last 30 days column
    lunches_365days = get_lunches(
        lunch_dict, 365, employe
    )  # get the lunches from the last 365 days
    sum_lunches_365days = sum(
        lunches_365days.values()
    )  # add upp the cost of the lunches

    lunches_365days_page = [  # create the layout for the last 365 days page
        [sg.Text("Senaste 365 dagarna")],
        [
            sg.Text("Totalt:"),
            sg.Text(f"{sum_lunches_365days} kr"),
        ],  # display the total amount spent in the last 365 days
    ]

    # create tabs for chosing number of days https://csveda.com/creating-tabbed-interface-using-pysimplegui/
    # uses layouts created above
    display_column = [
        [
            sg.TabGroup(
                [
                    [sg.Tab(title="Senaste 7 dagarana", layout=lunches_7days_page)],
                    [sg.Tab(title="Senaste 30 dagarana", layout=lunches_30days_page)],
                    [sg.Tab(title="Senaste 365 dagarana", layout=lunches_365days_page)],
                ],
            )
        ]
    ]

    # Define base layout
    layout = [
        # top buttons:
        [
            sg.Button("Importera luncher"),  # button for importing lunches
            sg.Button("Exportera luncher"),  # button for exporting lunches
            sg.Text(  # empty text element for spacing out to buttons
                " ", expand_x=True
            ),
            sg.OptionMenu(  # create dropdown select with employes
                values=lunch_dict.keys(),
                default_value=employe,
                size=(10, 1),
                key="-EMPLOYE_SELECT-",
            ),
            sg.Button("Välj"),  # Empty button wich makes GUI update
        ],
        # horizontal separator
        [sg.HSeparator()],
        # main part of the layout:
        [
            # Create column for inputing new lunch
            sg.Column(layout=new_lunch_column),
            sg.VSeparator(),  # Vertical separiting line
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
        title="Importera luncher från fil",
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
def save_lunch(lunch_date: str, lunch_type: str, lunch_dict: dict, employe: str):

    # if no lunch type was selected warn user and don't add anything to the dict
    if lunch_type == "Välj lunch alternativ":
        sg.popup("FEL!", "Välj en lunch typ och försök igen!", title="ERROR")
        return lunch_dict

    # if type is no lunch set cost 0
    elif lunch_type == "Ingen lunch":
        lunch_cost = 0

    # if type is normal lunch set cost 75
    elif lunch_type == "Vanlig lunch (75kr)":
        lunch_cost = 75

    # if type is luxury lunch set cost 125
    elif lunch_type == "Lyx lunch (125kr)":
        lunch_cost = 125

    # save lunch entry with date and cost to dict
    lunch_dict[employe][lunch_date] = lunch_cost

    # return the updated dict
    return lunch_dict


# * Function for getting last {N} days of lunch
def get_lunches(lunch_dict: dict, number_of_days: int, employe: str):

    # initialize a new empty dict
    last_lunches = {}

    # get all the lunches from chosen employe
    all_dates = list(lunch_dict[employe].keys())

    # loop through the lunches
    for lunch_date_text in all_dates:

        # split the current lunch's date into a array with year, month, and day
        # [YYYY, MM, DD]
        lunch_date_list = lunch_date_text.split("-")

        lunch_date = date(  # convert list to date object
            int(lunch_date_list[0]), int(lunch_date_list[1]), int(lunch_date_list[2])
        )

        lunch_date_ordinal = (
            lunch_date.toordinal()
        )  # convert the date object to ordinal string (number of days since 0001-01-01)

        today = date.today().toordinal()  # get todays date in ordinal form

        if (  # Check if current lunch date is within the last {N} amount of days
            today - lunch_date_ordinal < number_of_days
            and today - lunch_date_ordinal >= 0
        ):
            # save the lunch top the new dict
            last_lunches[lunch_date_text] = lunch_dict[employe][lunch_date_text]

    # return dict containing all lunches from last {N} amount of days
    return last_lunches


# * If this file is run directly, run main function
if __name__ == "__main__":
    main()
