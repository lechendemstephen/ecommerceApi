from pydantic_settings import BaseSettings 

class Settings(BaseSettings): 
    DATABASE_NAME: str 
    DATABASE_PASSWORD: str 
    DATABASE_HOST: str 


    class Config: 
        env_file = '.env'


settings = Settings()

