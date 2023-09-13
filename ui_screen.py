from DRV8825 import A4988Nema
from color_wheel import ColorWheel
from display import Display
from shot_tray import ShotTray
from water_pump import WaterPump


class UiScreen:
    Main = 0
    AdjustShotSize = 1
    MoveToPos = 2
    Credits = 3
    #TurnOnPump = 4

    screen_selected = False

    def __init__(self, oled: Display, tray: ShotTray, water_pump: WaterPump, stepper: A4988Nema, color_wheel: ColorWheel):
        self.currentScreen = self.Main
        self.oled: Display = oled
        self.tray: ShotTray = tray
        self.water_pump: WaterPump = water_pump
        self.stepper: A4988Nema = stepper
        self.color_wheel: ColorWheel = color_wheel

    def get(self):
        return self.currentScreen

    def show(self):
        if self.currentScreen == 0:
            if self.stepper.current_position != 0:
                self.color_wheel.showYellow()
                self.oled.write_text_to_display(None, "Stepper Motor", "nicht in", "Nullposition", "", "Start druecken")
            elif self.tray.get_amount_of_glasses() == 0:
                self.color_wheel.showYellow()
                self.oled.write_text_to_display(None, "Keine Glaeser", "erkannt", "", "")
            else:
                self.color_wheel.showGreen()
                self.oled.write_text_to_display(None, "Einsatzbereit", "", "Erkannte Glaeser", str(self.tray.get_amount_of_glasses()))
        elif self.currentScreen == 1:
            if self.screen_selected:
                self.color_wheel.showBlue()
                self.oled.write_text_to_display(None, "Shotgroesse", "bearbeiten", "Aktuelle", str(self.water_pump.default_shot_size))
            else:
                self.color_wheel.showGreen()
                self.oled.write_text_to_display(None, "Hier laesst", "sich die", "Shotgroesse", "bearbeiten")
        elif self.currentScreen == 2:
            if self.screen_selected:
                self.color_wheel.showBlue()
                self.oled.write_text_to_display(None, "Aktuelle Position", str(self.stepper.current_position), "")
            else:
                self.color_wheel.showGreen()
                self.oled.write_text_to_display(None, "Fahre den Motor", "zu einer", "bestimmten", "Position")
        elif self.currentScreen == 3:
            self.color_wheel.showGreen()
            self.oled.write_text_to_display(None, "Created by", "Max Schaefer", "Noah Roeschard", "Nikita Tarasov",
                                            "Joshua von Horn")
        return self

    def selectScreen(self):
        self.screen_selected = not self.screen_selected
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
