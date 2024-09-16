#Importing the required libraries
import socket
import os
from dotenv import load_dotenv
from kafka import KafkaProducer
load_dotenv()

#Socket Connection
socket_connection = socket.socket()
print("Waiting to Listen for Consumer...")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
# socket_connection.connect((HOST, int(PORT)))
socket_connection.connect((HOST,int( PORT)))
bootstrap_servers =os.getenv("bootstrap_servers")

PRODUCER = KafkaProducer(bootstrap_servers=bootstrap_servers, retries=3)
TOPIC_NAME = os.getenv("topic_name")

while True:
    try:
        DATA = socket_connection.recv(70240)
        # print(DATA)
        #Sending the data to the specified topic_name in kafka-server.
        PRODUCER.send(TOPIC_NAME, DATA)
        

    except Exception as exception:
        print(exception)
socket_connection.close()