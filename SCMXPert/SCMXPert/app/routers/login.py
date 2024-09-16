#Importing the Required Packages
import datetime as dt
from config.config import Environment
from fastapi import APIRouter,Request,Form,HTTPException, status, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
# from routers.authentication import login_for_access_token
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Dict, List, Optional
from jose import JWTError, jwt
app = APIRouter()
TEMPLATES = Jinja2Templates(directory="templates")

#Password hashing and dehashing function
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
# def password_hashing(password: str):
#    #Function to change plain password to Hash
#    return PWD_CONTEXT.hash(password)
def password_verification(password: str, hashed_password: str):
   #Function to verify hased password
   return PWD_CONTEXT.verify(password, hashed_password)

#BaseModel for Login form
class login(BaseModel):
   Email: str
   Password: str


class OAuth2PasswordBearerWithCookie(OAuth2):
    
 def __init__(self,tokenUrl: str,scheme_name: Optional[str] = None,scopes: Optional[Dict[str, str]] = None,description: Optional[str] = None,auto_error: bool = True):
       if not scopes:
          scopes = {}
       flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
       super().__init__(flows=flows,scheme_name=scheme_name,description=description,auto_error=auto_error)

 async def __call__(self, request: Request) -> Optional[str]:
    authorization: str = request.cookies.get(Environment.cookie_name)
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        if self.auto_error:
            raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Not authenticated",
               headers={"WWW-Authenticate": "Bearer"},
               )
        else:
            return None
    return param

OAUTH2_SCHEME = OAuth2PasswordBearerWithCookie(tokenUrl="token")


#Generating JWT_token using user email,secret_key and HS256 algorithm.
def generating_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=Environment.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,Environment.secret_key,algorithm=Environment.algorithm)
    return encoded_jwt


#Authenticating  the user by email,password entered in login form 
def authenticating_user(email: str, password: str) -> login:
    user = fetching_user(email)
    if not user:
        return False
    if not password_verification(password, user['Password']):
        return False
    return user


#Checking the user is existed or not in signup collection using email entered in login form
def fetching_user(email: str) -> login:
    user = Environment.signup.find_one({"Email":email})
    if user:
        return user
    return None

#Getting the active user from the cookie
def active_user_from_cookie(request: Request) -> login:
    token = request.cookies.get(Environment.cookie_name)
    user = decode_token(token)
    return user


#Decoding the JWT_token using same secret_key, HS256 algorithm and getting the username(email).
def decode_token(token: str) -> login:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Session Timeout, Login Again! "
    )
    token = str(token).replace("Bearer", "").strip()
    try:
        payload = jwt.decode(token, Environment.secret_key, algorithms=[Environment.algorithm])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    
    user = fetching_user(email)
    return user


#Getting the active user from the token
def active_user_from_token(token: str = Depends(OAUTH2_SCHEME)) -> login:
    user = decode_token(token)
    return user


#-------------------------------------------
#Post method for the token
#--------------------------------------------

@app.post("token")
def login_for_access_token(response: Response,form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    # Authenticate the user with the provided credentials
    user = authenticating_user(form_data.email, form_data.password)
    if not user:
        # If the user is not authenticated, raise an HTTPException with 401 status code
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    # Create an access token for the authenticated user
    access_token = generating_token(data={"email": user["Email"]})
    # Set an HttpOnly cookie in the response. `httponly=True` prevents
    # JavaScript from reading the cookie.
    response.set_cookie(
        key=Environment.cookie_name,
        value=f"Bearer {access_token}",
        httponly=True
        # secure=True
    )
    # Return the access token and token type in a dictionary
    return {Environment.cookie_name: access_token, "token_type": "bearer"}



#Backend Validation for the login form
class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: str = ""
        self.email: Optional[str] = None
        self.password: Optional[str] = None

#Getting email and password entered by user at Login time.
    async def load_data(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.password = form.get("password")

#Validating email contains @ or not and password should have atleast 8 characters
    async def is_valid(self):
        if not self.email or not (self.email.__contains__("@")):
            self.errors="Email is required"
        if not self.password or not len(self.password) >= 8:
            self.errors="A valid password is required"
        if not self.errors:
            return True
        return False

#--------------------------------------------
#Login Get Method
#--------------------------------------------

@app.get("/login",response_class = HTMLResponse)
def login_get(request:Request):
   return TEMPLATES.TemplateResponse("login.html",{"request":request})

#--------------------------------------------------
#Login Post Method
#---------------------------------------------------

@app.post("/login",response_class = HTMLResponse)
async def login_post(request:Request, email:str=Form(...),password:str=Form(...)):
# async def login_post(request:Request):
   form = LoginForm(request)
   await form.load_data()
   try:
      if not await form.is_valid():
            # Form data is not valid
            raise HTTPException(status_code=400, detail="Form data is not valid")
        # Form data is valid, generate new access token
      response = RedirectResponse("/dashboard", status.HTTP_302_FOUND)

      login_for_access_token(response=response, form_data=form)
    #   form.__dict__.update(message="Login Successful!")
      return response

   except HTTPException as exception:
      # Catch HTTPException and update form with error message
      form.__dict__.update(message="Incorrect email or password")
    #   form.__dict__.get("errors")#.append(exception.detail)
      return TEMPLATES.TemplateResponse("login.html", form.__dict__)

   except Exception as exception:
      # Catch any other exception and return 500 Internal Server Error
      raise HTTPException(status_code=500, detail=str(exception)) from exception