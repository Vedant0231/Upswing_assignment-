import paho.mqtt.publish as publish
import json

def send_mqtt_message(topic, message, broker_host="localhost", broker_port=1883):
    """
    this function is to send message to mqtt by the help of broker host
    """

    try:
        publish.single(topic, json.dumps(message), hostname=broker_host, port=broker_port)
    except Exception as e:
        raise Exception(f"error while publish message to mqtt: {str(e)}")


iot_message = input("iot_message: " )

if iot_message:
    # For now i am just taking simple text as a input but we can take complex json, just need to modified this little bit
    send_mqtt_message("test/topic", {"message": iot_message})
else:
    print ("message cannot be empty")