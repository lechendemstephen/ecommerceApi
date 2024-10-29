from jose import jwt, JWTError
from datetime import datetime, timedelta
from .schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
#access_token_expire_minutes
#secret_key 
#algorithm 

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = '3797417a0826d8795ac273d0f3af032d79ab13479c6a3007a66be47e161bbbe6'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 

# function to create an access token
def create_access_token(data: dict): 
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# verify the token 

def verify_access_token(token: str, credential_exception): 
    try: 
       payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except: 
        raise credential_exception
    
    id: str =  payload.get('user_id')
    if not id: 
        raise JWTError

    Token_data = TokenData(token=str(id))

    return Token_data

def get_curent_user(token: str  = Depends(oath2_scheme)): 
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')

    return verify_access_token(token, credential_exception)

   

    