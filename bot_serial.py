import serial


class SerialWrapper(object):
    """ Simple wrapper around pyserial to easily send beerbot commands to the bot """

    def __init__(self, dev, speed=9600, timeout=1):
        self.ser = serial.Serial(dev, speed, timeout=timeout)

    def send_command(self, command, wait_for_reply=True, wait_for_empty_buffer=False):
        """ Send serial command to arduino
            Set wait_for_reply to wait and return reply
            wait_for_empty_buffer to continue reading until the buffer is empty
        """
        retval = []
        self.ser.write(command+"\n")
        if wait_for_reply:
            retval.append(self.ser.readline().strip())

        if wait_for_empty_buffer:
            while self.ser.inWaiting():
                retval.append(self.ser.readline().strip())

        return retval
