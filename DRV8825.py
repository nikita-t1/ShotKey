import sys
import time
from machine import Pin, I2C

class StopMotorInterrupt(Exception):
    """ Stop the motor """
    pass

class A4988Nema(object):
    """ Class to control a Nema bi-polar stepper motor with a A4988 also tested with DRV8825"""
    def __init__(self, direction_pin, step_pin):
        """ class init method 3 inputs
        (1) direction type=int , help=GPIO pin connected to DIR pin of IC
        (2) step_pin type=int , help=GPIO pin connected to STEP of IC
        (3) mode_pins type=tuple of 3 ints, help=GPIO pins connected to
        Microstep Resolution pins MS1-MS3 of IC, can be set to (-1,-1,-1) to turn off
        GPIO resolution.
        (4) motor_type type=string, help=Type of motor two options: A4988 or DRV8825
        """
        
        self.dirPin = direction_pin
        self.stepPin = step_pin
        
        #self.direction_pin = direction_pin
        #self.step_pin = step_pin

        self.stop_motor = False
        
        self.resolution = {'Full': (0, 0, 0),
                          'Half': (1, 0, 0),
                          '1/4': (0, 1, 0),
                          '1/8': (1, 1, 0),
                          '1/16': (0, 0, 1),
                          '1/32': (1, 0, 1)}

    def motor_stop(self):
        """ Stop the motor """
        self.stop_motor = True

    def motor_go(self, clockwise=False, steps=20, stepdelay=.005, verbose=False, initdelay=.05):
        """ motor_go,  moves stepper motor based on 6 inputs
         (1) clockwise, type=bool default=False
         help="Turn stepper counterclockwise"
         (2) steptype, type=string , default=Full help= type of drive to
         step motor 5 options
            (Full, Half, 1/4, 1/8, 1/16) 1/32 for DRV8825 only 1/64 1/128 for LV8729 only
         (3) steps, type=int, default=200, help=Number of steps sequence's
         to execute. Default is one revolution , 200 in Full mode.
         (4) stepdelay, type=float, default=0.05, help=Time to wait
         (in seconds) between steps.
         (5) verbose, type=bool  type=bool default=False
         help="Write pin actions",
         (6) initdelay, type=float, default=1mS, help= Intial delay after
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
                        print("Steps count {}".format(i+1), end="\r", flush=True)

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