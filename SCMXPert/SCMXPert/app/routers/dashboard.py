#Importing Required Libraries
from fastapi import APIRouter,Request,HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers.login import active_user_from_token,login
TEMPLATES = Jinja2Templates(directory="templates")
app = APIRouter() 


#----------------------------------
#GET Method for dashboard
#-----------------------------------
@app.get("/dashboard",response_class = HTMLResponse) 
def dashboard_get(request:Request, user: login = Depends(active_user_from_token)): 
    try: 
        context = { "user": user, "request": request } 
        return TEMPLATES.TemplateResponse("dashboard.html", context) 
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))