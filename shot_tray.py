from machine import Pin


class ShotTray:
    def __init__(self, tray_1: Pin, tray_2: Pin, tray_3: Pin, tray_4: Pin, tray_5: Pin, tray_6: Pin, tray_7: Pin, tray_8: Pin):
        self.tray_1 = tray_1
        self.tray_2 = tray_2
        self.tray_3 = tray_3
        self.tray_4 = tray_4
        self.tray_5 = tray_5
        self.tray_6 = tray_6
        self.tray_7 = tray_7
        self.tray_8 = tray_8

        self.trays = [tray_1, tray_2, tray_3, tray_4, tray_5, tray_6, tray_7, tray_8]
