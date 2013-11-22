from subprocess import call
import time

import piface.pfio as pfio

pfio.init()

class Servo(object):
    def __init__(self, port, min_pulse, max_pulse, pulse_multiplier=0.1):
        self.port = port
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        self.pulse_diff = max_pulse - min_pulse
        self.pulse_multiplier = pulse_multiplier

    def pulse_from_position(self, position):
        pulse = self.min_pulse + float(position)*self.pulse_diff
        return int(self.pulse_multiplier * pulse)

    def set(self, position):
        call ("echo "+str(self.port)+"="+str(self.pulse_from_position(position))+" > /dev/servoblaster", shell=True)

class Motor(object):
    def __init__(self, port, duty_cycle=1, duty_cycle_period=0.05):
        self.port = port
        self.duty_cycle = duty_cycle
        self.duty_cycle_period = duty_cycle_period
        self.duty_cycle_position = 0
        self.last_tick = time.time()
        self.state = 0
        
        self.clear()

    def set(self, state):
        pfio.digital_write(self.port, state)
        self.state = state

    def tick(self):
        """ Continue duty cycle, turn motor on or off accordingly """
        now = time.time()
        tick_diff = now - self.last_tick 

        self.duty_cycle_position += tick_diff
        if self.duty_cycle_position > self.duty_cycle_period:
            self.duty_cycle_position = 0
            
        if self.duty_cycle_position > self.duty_cycle_period*self.duty_cycle:
            self.set(0)
        else:
            self.set(1)
        board.set(self.port)

        self.last_tick = now