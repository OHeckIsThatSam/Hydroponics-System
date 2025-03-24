import network, config, sys, machine
from time import sleep

led = machine.Pin('LED', machine.Pin.OUT)


def connect_to_wifi():
    # Create wireless lan object
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Try to connect to wifi
    wlan.connect(config.SSID, config.PASSWORD)
    # Wait for Pico to connect
    while wlan.isconnected() == False:
        led.on()
        sleep(0.25)
        led.off()


connect_to_wifi()
