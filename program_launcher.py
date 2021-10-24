# PySimpleGUI Docs: https://pysimplegui.readthedocs.io/en/latest/
import PySimpleGUI as sg

# Import other programs
import salary_calculator
import salary_increase


def main():
    layout = [
        [
            sg.Button("Starta löneuträknare"),
            sg.Button("Starta löneöknings räknare"),
        ]
    ]

    window = sg.Window(title="Programstartare", layout=layout, margins=(100, 50))

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == "Starta löneuträknare":
            salary_calculator.main()
        elif event == "Starta löneöknings räknare":
            salary_increase.main()

    window.close()


if __name__ == "__main__":
    main()
