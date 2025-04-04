import logging
from temperature_sensor import TemperatureSensor
from light_sensor import LightSensor

class SensorController:

    def __init__(self):
        self._sensors = []
        self._logger = logging.getLogger(__name__)


    def init_sensors(self, base_topic, decimal_places, sensor_params):
        """
        Initialises sensor objects from parameters.

        Returns
        -------
        sensors: list[(str, Sensor)]
            A list of sensors and their publishing topic.
        """
        for key in sensor_params:
            try:
                topic = f"{base_topic}/{key}"

                if key == "temperature":
                    self._sensors.append((topic, TemperatureSensor(decimal_places, sensor_params[key]["pin"])))
                elif key == "light_level":
                    self._sensors.append((topic, LightSensor(decimal_places, sensor_params[key]["pin"])))
                else:
                    raise ValueError(f"Unknown sensor type of {key}.")
                
            except (ValueError, TypeError, AttributeError) as e:
                self._logger.exception("Invalid config in sensor section, unable to initialise sensor.", exc_info=e)


    def read_sensors(self):
        readings = []

        for (topic, sensor) in self._sensors:
            readings.append((topic, sensor.read()))

        return readings
    

    def set_accuracy(self, new_accuracy):
        for sensor in self._sensors:
            sensor.set_accuracy(new_accuracy)


    def sensor_count(self):
        return len(self._sensors)
