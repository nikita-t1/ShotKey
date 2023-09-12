def initColorWheel():
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

    return color_wheel