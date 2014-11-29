import time
import argparse

from api import Api
from bot_serial import SerialWrapper
from motors import Motor


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Control the potato beer delivery system via an arduino.')
    parser.add_argument('dev', type=str, help='serial device the arduino is connected to')
    args = parser.parse_args()

    serial = SerialWrapper(dev=args.dev, speed=57600)
    speed_motor = Motor(serial, arduino_command="S")
    direction_motor = Motor(serial, arduino_command="D")
    api = Api()
    api.demonize()

    while True:
        # api events
        with api.lock:
            for event, kwargs in api.events:
                print kwargs
                if event == "set":
                    direction_motor.set(kwargs["position"])
                if event == "set_speed":
                    speed_motor.set(kwargs["position"])
            api.events = []
