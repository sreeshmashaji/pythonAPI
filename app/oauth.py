from datetime import datetime, timedelta
from fastapi import Depends, HTTPException,status
from jose import JWTError,jwt
import pytz
from . import schemas,database,model
from fastapi.security.oauth2 import OAuth2PasswordBearer
from pytz import timezone
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema=OAuth2PasswordBearer(tokenUrl='login')
IST = timezone('Asia/Kolkata')

SECRET_KEY =settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes





def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(pytz.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    print(to_encode)
    print(expire)
    encode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    print(encode_jwt)
    return encode_jwt



def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        print(payload.get("exp"))
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
        print(type(token_data.id))
    except JWTError:
        raise credentials_exception

    return token_data
    


def getCurrent_user(token: str = Depends(oauth2_schema),db:Session=Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token= verify_access_token(token, credentials_exception)
    user=db.query(model.Users).filter(model.Users.id==token.id).first()
    print("user",user.id)
    return user

   