from fastapi import APIRouter, Depends, HTTPException, status
from ..database.database import get_db
from sqlalchemy.orm import Session
from .. import schemas
from ..models.models import SignUp
from ..utils import hash_password, verify_password
from ..oath2 import create_access_token
from typing import List



router = APIRouter(
    tags= ['Authentication'],
    prefix='/user'
)


@router.get('/')
def get_users(db: Session = Depends(get_db), limit=3): 
    all_users = db.query(SignUp).limit(limit).all()

    return {
        "users": all_users
    }

# signup users to the Api 
@router.post('/', response_model=schemas.SignupResponse)
def create_user(request_user:schemas.SignUp,  db: Session = Depends(get_db)): 

    request_user.password = hash_password(request_user.password)

    new_user = SignUp(
        **request_user.dict()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post('/login')
def login_user(request_user: schemas.Login, db: Session = Depends(get_db)): 
    
    user = db.query(SignUp).filter(SignUp.email==request_user.email).first()
# checking if a user with the provided email address exist in the database 
    if user == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid user credentials')
# verifying the password provided 
    if not verify_password(request_user.password, user.password): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid user credentials')
    
    # generate an access token
    access_token = create_access_token({"user_id": user.id})


    return {
        "message": access_token
    }
    
@router.delete('/id')
async def delete_user(id:int, db: Session = Depends(get_db)):
    user = db.query(SignUp).filter(SignUp.id == id).first()

    if user == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'no user found with id {id}')
    db.delete(user)
    db.commit()

    return {
        "message": f'user with id {id} deleted'
    }

@router.put('/id')
async def edit_user(update_user: schemas.UpdateSignUp, id:int, db: Session =Depends(get_db)): 
    edit_user = db.query(SignUp).filter(SignUp.id == id).first()

    if edit_user == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'no user with id: {id} found')
    
    for key, value in update_user.dict().items(): 
        if value is not None: 
            setattr(edit_user, key, value)
    
    db.commit()
    db.refresh(edit_user)

    return {
        "message": f'user with {id} edited'
    }
    


