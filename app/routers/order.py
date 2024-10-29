from fastapi import APIRouter 



router = APIRouter(
    tags= ['Orders']
)


@router.get('/orders')
async def get_users(): 


    return {
        "orders": "show all orders"
    }


