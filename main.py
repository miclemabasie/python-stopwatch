import PySimpleGUI as sg
from time import time
import logging


logger = logging.getLogger(__name__)


def create_window():
    sg.theme('black')
    layout = [
        # [sg.Image('images/download.png')],
        [sg.Push(), sg.Text("X", key="-CLOSE-", pad=0, enable_events=True)],
        [sg.VPush()],
        [sg.Text("0:0", font="Young 50", key="-TIME-")],
        [sg.Button("Start", key="-STARTSTOP-", button_color=("#FFFFFF", "#ff0000"), border_width=0),
         sg.Button('Lap', key="-LAP-", button_color=("#FFFFFF", "#FF0000"), border_width=0, visible=False)],
        [sg.Column([[]], key='-LAPS-')],
        [sg.VPush()]

    ]

    return sg.Window('Stopwatch', layout, size=(300, 300),
                     no_titlebar=True, element_justification='center')


def main():
    app = create_window()
    start_time = 0
    active = False
    lap_ammount = 1
    while True:
        event, value = app.read(timeout=10)

        if event == (sg.WIN_CLOSED or '-CLOSE-'):
            break

        if event == '-STARTSTOP-':
            if active:
                # from active to stop
                active = False
                app['-STARTSTOP-'].update("Reset")
                app['-LAP-'].update(visible=False)

            else:
                # from stop to active
                if start_time > 0:
                    app.close()
                    app = main()
                    start_time = 0
                    lap_ammount = 1
                else:
                    # from start to active
                    start_time = time()
                    active = True
                    app['-STARTSTOP-'].update("Stop")
                    app['-LAP-'].update(visible=True)

        if active:
            elapsed_time = round(time() - start_time, 1)
            app['-TIME-'].update(elapsed_time)

        if event == '-LAP-':
            app.extend_layout(
                app['-LAPS-'], [[sg.Text(lap_ammount), sg.VSeparator(), sg.Text(elapsed_time)]])
            lap_ammount += 1
    app.close()


if __name__ == "__main__":
    main()
