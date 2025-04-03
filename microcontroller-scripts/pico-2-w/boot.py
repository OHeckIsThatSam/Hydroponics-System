import network, config, sys, machine, time, logging

# Set logging defaults
logging.basicConfig(
        filename="errors.log",
        filemode="w",
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG
    )

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
