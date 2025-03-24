class Sensor():
    """
    A base class representing a generic sensor.
    
    Attributes
    ----------
    accuracy: int
        The number of decimal places returned in a reading.
    conversion_factor: float
        The factor used when converting from the input voltage.
    """
    
    
    def __init__(self, decimal_places):
        """
        Initialises a Sensor object.
        
        Parameters
        ----------
        decimal_places : int
            The number of decimal places.
        """
        if not isinstance(decimal_places, int) or decimal_places < 0:
            raise ValueError("decimal_places must be an int above 0.")
        
        self.accuracy = decimal_places
        self.conversion_factor = 3.3 / 65535
    
    
    def set_accuracy(decimal_places):
        """
        Sets the accuracy of the sensor readings.
        
        Parameters
        ----------
        decimal_places : int
            The number of decimal places.
        """
        if isinstance(decimal_places, int) and decimal_places >= 0: 
            self.accuracy = decimal_places
            
           
    def read(self):
        """
        Empty function as MicroPython dosen't recognise abstract classes or functions.
        Reads the value of the sensor.
        
        Returns
        -------
        float:
            The value of the reading.
        """
        pass
