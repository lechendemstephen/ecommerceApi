from fastapi import FastAPI
from .database.database import Base, engine
from .models import models
from .routers import authentication, order, cart, products


Base = models.Base.metadata.create_all(bind=engine)
app = FastAPI(

)


app.include_router(authentication.router)
app.include_router(order.router)
app.include_router(products.router)
app.include_router(cart.router)

