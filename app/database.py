from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
import time

#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip_adress/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


'''
while True:
    try:
        conn = psycopg2.connect(host=, database=, user=,
                                password=, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Database connection was sucessfull!")
        break
    except Exception as error:
        print(f"Coonection to dabase failed ->\n Error was {error}")
        time.sleep(5)
'''