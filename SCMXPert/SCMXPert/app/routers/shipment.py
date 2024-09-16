#Importing the Required Packages
from config.config import Environment
from fastapi import APIRouter,Request,Form,HTTPException,Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers.login import active_user_from_token,login
TEMPLATES = Jinja2Templates(directory="templates")

app = APIRouter()
from pydantic import BaseModel

class shipment(BaseModel):
    Invoice_Number : str
    PO_Number : int
    Container_Number : int
    Delivery_Number : int
    Expected_Delivery_Date : str
    NDC_Number : int
    Route_Details : str
    Batch_ID : int
    Goods_Type : str
    Serial_number : int
    Select_Device : str
    Shipment_Description : str


#----------------------------------
#GET Method for Shipment
#-----------------------------------

@app.get("/shipment",response_class = HTMLResponse) 
def shipment_get(request:Request, user: login = Depends(active_user_from_token)):
    try: 
        context = { "user": user, "request": request } 
        return TEMPLATES.TemplateResponse("shipment.html", context) 
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))

#----------------------------------
#POST Method for Shipment
#-----------------------------------

@app.post("/shipment",response_class = HTMLResponse)
def shipment_post(request:Request, invoice:str=Form(...),ponum:int=Form(...),containernumber:int=Form(...),deliverynumber:int=Form(...),deliverydate:str=Form(...),ndcnumber:int=Form(...),route:str=Form(...),batch:int=Form(...),goods:str=Form(...),serialnumber:int=Form(...),device:str=Form(...),description:str=Form(...)):
    shipment_data = shipment(Invoice_Number=invoice,PO_Number=ponum,Container_Number=containernumber,Delivery_Number=deliverynumber,Expected_Delivery_Date=deliverydate,NDC_Number=ndcnumber,Route_Details=route,Batch_ID=batch,Goods_Type=goods,Serial_number=serialnumber,Select_Device=device,Shipment_Description=description)
    invoice = Environment.shipments.find_one({"Invoice_Number":invoice})
    if not invoice:
        collection = Environment.shipments.insert_one(shipment_data.dict())
        return TEMPLATES.TemplateResponse("shipment.html", {"request":request, "ShipmentCreated":"Shipment Created Successfully"})
    else:
        return TEMPLATES.TemplateResponse("shipment.html", {"request":request, "Invoice":"Invoice Number Existed"})
