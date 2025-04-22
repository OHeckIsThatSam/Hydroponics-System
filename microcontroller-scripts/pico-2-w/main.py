import config, logging, machine, time
from sensor_controller import SensorController
from umqtt.simple import MQTTClient


logger = logging.getLogger(__name__)

_callbacks = {}

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
    sensor_controller = SensorController()
    sensor_controller.init_sensors(config.PUBLISH_TOPIC, config.DECIMAL_PLACES, config.SENSORS)
    if sensor_controller.sensor_count() == 0:
        logger.warning("No sensors were successfully initialised.")
    
    # Set the callbacks for commands
    _callbacks["accuracy"] = sensor_controller.set_accuracy
    
    logger.info("Subscribing to topics.")
    # Subscribe to any topics here that trigger message callback
    mqtt.set_callback(subscription_callback)
    mqtt.subscribe(config.COMMAND_TOPIC)
    
    while True:
        mqtt.check_msg()
        
        for (topic, reading) in sensor_controller.read_sensors():
            mqtt.publish(topic, str(reading).encode())
        
        time.sleep(config.PUBLISH_INTERVAL)
      

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


def subscription_callback(topic, message):
    print(f"Callback triggered for topic {topic}")
    print(f"Message: {message}")
    # Update/Change config

    # Set value of running sensors
    if topic.endswith("accuracy"):
        print("Updating accuracy")
        try:
            _callbacks["accuracy"](int(message))
        except ValueError as e:
            logger.warning(f"Invalid command message {message}; Ignoring command.")

    # Set value of running actuator


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
    