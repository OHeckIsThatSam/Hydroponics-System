import seeed_dht
import config, logging, time
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)
dht_sensor = seeed_dht.DHT("11", 4)

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, config.client_id)
    
    client.on_message = on_message
    
    client.connect(config.host, config.port, config.keep_alive)
    
    client.subscribe(config.command_topic)
    
    client.loop_start()
    while True:
        humi, temp = dht_sensor.read()
        
        client.publish(f"{config.base_pub_topic}/temperature", temp)
        client.publish(f"{config.base_pub_topic}/humidity", humi)
        
        time.sleep(config.pub_interval)
    client.loop_stop()

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    
if __name__ == "__main__":
    main()