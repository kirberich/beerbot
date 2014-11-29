class Motor(object):
    def __init__(self, serial, arduino_command, speed=0):
        """ serial is the pyserial object attached to an arduino
            arduino_command is the command byte to send to the arduino along with the speed value
        """
        self.serial = serial
        self.arduino_command = arduino_command
        self.speed = speed

    def make_serial_command(self):
        arduino_speed = int(round(self.speed*255))
        return "%s%d" % (self.arduino_command, arduino_speed)

    def set(self, speed):
        speed = min(max(speed, -1.0), 1.0)
        if speed == self.speed:
          return

        self.speed = speed

        print self.serial.send_command(self.make_serial_command())
