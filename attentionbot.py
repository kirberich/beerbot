import time

from api import Api
from servo import Servo

servo = Servo(port=1, min_pulse=750, max_pulse=2250)

def wave(min=0.0, max=1.0):
    servo.set(min)
    time.sleep(1)
    servo.set(max)
    time.sleep(1)
    servo.set(0.5)

api = Api()
api.demonize()

while True:
    for event, kwargs in api.events:
        if event == "wave":
            wave(**kwargs)
        if event == "set":
            servo.set(kwargs["position"])
    api.events = []
    time.sleep(0.01)