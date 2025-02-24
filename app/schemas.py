from pydantic import BaseModel, EmailStr
import os
from fastapi import UploadFile, File 


class SignUp(BaseModel):
    name: str 
    email: EmailStr
    password: str 

class Login(BaseModel): 
    email: EmailStr
    password: str

class TokenData(BaseModel): 
    token: str 

class product(BaseModel): 
    name: str 
    description: str 
    price: float 
    image:  UploadFile = File(...)

# Upload directory for the images 
PRODUCT_DIR = 'products/'
# ensure the upload directory exist
os.makedirs(PRODUCT_DIR, exist_ok=True)
