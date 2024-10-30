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
async def get_users(db: Session = Depends(get_db), limit=10): 
    all_products = db.query(Products).limit(limit).all()


    return {
        "products": all_products
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

@router.delete('/id')
async def delete_product(id: int , db: Session = Depends(get_db)): 
    single_product = db.query(Products).filter(Products.id == id).first()

    if single_product == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'no product found with id: {id}')
    
    db.delete(single_product)
    db.commit()

    return {
        "message": f'product with id {id} successfully deleted'
    }

@router.put('/id')
async def update_product(id:int,
    update_product = schemas.ProductUpdate,          
    image:  UploadFile = File(...), db: Session = Depends(get_db)): 

    edit_product = db.query(Products).filter(Products.id ==id).first()

    if edit_product == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'no product with id {id} found')
    
    for key, value in update_product.dict().items(): 
        if value is not None: 
            setattr(edit_product, key, value)

    if image: 
        # saving uploaded image 
        image_fileaname = f'{uuid4()}.jpg'
        image_path = os.path.join(schemas.PRODUCT_DIR, image_fileaname)
    
        with open(image_path, "wb") as buffer: 
            buffer.write(await image.read())
        
        edit_product.img_path = image_path 
    
    db.commit()
    db.refresh(edit_product)

    return edit_product 

