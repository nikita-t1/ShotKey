import utime
from machine import Pin

import DRV8825
from initHardware import init_color_wheel, init_rotary_encoder, init_stepper_motor, init_display, init_shot_tray, \
    init_start_button
from color_wheel import ColorWheel
from rotary_encoder import RotaryEncoder
from shot_tray import ShotTray

oled = init_display()

###
oled.write_text_to_display(None, "", "Start", "")
utime.sleep(3)
###

###
oled.write_text_to_display(None, "", "Initialisiere", "Farbrad", "")
color_wheel: ColorWheel = init_color_wheel()
###

###
oled.write_text_to_display(None, "", "Initialisiere", "Drehschalter", "")
rotary_encoder: RotaryEncoder = init_rotary_encoder()
###

###
oled.write_text_to_display(None, "", "Initialisiere", "Glaserkennung", "")
shot_tray: ShotTray = init_shot_tray()
###

###
oled.write_text_to_display(None, "", "Initialisiere", "Stepper Motor", "")
stepper: DRV8825.A4988Nema = init_stepper_motor()
###

###
oled.write_text_to_display(None, "", "Fahre zu ", "Nullposition", "")
stepper.move_to_end_switch()
oled.write_text_to_display(None, "", "Nullposition", "erreicht", "")
utime.sleep(3)
###

buttonStart = init_start_button()

def start_rotate():
    print("Starte Ablauf")

    if shot_tray.tray_1.value():
        stepper.move_to_position(0)

    if shot_tray.tray_2.value():
        stepper.move_to_position(1)

    if shot_tray.tray_3.value():
        stepper.move_to_position(2)

    if shot_tray.tray_4.value():
        stepper.move_to_position(3)

    if shot_tray.tray_5.value():
        stepper.move_to_position(4)

    if shot_tray.tray_6.value():
        stepper.move_to_position(5)

    if shot_tray.tray_7.value():
        stepper.move_to_position(6)

    if shot_tray.tray_8.value():
        stepper.move_to_position(7)

    stepper.move_to_end_switch()


class UI_Screen:
    Main = 0
    AdjustFillLevel = 1
    Settings = 2
    Credits = 3

    def __init__(self):
        self.currentScreen = self.Main

    def get(self):
        return self.currentScreen

    def show(self):
        print("show")
        print(str(self.currentScreen))
        if self.currentScreen == 0:
            oled.write_text_to_display(None, "Einsatzbereit", "", "Fuellstand", "69%")
        elif self.currentScreen == 1:
            oled.write_text_to_display(None, "Hier laesst", "sich spaeter der", "Stepper manuell", "drehen")
        elif self.currentScreen == 2:
            oled.write_text_to_display(None, "Hier laesst", "sich spaeter der", "Fuellstand", "bearbeiten")
        elif self.currentScreen == 3:
            oled.write_text_to_display(None, "Created by", "Max Schaefer", "Noah Roeschard", "Nikita Tarasov")
        return self

    def next(self):
        screen = self.currentScreen + 1
        if screen > 3:
            screen = 0
        self.currentScreen = screen
        return self

    def previous(self):
        screen = self.currentScreen - 1
        if screen < 0:
            screen = 3
        self.currentScreen = screen
        return self


oled.write_text_to_display(None, "Einsatzbereit", "", "Fuellstand", "69%")
color_wheel.showGreen()

screen = UI_Screen()
while True:
    enc = rotary_encoder.readRotaryEncoder()
    if enc == rotary_encoder.ROTARY_CW:
        screen.next().show()
        print("    ~~> rotary increase [clockwise]")
    elif enc == rotary_encoder.ROTARY_CCW:
        screen.previous().show()
        print("    ~~> rotary decrease [counter clockwise]")
    if buttonStart.value():
        start_rotate()
        color_wheel.showYellow()
        utime.sleep(3)
        print("Ablauf beendet")
        color_wheel.showGreen()
