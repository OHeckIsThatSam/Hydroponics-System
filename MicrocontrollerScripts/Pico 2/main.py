from TemperatureSensor import TemperatureSensor
from time import sleep

sensor = TemperatureSensor()

while True:
    print(sensor.get_temperature())
    sleep(1)
