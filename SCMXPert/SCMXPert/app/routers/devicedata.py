#Importing Required Packages
from config.config import Environment
from fastapi import APIRouter,Request,HTTPException,Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers.login import active_user_from_token,login
TEMPLATES = Jinja2Templates(directory="templates")
from dotenv import load_dotenv
load_dotenv()

app = APIRouter() 
client = Environment.client
db = client["SCM_Training"]
device_data_stream = db["DeviceData"]

#----------------------------------
#GET Method for DeviceData
#-----------------------------------
@app.get("/devicedata",response_class = HTMLResponse)
def devicedata_get(request:Request,user: login = Depends(active_user_from_token)):
   try:
        device_data = []
        stream_data = device_data_stream.find({},{"_id":0})
        for data in stream_data:
            device_data.append(data)
        content = {"request":request,"device_data":device_data,"user": user}
#Rendering devicedata webpage along with the kafka-server data
        return TEMPLATES.TemplateResponse("devicedata.html",content)
#Exceptional case
   except Exception as e:
        error_msg = f"Something went wrong while retrieving data from the database: {str(e)}"
        return HTTPException(status_code=500, detail=error_msg)