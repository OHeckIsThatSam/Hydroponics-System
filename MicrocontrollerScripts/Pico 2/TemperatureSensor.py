from machine import ADC

class TemperatureSensor:
    def __init__(self):
        self.accuracy = 2
        self.sensor = ADC(4)
    
    
    def set_accuracy(decimal_places):
        """"""
        self.accuracy = decimal_places
    
    
    def get_temperature(self):
        """"""
        raw_value = self.sensor.read_u16()
        voltage = raw_value * (3.3 / 65535.0)
            
        return round(27 - (voltage - 0.706) / 0.001721, self.accuracy)
