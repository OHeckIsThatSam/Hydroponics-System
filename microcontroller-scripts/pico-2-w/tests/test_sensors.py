import unittest
from unittest.mock import Mock, patch

# Add path to sensors module
import sys, os
sys.path.append(os.path.abspath('../'))
from sensor import Sensor

# Mock implementations for required MicroPython-specific modules
class MockMachine:
    class Pin:
        def __init__(self, pin):
            self.pin = pin
            
            
    class ADC:
        def __init__(self, pin):
            self.pin = pin
        
        def read_u16(self):
            # Default mock implementation
            return 31191

# Overwriting the module before they are used in the imports
sys.modules['machine'] = MockMachine()
from temperature_sensor import TemperatureSensor
from light_sensor import LightSensor


class SensorsTestCase(unittest.TestCase):
    

    def setUp(self):     
        self.sensor = Sensor(1)
        self.temp_sensor = TemperatureSensor(3, 4)
        self.light_sensor = LightSensor(3, 26)
    
    
    ####################################################
    # Sensor base class testing
    ####################################################
    def test_decimal_min(self):
        with self.assertRaises(ValueError):
            sensor = Sensor(-1)
        
        self.assertIsInstance(Sensor(0), Sensor)
            
    
    def test_decimal_type(self):
        with self.assertRaises(ValueError):
            sensor = Sensor('1')
        
        
    def test_set_accuracy(self):
        self.sensor.set_accuracy(3)
        self.assertEqual(self.sensor.accuracy, 3)
    
    
    def test_set_accuracy_min(self):
        self.sensor.set_accuracy(-1)
        self.assertNotEqual(self.sensor.accuracy, -1)
        
        self.sensor.set_accuracy(0)
        self.assertEqual(self.sensor.accuracy, 0)
    
    
    def test_set_accuracy_type(self):
        self.sensor.set_accuracy('33')
        self.assertNotEqual(self.sensor.accuracy, '33')
       
    
    ####################################################
    # TemperatureSensor class testing
    ####################################################
    def test_temp_pin_range(self):
        with self.assertRaises(ValueError):
            temp_sensor = TemperatureSensor(0, 1)
        with self.assertRaises(ValueError):
            temp_sensor = TemperatureSensor(0, 29)
            
        self.assertIsInstance(TemperatureSensor(0, 2), TemperatureSensor)
        self.assertIsInstance(TemperatureSensor(0, 16), TemperatureSensor)
        self.assertIsInstance(TemperatureSensor(0, 28), TemperatureSensor)
        
    
    def test_temp_pin_type(self):
      with self.assertRaises(TypeError):
          temp_sensor = TemperatureSensor(0, '2')
          
    
    def test_temp_read(self):
        temp = self.temp_sensor.read()
        decimal_num = str(temp)[::-1].find('.')
        
        self.assertIsInstance(temp, float)
        self.assertEqual(decimal_num, self.temp_sensor.accuracy)
        
        
    ##################################################
    # LightSensor class testing
    ####################################################
    def test_light_pin_range(self):
        with self.assertRaises(ValueError):
            light_sensor = LightSensor(0, 1)
        with self.assertRaises(ValueError):
            light_sensor = LightSensor(0, 29)
            
        self.assertIsInstance(LightSensor(0, 2), LightSensor)
        self.assertIsInstance(LightSensor(0, 16), LightSensor)
        self.assertIsInstance(LightSensor(0, 28), LightSensor)
            
    
    def test_light_pin_type(self):
        with self.assertRaises(TypeError):
            light_sensor = LightSensor(0, '2')
            
    
    def test_light_read(self):
        light_level = self.light_sensor.read()
        decimal_num = str(light_level)[::-1].find('.')
        
        self.assertIsInstance(light_level, float)
        self.assertEqual(decimal_num, self.temp_sensor.accuracy)
        