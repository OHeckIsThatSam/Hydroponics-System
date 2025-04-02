from sensor import Sensor
from light_sensor import LightSensor
from temperature_sensor import TemperatureSensor


class SensorFactory:
    def create_sensor(key, decimal_places, pin) -> Sensor:
        match key:
            case "temperature":
                return TemperatureSensor(decimal_places, pin)
            case "light_level":
                return LightSensor(decimal_places, pin)
            case _:
                raise ValueError(f"Unknown sensor type {key}.")
