from sqlalchemy import create_engine
from typing import cast, Any
import psycopg
from psycopg.rows import dict_row
import time
from .config import settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try:
#         conn = psycopg.connect(host='localhost',dbname='Fastapi', user='postgres',
#                             password='Alimola-#12', row_factory=cast(Any, dict_row) )
#         cursor= conn.cursor()
#         print("Database connection was succesfull!")
#         break;
#     except Exception as error:
#         print("Connecting to database failed!")
#         print("error: ", error)
#         time.sleep(2)
