import sys
import time
from machine import Pin, I2C


class StopMotorInterrupt(Exception):
    """ Stop the motor """
    pass


class A4988Nema(object):
    """ Class to control a Nema bi-polar stepper motor with a A4988 also tested with DRV8825"""

    def __init__(self, direction_pin, step_pin, enablePinPin, end_switch_pin):
        self.dirPin = direction_pin
        self.stepPin = step_pin
        self.enablePin = enablePinPin
        self.end_switch_pin = end_switch_pin

        self.current_position = 0

        self.stop_motor = False

        self.resolution = {'Full': (0, 0, 0),
                           'Half': (1, 0, 0),
                           '1/4': (0, 1, 0),
                           '1/8': (1, 1, 0),
                           '1/16': (0, 0, 1),
                           '1/32': (1, 0, 1)}

    def move_to_end_switch(self):
        """ Moves the motor until the end switch is triggered """
        self.enablePin.value(0)
        while self.end_switch_pin.value() == 0:
            self.motor_go(clockwise=False, steps=5, stepdelay=.005, verbose=False, initdelay=.00)
            # TODO: Add a timeout here
        self.current_position = 0
        self.enablePin.value(1)

    def move_to_position(self, position):
        """ Moves the motor to the specified position """
        if position > 7 or position < 0:
            raise ValueError("Position must be between 0 and 7")
        if position == self.current_position:
            return

        self.enablePin.value(0)
        if position > self.current_position:
            for i in range(self.current_position, position):
                self.motor_go(clockwise=True, steps=200, stepdelay=.005, verbose=False, initdelay=.00)
            #steps = (position - self.current_position) * 200
            #self.motor_go(clockwise=True, steps=steps, stepdelay=.005, verbose=False, initdelay=.00)
        else:
            for i in range(position, self.current_position):
                self.motor_go(clockwise=False, steps=200, stepdelay=.005, verbose=False, initdelay=.00)
            #steps = (self.current_position - position) * 200
            #self.motor_go(clockwise=False, steps=steps, stepdelay=.005, verbose=False, initdelay=.00)

        self.current_position = position
        self.enablePin.value(1)

    def motor_stop(self):
        """ Stop the motor """
        self.stop_motor = True

    def motor_go(self, clockwise=False, steps=20, stepdelay=.005, verbose=False, initdelay=.05):
        """ motor_go,  moves stepper motor based on 6 inputs
         (1) clockwise, type=bool default=False
         help="Turn stepper counterclockwise"
         (2) steps, type=int, default=200, help=Number of steps sequence's
         to execute. Default is one revolution , 200 in Full mode.
         (3) stepdelay, type=float, default=0.05, help=Time to wait
         (in seconds) between steps.
         (4) verbose, type=bool  type=bool default=False
         help="Write pin actions",
         (5) initdelay, type=float, default=1mS, help= Intial delay after
         GPIO pins initialized but before motor is moved.
        """
        self.stop_motor = False
        self.dirPin.value(clockwise)

        try:
            time.sleep(initdelay)

            for i in range(steps):
                if self.stop_motor:
                    raise StopMotorInterrupt
                else:
                    self.stepPin.on()
                    time.sleep(stepdelay)
                    self.stepPin.off()
                    time.sleep(stepdelay)
                    if verbose:
                        print("Steps count {}".format(i + 1), end="\r", flush=True)

        except KeyboardInterrupt:
            print("User Keyboard Interrupt : RpiMotorLib:")
        except StopMotorInterrupt:
            print("Stop Motor Interrupt : RpiMotorLib: ")
        except Exception as motor_error:
            print(sys.exc_info()[0])
            print(motor_error)
            print("RpiMotorLib  : Unexpected error:")
        else:
            # You can use the else keyword to define a block of code to be executed if no errors were raised
            # print report status
            if verbose:
                print("\nRpiMotorLib, Motor Run finished, Details:.\n")
                print("Clockwise = {}".format(clockwise))
                print("Number of steps = {}".format(steps))
                print("Step Delay = {}".format(stepdelay))
                print("Intial delay = {}".format(initdelay))

        finally:
            # cleanup
            self.stepPin.off()
            self.dirPin.off()
