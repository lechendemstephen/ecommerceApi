from fastapi import APIRouter 



router = APIRouter(
    tags= ['cart']
)


@router.get('/cart')
async def get_users(): 


    return {
        "carts": "show all carts"
    }


