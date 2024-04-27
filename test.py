import json
import paho.mqtt.client as mqtt
import pymongo
import os
from dotenv import load_dotenv
load_dotenv(os.getenv("ENV_FILE", ".env"))


# MQTT Settings
mqtt_broker_host = "localhost"
mqtt_broker_port = 1883
mqtt_topic = "test/topic"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print("test",msg.topic+" "+str(msg.payload))
    print(msg.payload)
    # Connect to MongoDB (provide username and password if authentication is enabled)
    client = pymongo.MongoClient(f"mongodb://{os.environ["MONGO_INITDB_ROOT_USERNAME"]}:{os.environ["MONGO_INITDB_ROOT_PASSWORD"]}@localhost:27017/")
    # Choose/Create a database
    db = client["mydatabase"]
    # Choose/Create a collection (table)
    user_collection = db["users"]
    payload_str = msg.payload.decode("utf-8").replace("'", '"')
    message_data = {
        "topic": msg.topic,
        "payload": json.loads(payload_str)
    }
    user_collection.insert_one(message_data)



client = mqtt.Client(protocol=mqtt.MQTTv311)  # Specify the MQTT protocol version
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_host, mqtt_broker_port, 60)

client.loop_forever()
