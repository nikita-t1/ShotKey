import utime

currentTime = utime.ticks_ms()
loopTime = currentTime
encoderA_prev: int = 0


class RotaryEncoder:

    ROTARY_NO_MOTION = 0
    ROTARY_CCW = 1
    ROTARY_CW = 2

    def __init__(self, encoderAPin, encoderBPin):
        self.encoderAPin = encoderAPin
        self.encoderBPin = encoderBPin

    def readRotaryEncoder(self) -> int:
        """
        Read the rotary encoder and return the event
        """
        global currentTime
        global loopTime
        global encoderA_prev

        event = self.ROTARY_NO_MOTION
        # get the current elapsed time
        currentTime = utime.ticks_ms()
        if currentTime >= (loopTime + 5):
            # 5ms since last check of encoder = 200Hz
            encoderA = self.encoderAPin.value()
            encoderB = self.encoderBPin.value()
            if (not encoderA) and (encoderA_prev):
                # encoder A has gone from high to low
                # CW and CCW determined
                if encoderB:
                    # B is low so counter-clockwise
                    event = self.ROTARY_CW
                else:
                    # encoder B is high so clockwise
                    event = self.ROTARY_CCW
            encoderA_prev = encoderA  # Store value of A for next time
            loopTime = currentTime
        return event
