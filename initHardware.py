import utime
from machine import PWM, Pin, I2C

import DRV8825
from color_wheel import ColorWheel
from display import Display
from rotary_encoder import RotaryEncoder
from shot_tray import ShotTray
from water_pump import WaterPump


def init_display() -> Display:
    i2c = I2C(0, sda=Pin(0), scl=Pin(1))
    oled = Display(i2c)
    return oled


def init_color_wheel() -> ColorWheel:
    bluePin = PWM(Pin(2))
    greenPin = PWM(Pin(4))
    redPin = PWM(Pin(5))

    color_wheel = ColorWheel(bluePin, greenPin, redPin)

    color_wheel.showRed()
    utime.sleep(2)
    color_wheel.showYellow()
    utime.sleep(2)
    color_wheel.showGreen()
    utime.sleep(2)
    color_wheel.showBlue()
    utime.sleep(2)

    return color_wheel


def init_rotary_encoder() -> RotaryEncoder:
    encoderAPin = Pin(15, Pin.IN, Pin.PULL_UP)
    encoderBPin = Pin(14, Pin.IN, Pin.PULL_UP)

    rotary_encoder = RotaryEncoder(encoderAPin, encoderBPin)
    utime.sleep(3)
    return rotary_encoder


def init_stepper_motor() -> DRV8825.A4988Nema:
    dirPin = Pin(13, Pin.OUT, value=0)
    stepPin = Pin(12, Pin.OUT, Pin.PULL_DOWN)
    enablePinPin = Pin(11, Pin.OUT, value=0)

    endSwitchPin = Pin(28, Pin.IN, Pin.PULL_DOWN)  # Endschalter

    stepper: DRV8825.A4988Nema = DRV8825.A4988Nema(dirPin, stepPin, enablePinPin, endSwitchPin)
    utime.sleep(3)
    return stepper


def init_start_button() -> Pin:
    startButton = Pin(3, Pin.IN, Pin.PULL_DOWN)
    return startButton


def init_shot_tray() -> ShotTray:
    btn1 = Pin(27, Pin.IN, Pin.PULL_DOWN)
    btn2 = Pin(26, Pin.IN, Pin.PULL_DOWN)
    btn3 = Pin(22, Pin.IN, Pin.PULL_DOWN)
    btn4 = Pin(21, Pin.IN, Pin.PULL_DOWN)
    btn5 = Pin(20, Pin.IN, Pin.PULL_DOWN)
    btn6 = Pin(19, Pin.IN, Pin.PULL_DOWN)
    btn7 = Pin(18, Pin.IN, Pin.PULL_DOWN)
    btn8 = Pin(17, Pin.IN, Pin.PULL_DOWN)

    shot_tray = ShotTray(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    utime.sleep(3)
    return shot_tray


def init_water_pump() -> WaterPump:
    pump_pin = Pin(10, Pin.OUT, value=0)
    whiskey_pump = WaterPump(pump_pin)
    return whiskey_pump
