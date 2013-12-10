import time
import threading
from subprocess import call

import piface.pfio as pfio

pfio.init()

class Servo(object):
    def __init__(self, port, min_pulse, max_pulse, pulse_multiplier=0.1, min_position=0, max_position=1):
        self.port = port
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        self.pulse_diff = max_pulse - min_pulse
        self.pulse_multiplier = pulse_multiplier
        self.min_position = min_position
        self.max_position = max_position
        self.position = -1
            
        t = threading.Thread(target=self.write_position)
        t.daemon = True
        t.start()

    def pulse_from_position(self, position):
        position = max(position, self.min_position)
        position = min(position, self.max_position)
        pulse = self.min_pulse + float(position)*self.pulse_diff
        return int(self.pulse_multiplier * pulse)

    def write_position(self):
        while True:
            call ("echo "+str(self.port)+"="+str(self.pulse_from_position(self.position))+" > /dev/servoblaster", shell=True)
            time.sleep(0.1)

    def set(self, position):
        self.position = position

class Motor(object):
    def __init__(self, port, duty_cycle=1):
        self.port = port
        self.duty_cycle = duty_cycle
        self.duty_cycle_position = 0
        self.state = 0
        
    def set(self, state):
        if state == self.state: 
          return
        pfio.digital_write(self.port, state)
        self.state = state

    def tick(self):
        """ Continue duty cycle, turn motor on or off accordingly """
        self.duty_cycle_position += 0.1
        if self.duty_cycle_position >= 1:
            self.duty_cycle_position = 0
            
        if self.duty_cycle_position >= self.duty_cycle:
            self.set(0)
        else:
            self.set(1)

