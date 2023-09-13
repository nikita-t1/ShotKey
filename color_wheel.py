PWM_FREQ = 5000
COLOUR_MAX = 65535


class ColorWheel:
    def __init__(self, blue_pin, green_pin, red_pin):
        self.blue_pin = blue_pin
        self.green_pin = green_pin
        self.red_pin = red_pin

        self.blue_pin.freq(PWM_FREQ)
        self.blue_pin.duty_u16(COLOUR_MAX)

        self.green_pin.freq(PWM_FREQ)
        self.green_pin.duty_u16(COLOUR_MAX)

        self.red_pin.freq(PWM_FREQ)
        self.red_pin.duty_u16(COLOUR_MAX)

    # Converts a value that exists within a range to a value in another range
    def convertScale(self,
                     value,
                     originMin=0,
                     originMax=255,
                     destinationMin=0,
                     destinationMax=COLOUR_MAX) -> float:
        originSpan = originMax - originMin
        destinationSpan = destinationMax - destinationMin
        scaledValue = float(value - originMin) / float(originSpan)
        return destinationMin + (scaledValue * destinationSpan)

    # This method ensures the value is in the range [0-255]
    # it then maps the value to a number between [0-65535]
    # it then inverts the value
    def normalise(self, colour_element) -> int:
        value = colour_element
        if value > 255:
            value = 255
        if value < 0:
            value = 0
        return COLOUR_MAX - int(self.convertScale(value))

    def setColourRGB(self, red, green, blue):
        self.red_pin.duty_u16(self.normalise(red))
        self.green_pin.duty_u16(self.normalise(green))
        self.blue_pin.duty_u16(self.normalise(blue))

    def showGreen(self):
        self.setColourRGB(0, 128, 0)

    def showBlue(self):
        self.setColourRGB(0, 0, 128)

    def showRed(self):
        self.setColourRGB(128, 0, 0)

    def showYellow(self):
        self.setColourRGB(128, 128, 0)
