from machine import Pin
import utime


class WaterPump:
    ml_per_second: float = 4.0
    default_shot_size: int = 40  # ml

    def __init__(self, signal_pin: Pin):
        self.signal_pin = signal_pin

        shot_size_file = open("shotSize.txt", "r")
        self.default_shot_size = int(shot_size_file.read())
        shot_size_file.close()

    def on(self):
        self.signal_pin.value(1)

    def off(self):
        self.signal_pin.value(0)

    def toggle(self):
        if self.signal_pin.value():
            self.off()
        else:
            self.on()

    def fill_shot(self):
        self.turn_on_for_ml(self.default_shot_size)

    def change_shot_size(self, shot_size: int):
        if shot_size < 0 or shot_size > 100:
            return
        self.default_shot_size = shot_size
        shot_size_file = open("shotSize.txt", "w")
        shot_size_file.write(str(shot_size))
        shot_size_file.close()

    def turn_on_for_duration(self, duration: float):
        self.on()
        utime.sleep(duration)
        self.off()

    def turn_on_for_ml(self, milliliters: int):
        self.on()
        utime.sleep(milliliters / self.ml_per_second)
        self.off()
