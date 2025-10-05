import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

def get_phonepe_engine():
    load_dotenv()  
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")

    return create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")