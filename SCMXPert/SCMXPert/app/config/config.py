#Importing the Required Packages
import os
import pymongo
from dotenv import load_dotenv
load_dotenv()

class settings:
    client = pymongo.MongoClient(os.getenv("mongouri"))
    db = client["SCM_Training"]
    device_data = db["DeviceData"]
    shipments = db["Shipments"]
    signup = db["Signup"]
    secret_key:str = "secret-key"
    algorithm = "HS256"
    access_token_expire_minutes = 10 # in mins
    cookie_name = "jwt_token"
    # host = os.getenv("HOST")
    # port = os.getenv("PORT")
Environment = settings()
