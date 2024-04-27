import json
import paho.mqtt.client as mqtt
import pymongo
import os
from dotenv import load_dotenv
load_dotenv(os.getenv("ENV_FILE", ".env"))


# MQTT Settings
mqtt_broker_host = os.environ["MQTT_BROKER_HOST"]
mqtt_broker_port = os.environ["MQTT_BROKER_PORT"]
mqtt_topic = os.environ["MQTT_TOPIC"]

def on_connect(client, userdata, flags, rc):
    """
    Function to create connection
    """
    try:
        print("Connected with result code "+str(rc))
        client.subscribe(mqtt_topic)
    except Exception as e:
        return f"error while connecting the mqtt: {str(e)}"
    

def on_message(client, userdata, msg):
    """
    Function to process message and store in database
    """
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(f"mongodb://{os.environ["MONGO_INITDB_ROOT_USERNAME"]}:{os.environ["MONGO_INITDB_ROOT_PASSWORD"]}@localhost:27017/")
        # Choose or Create a database
        db = client["mydatabase"]
        # Choose or Create a collection
        user_collection = db["users"]
        payload_str = msg.payload.decode("utf-8").replace("'", '"')
        message_data = {
            "topic": msg.topic,
            "payload": json.loads(payload_str)
        }
        # Insert data in database
        user_collection.insert_one(message_data)
    except Exception as e:
        return f"error while processing the message: {str(e)}"



client = mqtt.Client(protocol=mqtt.MQTTv311)  # Specify the MQTT protocol version
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_host, mqtt_broker_port, 60)

client.loop_forever()
