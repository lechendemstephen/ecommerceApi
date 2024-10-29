from fastapi import APIRouter 



router = APIRouter(
    tags= ['products']
)


@router.get('/product')
async def get_users(): 

    return {
        "products": "show all product"
    }

# adding products to the database 


