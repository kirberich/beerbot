from subprocess import call

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