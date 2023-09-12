from machine import Pin, I2C, PWM
import DRV8825
import utime

from color_wheel import ColorWheel
from rotary_encoder import RotaryEncoder
from display import Display

Objectname = open("fillLevel.txt", "w")
print(open("fillLevel.txt", "r").read())
Objectname.write(str(50))
Objectname.close()
print(open("fillLevel.txt", "r").read())

i2c = I2C(0, sda=Pin(16), scl=Pin(17))
oled = Display(i2c)

###
oled.write_text_to_display(None, "", "Start", "")
utime.sleep(3)
###

###
oled.write_text_to_display(None, "", "Initialisiere", "Farbrad", "")

bluePin = PWM(Pin(11))
greenPin = PWM(Pin(12))
redPin = PWM(Pin(13))

color_wheel = ColorWheel(bluePin, greenPin, redPin)

color_wheel.showRed()
utime.sleep(2)
color_wheel.showYellow()
utime.sleep(2)
color_wheel.showGreen()
utime.sleep(2)
color_wheel.showBlue()
utime.sleep(2)
###

###
oled.write_text_to_display(None, "", "Initialisiere", "Drehschalter", "")

encoderAPin = Pin(22, Pin.IN, Pin.PULL_UP)
encoderBPin = Pin(26, Pin.IN, Pin.PULL_UP)

rotary_encoder = RotaryEncoder(encoderAPin, encoderBPin)
###

###
oled.write_text_to_display(None, "", "Initialisiere", "Stepper Motor", "")

dirPin = Pin(20, Pin.OUT, value=0)
stepPin = Pin(19, Pin.OUT, Pin.PULL_DOWN)
enablePinPin = Pin(18, Pin.OUT, value=0)

stepper = DRV8825.A4988Nema(dirPin, stepPin)
utime.sleep(3)
###

###
oled.write_text_to_display(None, "", "Fahre zu ", "Nullposition", "")

stepperAdjustPin = Pin(14, Pin.IN, Pin.PULL_DOWN)  # K4
while stepperAdjustPin.value() == 1:
    stepper.motor_go(clockwise=False, steps=5, stepdelay=.005, verbose=False, initdelay=.00)

oled.write_text_to_display(None, "", "Nullposition", "erreicht", "")
utime.sleep(3)


###
def start_rotate():
    enPin = Pin(18, Pin.OUT, value=0)
    oneStep = 200
    lastPos = 0
    print("Start")

    if button1.value():
        stepper.motor_go(clockwise=True, steps=lastPos, stepdelay=.005, verbose=False, initdelay=.00)
        if button1.value():
            print("Befülle Glas Nr 1")
            print(lastPos)
            utime.sleep(2)
        lastPos = 0

    lastPos = lastPos + oneStep
    if button2.value():
        stepper.motor_go(clockwise=True, steps=lastPos, stepdelay=.005, verbose=False, initdelay=.00)
        if button2.value():
            print("Befülle Glas Nr 2")
            print(lastPos)
            utime.sleep(2)
        lastPos = 0

    lastPos = lastPos + oneStep
    if button3.value():
        stepper.motor_go(clockwise=True, steps=lastPos, stepdelay=.005, verbose=False, initdelay=.00)
        if button3.value():
            print("Befülle Glas Nr 3")
            print(lastPos)
            utime.sleep(2)
        lastPos = 0

    lastPos = lastPos + oneStep
    if button4.value():
        stepper.motor_go(clockwise=True, steps=lastPos, stepdelay=.005, verbose=False, initdelay=.00)
        if button4.value():
            print("Befülle Glas Nr 4")
            print(lastPos)
            utime.sleep(2)
        lastPos = 0

    lastPos = lastPos + oneStep
    if button5.value():
        stepper.motor_go(clockwise=True, steps=lastPos, stepdelay=.005, verbose=False, initdelay=.00)
        if button5.value():
            print("Befülle Glas Nr 5")
            print(lastPos)
            utime.sleep(2)
        lastPos = 0

    lastPos = lastPos + oneStep
    if button6.value():
        stepper.motor_go(clockwise=True, steps=lastPos, stepdelay=.005, verbose=False, initdelay=.00)
        if button6.value():
            print("Befülle Glas Nr 6")
            print(lastPos)
            utime.sleep(2)
        lastPos = 0

    lastPos = lastPos + oneStep
    if button7.value():
        stepper.motor_go(clockwise=True, steps=lastPos, stepdelay=.005, verbose=False, initdelay=.00)
        if button7.value():
            print("Befülle Glas Nr 7")
            print(lastPos)
            utime.sleep(2)
        lastPos = 0

    lastPos = lastPos + oneStep
    if button8.value():
        stepper.motor_go(clockwise=True, steps=lastPos, stepdelay=.005, verbose=False, initdelay=.00)
        if button8.value():
            print("Befülle Glas Nr 8")
            print(lastPos)
            utime.sleep(2)
        lastPos = 0

    while stepperAdjustPin.value() == 1:
        stepper.motor_go(clockwise=False, steps=5, stepdelay=.005, verbose=False, initdelay=.00)

    enPin.value(1)


###
oled.write_text_to_display(None, "", "Initialisiere", "Glaserkennung", "")

button1 = Pin(1, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(2, Pin.IN, Pin.PULL_DOWN)
button3 = Pin(3, Pin.IN, Pin.PULL_DOWN)
button4 = Pin(4, Pin.IN, Pin.PULL_DOWN)
button5 = Pin(5, Pin.IN, Pin.PULL_DOWN)
button6 = Pin(6, Pin.IN, Pin.PULL_DOWN)
button7 = Pin(7, Pin.IN, Pin.PULL_DOWN)
button8 = Pin(8, Pin.IN, Pin.PULL_DOWN)

utime.sleep(3)


###

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


buttonStart = Pin(15, Pin.IN, Pin.PULL_DOWN)
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
