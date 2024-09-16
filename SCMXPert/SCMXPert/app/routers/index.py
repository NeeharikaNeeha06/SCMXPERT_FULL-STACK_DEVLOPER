#Importing the required Packages
from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
app = APIRouter()
TEMPLATES = Jinja2Templates(directory="templates")

#Get Method For Rendering the Home(Index) Page
@app.get("/",response_class = HTMLResponse)
def home(request:Request):
   return TEMPLATES.TemplateResponse("index.html",{"request":request})