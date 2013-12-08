import cwiid

BUTTONS = {
    'up': 2048,
    'down': 1024,
    'left': 256,
    'right': 512,
    'a': 8,
    'b': 4,
    'home': 128,
    'minus': 16,
    'plus': 4096,
    '1': 2,
    '2': 1
}

class Remote(object):
    def __init__(self):
        self.wm = None
        self.accel_calibration = (0, 0, 0)
        self.rumbling = False

        tries = 0
        while not self.wm:
            try:
                self.wm = cwiid.Wiimote()
                self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_NUNCHUK
                self.wm.led = 1
            except RuntimeError:
                if tries > 5:
                    return
            finally:
                tries += 1

    def pressed(self, button=None, buttons=None):
        button_index = 0
        if button:
            button_index = BUTTONS[button.lower()]
        if buttons:
            for _button in buttons:
                button_index = button_index | BUTTONS[_button_name.lower()]

        return self.wm.state['buttons'] & button_index

    def accel(self):
        return [x-y for x,y in zip(self.wm.state['acc'], self.accel_calibration)]

    def calibrate(self):
        _avg = (0, 0, 0)

        for x in range(0, 20):
            _avg = [x+y for x,y in zip(_avg, self.wm.state['acc'])]
        self.accel_calibration = (_avg[0]/20.0, _avg[1]/20.0, _avg[2]/20.0)
        print "calibrated."
        print self.accel_calibration

    def rumble(self, state):
        if state != self.rumbling:
            self.wm.rumble = state
        self.rumbling = state

    def toggle_rumble(self):
        self.wm.rumble = not self.wm.rumble
