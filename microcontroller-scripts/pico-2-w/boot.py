import network, config, sys, time, logging
from machine import Pin, PWM


# Set logging defaults
logging.basicConfig(
        filename=config.LOG_FILENAME,
        filemode=config.LOG_FILEMODE,
        format=config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT,
        level=logging.DEBUG
    )

# Boot.py called from/before main so magic __name__ gives __main__ so logger
# specifically named as boot. __name__ should be used everywhere else.
logger = logging.getLogger("boot")
logger.info("Booting application...")


led = Pin('LED', Pin.OUT)


def initialise_actuators():
    try:
        for key in config.ACTUATORS:
            if key == "pump":
                pump = PWM(Pin(config.ACTUATORS[key]["pin"]))
                pump.freq(config.PWM_FREQ)
                pump.duty_u16(65536 * (config.ACTUATORS[key]["power"] / 100))
    except Exception as e:
        logger.exception("Exception thrown while initialising actuators...", exc_info=e)


def connect_to_wifi():
    # Create wireless lan object
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Try to connect to wifi
    wlan.connect(config.SSID, config.PASSWORD)
    # Wait for Pico to connect
    logger.debug("Initiated connection.")
    while wlan.isconnected() == False:
        led.on()
        time.sleep(0.25)
        led.off()
        logger.debug("Waiting for response...")
    
    logger.info("Wi-Fi connected.")
    logger.debug(f"IP, subnet: {wlan.ipconfig("addr4")}")
    

logger.info("Initialising actuators...")
initialise_actuators()
logger.info("Connecting to Wi-Fi...")
connect_to_wifi()
