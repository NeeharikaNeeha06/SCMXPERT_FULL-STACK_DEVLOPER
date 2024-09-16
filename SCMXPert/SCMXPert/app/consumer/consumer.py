#Importing required libraries
import os
import json
import sys
import pymongo
from kafka import KafkaConsumer
from dotenv import load_dotenv
load_dotenv()

#Connecting to the MongoDB Database and Collection.
CLIENT = pymongo.MongoClient(os.getenv("mongodbUri"))
DB = CLIENT['SCM_Training']
COLLECTION = DB["DeviceData"]

TOPIC_NAME = os.getenv("topic_name")
bootstrap_servers = os.getenv("bootstrap_servers")
print("Consumer is Listing...")

#Getting the data from the specified topic_name in kafka-server 
try:
    CONSUMER = KafkaConsumer(TOPIC_NAME,bootstrap_servers=bootstrap_servers,auto_offset_reset='latest' )
    for DATA in CONSUMER:
        try:
            DATA = json.loads(DATA.value)
            #Inserting the data received from the topic_name into MongoDB Collection.
            mongo_data = COLLECTION.insert_one(DATA)

            
        except json.decoder.JSONDecodeError:
            continue
except KeyboardInterrupt:
    sys.exit()
