#Importing the Required Packages
from config.config import Environment
from fastapi import APIRouter,Request,HTTPException
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
app = APIRouter()
TEMPLATES = Jinja2Templates(directory="templates")


#----------------------------------------------
#Get Method For Logout
#----------------------------------------------
@app.get("/logout", response_class=HTMLResponse)
def logout_get():
    try:
        response = RedirectResponse(url="/login")
        #Deleting the token from the cookie
        response.delete_cookie(Environment.cookie_name)
        return response
    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Cookie name not found.") from exc
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception