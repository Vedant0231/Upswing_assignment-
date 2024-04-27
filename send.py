import paho.mqtt.publish as publish
import json

def send_mqtt_message(topic, message, broker_host="localhost", broker_port=1883):
    """
    this function is to send message to mqtt by the help of broker host
    """
    publish.single(topic, json.dumps(message), hostname=broker_host, port=broker_port)



iot_message = input("iot_message: " )
send_mqtt_message("test/topic", {"message": iot_message})
