import time
import ioexpander as io
from evdev import UInput, AbsInfo, ecodes as e

class KeyFromPin:
    
    def __init__(self, pin, key):
        self.pin = pin
        self.key = key

        # input
        ui = UInput()

        # ioexpander setup
        self.ioe = io.IOE(i2c_addr=0x18)
        self.ioe.set_mode(self.pin, io.IN_PU)

        self.last_value = io.HIGH

    def check(self):

        newValue = self.ioe.input(self.pin)

        # no change
        if self.last_value == newValue:
            pass

        # PRESS: high to low
        elif self.last_value == io.HIGH and newValue == io.LOW:
            self.press()

        # RELEASE: low to high
        elif self.last_value == io.LOW and newValue == io.HIGH:
            self.release()

    def press(self):
        self.ui.write(e.EV_KEY, self.key, 1)
        self.ui.syn()
        

    def release(self):
        self.ui.write(e.EV_KEY, self.key, 0)
        self.ui.syn()


class IoeKeyboardController:
    def __init__(self):
        self.setup()
        self.main()


    def setup(self):
        self.injector = UInput(name = 'IoePico8Controller Keyboard')

        # define input pins & keys here
        buttons = [
            KeyFromPin(1, e.KEY_A),
            KeyFromPin(2, e.KEY_B),
            KeyFromPin(3, e.KEY_C)
        ]

    def main(self):
        try:
            while True:
                self.checkButtons()
                time.sleep(1.0 / 30)

        except KeyboardInterrupt:
            pass


    def checkButtons(self):
        for button in self.buttons:
            button.check()


if __name__ == "__main__":
		IoeKeyboardController()


# install ioexpander: 
# IOhttps://github.com/pimoroni/ioe-python

# install evdev: 
# pip install evdev

# enable service
# https://www.thedigitalpictureframe.com/ultimate-guide-systemd-autostart-scripts-raspberry-pi/
# sudo chmod 644 /etc/systemd/system/name-of-your-service.service
# sudo systemctl daemon-reload
# sudo systemctl enable name-of-your-service.service
# then reboot