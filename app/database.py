from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Sreeshma123#@localhost:5432/fastapi"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try:
#         conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',
#                             password='Sreeshma123#',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("DATABASE CONNECTION SUCCESSFULL")
#         break
#     except Exception as err:
#         print("SORRY !! CONNECTION FAILED")
#         print("ERROR : ",err)
#         time.sleep(0.1)