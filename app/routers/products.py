from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from .. import schemas
from ..database.database import get_db
from uuid import uuid4
import os
from ..models.models import Products

router = APIRouter(
    tags= ['products']
)


@router.get('/product')
async def get_users(): 

    return {
        "products": "show all product"
    }

# adding products to the database 
@router.post('/')
async def create_product(
    name: str ,
    description: str ,
    price: float ,
    image:  UploadFile = File(...), db: Session = Depends(get_db)): 

    if image.content_type not in ["image/jpeg", "image/png"]: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='only jpeg and png allowed')
    
    # saving uploaded image 
    image_fileaname = f'{uuid4()}.jpg'
    image_path = os.path.join(schemas.PRODUCT_DIR, image_fileaname)
   
    with open(image_path, "wb") as buffer: 
        buffer.write(await image.read())

    new_product = Products(
        name = name, 
        des = description, 
        img_path = image_path,
        price =price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product 

    


