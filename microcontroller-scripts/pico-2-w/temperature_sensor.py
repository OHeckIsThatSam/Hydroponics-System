from machine import ADC
from sensor import Sensor


class TemperatureSensor(Sensor):
    """
    A class wrapping logic for reading from a temperature sensor.
    
    Attributes
    ----------
    accuracy: int
        The number of decimal places returned in a reading.
    sensor: ADC
        The input pin of the sensor.
    conversion_factor: float
        The factor used when converting from voltage to temperature.
    """
    
    
    def __init__(self, decimal_places, input_pin=4):
        """
        Initialises a TemperatureSensor object.
        
        Parameters
        ----------
        decimal_places : int
            The number of decimal places.
        input_pin: int
            default: 4 (pin of internal temperature resistor on Pico 2 W)
            The pin the sensor is connected too.
        """
        if not isinstance(input_pin, int):
            raise TypeError("input_pin must be of type int")
        elif input_pin < 2 or input_pin > 28:
            raise ValueError("input_pin must be a vaild pin on the pico 2 W")
        
        super().__init__(decimal_places)
        self.sensor = ADC(input_pin)
    
    
    def read(self) -> float:
        """
        Gets the current temperature.
        
        Returns
        -------
        float
            The temperature, rounded to the set accuracy.
        """
        raw_value = self.sensor.read_u16()
        voltage = raw_value * self.conversion_factor
        
        # Convert voltage to celsius then round
        return round(27 - (voltage - 0.706) / 0.001721, self.accuracy)
