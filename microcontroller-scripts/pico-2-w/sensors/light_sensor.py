from machine import Pin, ADC
from sensors.sensor import Sensor


class LightSensor(Sensor):
    """
    A class wrapping logic for reading from a light level sensor.
    
    Attributes
    ----------
    accuracy: int
        The number of decimal places returned in a reading.
    sensor: ADC
        The input pin of the sensor.
    conversion_factor: float
        The factor used when converting from voltage to light level.
    """
    
    
    def __init__(self, decimal_places, input_pin):
        """
        Initialises a LightSensor object.
        
        Parameters
        ----------
        decimal_places : int
            The number of decimal places.
        input_pin: int
            The pin the sensor is connected too.
        """
        if not isinstance(input_pin, int):
            raise TypeError("input_pin must be of type int")
        elif input_pin < 2 or input_pin > 28:
            raise ValueError("input_pin must be a vaild pin on the pico 2 W")
        
        super().__init__(decimal_places)
        self.sensor = ADC(Pin(input_pin))
    
    
    def read(self) -> float:
        """
        Gets the current light level.
        
        Returns
        -------
        float
            The light level, ranging from 0 -> 3.3, rounded to the set accuracy.
        """
        light_level = self.sensor.read_u16() * self.conversion_factor
        return round(light_level, self.accuracy)
