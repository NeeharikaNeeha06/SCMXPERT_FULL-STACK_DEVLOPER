# from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, HTTPException, Response
from routers import index,login,signup,dashboard,shipment,devicedata,password,logout
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(HTTPException)
async def redirectting_to_login(request: Request, exception: HTTPException) -> Response:
    
     # pylint: disable=unused-argument
    if exception.status_code == 401:
        # Redirect to login page
        return HTMLResponse("<script>window.location.href = '/login';</script>")
    
    # Re-raise the exception for other status codes
    raise exception
    


app.include_router(index.app)
app.include_router(login.app)
app.include_router(signup.app)
app.include_router(dashboard.app)
app.include_router(shipment.app)
app.include_router(devicedata.app)
app.include_router(password.app)
app.include_router(logout.app)

