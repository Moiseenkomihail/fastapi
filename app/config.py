import os 
from dotenv import load_dotenv

load_dotenv()


DB_HOST= os.environ.get('DB_HOST')
DB_PORT= os.environ.get('DB_PORT')
DB_NAME= os.environ.get('DB_NAME')
DB_PASS= os.environ.get('DB_PASS')
DB_USER= os.environ.get('DB_USER')

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_ECHO = True

SECRET_KEY = os.environ.get('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60*24*14
ALGORITHM = "HS256"
    
