# PySimpleGUI Docs: https://pysimplegui.readthedocs.io/en/latest/
import PySimpleGUI as sg

# import function from salary calculator
from salary_calculator import import_salaries, update_dict


def main():
    # Innitial layout for employe name column:
    name_column = [[sg.Text(text="Anställd:")]]

    # Innitial layout for employe salary column:
    salary_column = [[sg.Text(text="Lön (1 månad):")]]

    # Innitial layout for employe salary column:
    next_year_column = [[sg.Text(text="Lön nästa år (1 månad):")]]

    layout = create_layout(
        name_column, salary_column, next_year_column, None, None, "5"
    )

    window = sg.Window("Löneöknings räknare", layout=layout, margins=(100, 50))

    next_year_salaries = {
        "total": "",
        "employes": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    }

    increase = "5"

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        # Import button (run function to import dict from file through GUI)
        elif event == "Importera Löner":
            salaries = import_salaries("salaries-2019.json")

        elif event == "Räkna ut nästa års löner":
            salaries = update_dict(values, salaries)

            increase = values["-SALARY_INCREASE-"]

            next_year_salaries = calc_next_year(salaries, increase)

        # Create lists from dict (helps for printing to GUI)
        workers_list = list(salaries["salaries-monthly"].keys())
        salaries_list = list(salaries["salaries-monthly"].values())

        # Set yearly total salary from dict
        yearly_salary_total = salaries["company-yearly"]

        # redefine columns (PySimpleGUI wierdness)
        name_column = [[sg.Text(text="Anställd:")]]
        salary_column = [[sg.Text(text="Lön (1 månad):")]]
        next_year_column = [[sg.Text(text="Lön nästa år (1 månad):")]]

        # Set yearly total salary from dict
        yearly_salary_total = salaries["company-yearly"]

        # Set next year total salary from dict
        next_year_total = next_year_salaries["total"]

        # update names list on GUI
        for i in range(len(workers_list)):
            name_column.append([sg.Text(text=workers_list[i], key=f"-NAME_{i}-")])

        # update salaries list on GUI
        for i in range(len(salaries_list)):
            salary_column.append(
                [
                    sg.Input(
                        default_text=salaries_list[i], key=f"-SALARY_{i}-", size=(10, 1)
                    ),
                    sg.Text("kr"),
                ]
            )

            next_year_column.append(
                [
                    sg.Text(
                        next_year_salaries["employes"][i], key=f"-NEXT_YEAR_SALARY_{i}-"
                    ),
                    sg.Text("kr"),
                ]
            )

        # recreating window to update content
        # source: https://github.com/PySimpleGUI/PySimpleGUI/issues/845#issuecomment-443862047
        layout1 = create_layout(
            name_column,
            salary_column,
            next_year_column,
            yearly_salary_total,
            next_year_total,
            increase,
        )
        window1 = sg.Window(title="Test", layout=layout1, margins=(100, 50))
        window.close()
        window = window1

    window.close()


def create_layout(
    name_column,
    salary_column,
    next_year_column,
    yearly_salary_total,
    next_year_total,
    increase,
):
    layout = [
        # top buttons:
        [sg.Button("Importera Löner")],
        # horizontal separator
        [sg.HSeparator()],
        # main part of the layout:
        [
            sg.Text("Total lön (1 år):"),
            sg.Input(
                key="-YEARLY_SALARY_TOTAL-",
                default_text=yearly_salary_total,
                size=(10, 1),
            ),
            sg.Text("kr"),
        ],
        [
            sg.Text("Total lön (nästa år):"),
            sg.Text(key="-YEARLY_SALARY_NEXT_YEAR-", text=next_year_total),
            sg.Text("kr"),
        ],
        [
            # add name column to main layout
            sg.Column(name_column),
            sg.VSeparator(),  # vertical separator line
            # add salary column to main layout
            sg.Column(salary_column),
            sg.VSeparator(),  # vertical separator line
            # add next year column to main layout
            sg.Column(next_year_column),
        ],
        [
            sg.Text("Ökning nästa år (procent):"),
            sg.Input(default_text=increase, size=(3, 1), key="-SALARY_INCREASE-"),
            sg.Text("%"),
            sg.Button("Räkna ut nästa års löner"),
        ],
    ]

    return layout


def calc_next_year(salaries, increase):
    next_year_salaries = {
        "total": 0,
        "employes": [],
    }

    factorial_increase = 1 + int(increase) / 100

    next_year_salaries["total"] = int(
        int(salaries["company-yearly"]) * factorial_increase
    )

    for key in salaries["salaries-monthly"]:
        next_year_salary = int(
            int(salaries["salaries-monthly"][key]) * factorial_increase
        )

        next_year_salaries["employes"].append(next_year_salary)

    print(next_year_salaries)

    return next_year_salaries


# If file is run directly, run main function
if __name__ == "__main__":
    main()
