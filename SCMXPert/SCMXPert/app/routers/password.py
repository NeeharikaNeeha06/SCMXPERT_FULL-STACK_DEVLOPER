#Importing the Required Packages
from config.config import Environment
from fastapi import APIRouter,Request,Form,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
app = APIRouter()
TEMPLATES = Jinja2Templates(directory="templates")
from pydantic import BaseModel
from passlib.context import CryptContext



PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
def password_hashing(password: str):
   """Function to change plain password to Hash"""
   return PWD_CONTEXT.hash(password)
def password_verification(password: str, hashed_password: str):
   """Function to verify hased password"""
   return PWD_CONTEXT.verify(password, hashed_password)

class forget(BaseModel):
   Email: str
   Password: str
   ConfirmPassword : str



ForgetPassPage = "forgetpass.html"

#----------------------------------------
#Get Method for forget
#----------------------------------------
@app.get("/forget",response_class = HTMLResponse)
def forget_get(request:Request):
   return TEMPLATES.TemplateResponse(ForgetPassPage,{"request":request})
   
#----------------------------------------
#Post Method for forget
#----------------------------------------
@app.post("/forget",response_class = HTMLResponse)
def forget_post(request:Request, email:str=Form(...),password:str=Form(...),cnfpassword:str=Form(...)):
   hashed_password = password_hashing(password)
   forget_data = forget(Email=email,Password=hashed_password,ConfirmPassword=hashed_password)
   user = Environment.signup.find_one({"Email":email})
   if not user:
      return TEMPLATES.TemplateResponse(ForgetPassPage,{"request":request,"NotRegisted":"User Not Registred yet!"})
   else:
      if  (password == cnfpassword):
         forget_data = Environment.signup.update_one({"Email":email},{"$set":{"Password":hashed_password,"ConfirmPassword":hashed_password}})
         return TEMPLATES.TemplateResponse(ForgetPassPage,{"request":request,"PasswordChanged":"Password Changed Successfully"})
   return TEMPLATES.TemplateResponse(ForgetPassPage,{"request":request})





  




