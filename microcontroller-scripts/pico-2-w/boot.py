import network, config, sys, machine, time, logging

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


led = machine.Pin('LED', machine.Pin.OUT)


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
    

logger.info("Connecting to Wi-Fi...")
connect_to_wifi()
