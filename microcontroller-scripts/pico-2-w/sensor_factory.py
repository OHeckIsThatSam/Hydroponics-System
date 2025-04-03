from sensor import Sensor
from light_sensor import LightSensor
from temperature_sensor import TemperatureSensor


class SensorFactory:
    def create_sensor(key, decimal_places, pin) -> Sensor:
        if key == "temperature":
            return TemperatureSensor(decimal_places, pin)
        elif key == "light_level":
            return LightSensor(decimal_places, pin)
        else:
            raise ValueError(f"Unknown sensor type of {key}.")
