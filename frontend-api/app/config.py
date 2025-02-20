import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL") or 'mysql+mysqlconnector://motunrayo:koyejo@mysql_container:3306/library_frontend'
    SECRET_KEY = os.environ.get("SECRET_KEY")
    BACKEND_API_URL = os.environ.get("BACKEND_API_URL")

config = Config()
