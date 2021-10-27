# PySimpleGUI Docs: https://pysimplegui.readthedocs.io/en/latest/
import PySimpleGUI as sg

# Import other programs
import salary_calculator
import salary_increase
import lunch_tracker


def main():
    layout = [
        [
            sg.Button("Starta löneuträknare"),
            sg.Button("Starta löneöknings räknare"),
            sg.Button("Starta lunch spårare"),
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
        elif event == "Starta lunch spårare":
            lunch_tracker.main()

    window.close()


if __name__ == "__main__":
    main()
