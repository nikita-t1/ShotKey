import utime
from machine import Pin

import DRV8825
from color_wheel import ColorWheel
from initHardware import init_color_wheel, init_rotary_encoder, init_stepper_motor, init_display, init_shot_tray, \
    init_start_button, init_water_pump
from rotary_encoder import RotaryEncoder
from shot_tray import ShotTray
from ui_screen import UiScreen

# Initialize Display
oled = init_display()
oled.write_text_to_display(None, "", "Start", "")
utime.sleep(3)

# Initialize the color wheel on the rotary encoder
oled.write_text_to_display(None, "", "Initialisiere", "Farbrad", "")
color_wheel: ColorWheel = init_color_wheel()

# Initialize the rotary encoder
oled.write_text_to_display(None, "", "Initialisiere", "Drehschalter", "")
rotary_encoder: RotaryEncoder = init_rotary_encoder()

# Initialize buttons on the shot tray
oled.write_text_to_display(None, "", "Initialisiere", "Glaserkennung", "")
shot_tray: ShotTray = init_shot_tray()

# Initialize the stepper motor
oled.write_text_to_display(None, "", "Initialisiere", "Stepper Motor", "")
stepper: DRV8825.A4988Nema = init_stepper_motor()

# Move the stepper motor counterclockwise until the end switch is reached
oled.write_text_to_display(None, "", "Fahre zu ", "Nullposition", "")
stepper.move_to_end_switch()
oled.write_text_to_display(None, "", "Nullposition", "erreicht", "")
utime.sleep(3)

# Initialize the water pump
oled.write_text_to_display(None, "", "Initialisiere", "Pumpe", "")
pump = init_water_pump()

# Initialize the UI screens
ui_screen: UiScreen = UiScreen(oled, shot_tray, pump, stepper, color_wheel)

# Initialize the start button (on the rotary encoder)
buttonStart: Pin = init_start_button()
color_wheel.showGreen()
oled.write_text_to_display(None, "", "Initialisierung", "abgeschlossen", "")
utime.sleep(3)


def fill_shots():
    color_wheel.showYellow()

    for i in range(0, 8):
        if shot_tray.trays[i].value():
            oled.write_text_to_display(None, "", "Fahre zu", "Position", str(i + 1))
            stepper.move_to_position(i)
            # Recheck if the glass is still there before filling
            if shot_tray.trays[i].value():
                oled.write_text_to_display(None, "", "Fuelle Glas", str(i + 1), "")
                pump.fill_shot()
                utime.sleep(3)
            # oled.write_text_to_display(None, "", "Current Position", str(stepper.current_position), "")

    oled.write_text_to_display(None, "", "Fahre zu", "Endposition", "")
    stepper.move_to_end_switch()
    oled.write_text_to_display(None, "", "Endposition", "erreicht", "")
    utime.sleep(1)


# debounce the button
current_button_state = False

# Main loop
while True:
    ui_screen.show()
    enc: int = rotary_encoder.readRotaryEncoder()
    if enc == rotary_encoder.ROTARY_CW:
        print("    ~~> rotary increase [clockwise]")

        if ui_screen.get() == ui_screen.AdjustShotSize and ui_screen.screen_selected:
            pump.change_shot_size(pump.default_shot_size + 1)
        elif ui_screen.get() == ui_screen.MoveToPos and ui_screen.screen_selected:
            if stepper.current_position < 7:
                stepper.move_to_position(stepper.current_position + 1)
        else:
            ui_screen.next().show()
    elif enc == rotary_encoder.ROTARY_CCW:
        print("    ~~> rotary decrease [counter clockwise]")

        if ui_screen.get() == ui_screen.AdjustShotSize and ui_screen.screen_selected:
            pump.change_shot_size(pump.default_shot_size - 1)
        elif ui_screen.get() == ui_screen.MoveToPos and ui_screen.screen_selected:
            if stepper.current_position > 0:
                stepper.move_to_position(stepper.current_position - 1)
        else:
            ui_screen.previous().show()

    if buttonStart.value() and not current_button_state:
        current_button_state = True
        if ui_screen.get() == ui_screen.Main:
            if stepper.current_position != 0:
                stepper.move_to_end_switch()
            else:
                fill_shots()
        elif ui_screen.get() == ui_screen.AdjustShotSize:
            ui_screen.selectScreen()
        elif ui_screen.get() == ui_screen.MoveToPos:
            ui_screen.selectScreen()
        elif ui_screen.get() == ui_screen.TurnOnPump:
            color_wheel.showYellow()
            pump.turn_on_for_duration(10)

        utime.sleep(0.3)
        current_button_state = False
