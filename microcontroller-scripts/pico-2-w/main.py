import config, time, machine
from sensors.light_sensor import LightSensor
from sensors.temperature_sensor import TemperatureSensor
from umqtt.simple import MQTTClient
from time import sleep
    

def main():
    mqtt = connect_mqtt()
    
    # Subscribe to any topics here that trigger message callback
    mqtt.set_callback(handle_message)
    mqtt.subscribe(config.COMMAND_TOPIC)
    
    while True:
        mqtt.check_msg()
        
        for (topic, sensor) in sensors:
            message = str(sensor.read()).encode()
            mqtt.publish(topic, message)
        
        sleep(config.PUBLISH_INTERVAL)


def init_sensors():
    light_topic = f"{config.PUBLISH_TOPIC}/light_level"
    light_sensor = LightSensor(config.DEFAULT_DECIMAL_PLACES, config.LIGHT_LEVEL_PIN)
    
    temp_topic = f"{config.PUBLISH_TOPIC}/temperature"
    temp_sensor = TemperatureSensor(config.DEFAULT_DECIMAL_PLACES, config.TEMPERATURE_PIN)
    
    return [(light_topic, light_sensor), (temp_topic, temp_sensor)]
        

def connect_mqtt():
    client = MQTTClient(
        client_id = config.CLIENT_ID,
        server = config.MQTT_BROKER,
        port = config.MQTT_PORT,
        keepalive = config.KEEP_ALIVE,
        ssl = config.IS_SSL)
            
    client.connect()
    
    return client


def handle_message(topic, message):
    print(message)
    

sensors = init_sensors()
if __name__ == "__main__":
    while True:
        try:
            main()
        except OSError as e:
            import sys
            sys.print_exception(e)
            machine.reset()
            
            