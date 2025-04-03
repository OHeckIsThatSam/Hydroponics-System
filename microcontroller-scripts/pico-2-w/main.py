import config, logging, machine, time
from sensor_factory import SensorFactory
from sensor import Sensor
from umqtt.simple import MQTTClient


logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Connecting to MQTT broker.")
        mqtt = connect_mqtt()
    except OSError as e:
        logger.critical("Unable to connect to MQTT broker.")
        logger.exception("", exc_info=e)
        restart()
    except (ValueError, TypeError, AttributeError) as e:
        logger.critical("Malformed config in MQTT section, unable to connect.")
        logger.exception("", exc_info=e)
        logger.critical("Stopping application...")
        return 0
    
    logger.info("Initialising sensors.")
    sensors = init_sensors()
    if len(sensors) == 0:
        logger.warning("No sensors were successfully initialised.")
    
    logger.info("Subscribing to topics.")
    # Subscribe to any topics here that trigger message callback
    mqtt.set_callback(handle_message)
    mqtt.subscribe(config.COMMAND_TOPIC)
    
    while True:
        mqtt.check_msg()
        
        for (topic, sensor) in sensors:
            message = str(sensor.read()).encode()
            mqtt.publish(topic, message)
        
        time.sleep(config.PUBLISH_INTERVAL)


def init_sensors() -> list[(str, Sensor)]:
    """
    Initialises sensor objects from supplied values in config.

    Returns
    -------
    sensors: list[(str, Sensor)]
        A list of sensors and their publishing topic.
    """
    sensors = []

    for key in config.SENSORS:
        try:
            topic = f"{config.PUBLISH_TOPIC}/{key}"
            sensor = SensorFactory.create_sensor(key, config.DECIMAL_PLACES, config.SENSORS[key]["pin"])
            sensors.append((topic, sensor))
        except (ValueError, TypeError, AttributeError) as e:
            # Send mqtt message
            logger.exception("Invalid config in sensor section, unable to initialise sensor.", exc_info=e)

    return sensors
        

def connect_mqtt() -> MQTTClient:
    """
    Creates an MQTTClient and connects to the broker, if possible.
    
    Returns
    -------
    client: MQTTClient
        The connected client object.
    """
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


def restart():
    logger.warning("Restarting machine...")
    logging.shutdown()
    # Wait for REPL interrupt
    for i in range(3):
        time.sleep(1)
    machine.reset()
    

if __name__ == "__main__":
    try:
        main()
        logger.info("Main exited.")
    except Exception as e:
        logger.critical("Unexpected error thrown.")
        logger.exception("", exc_info=e)
        restart()
    