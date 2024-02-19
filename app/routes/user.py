from typing import List
from fastapi import Depends, HTTPException,status,APIRouter
from .. import model,schemas,utills,oauth
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordBearer

oauth_schema=OAuth2PasswordBearer(tokenUrl="token")

router=APIRouter(prefix='/users')

@router.post('/createuser',status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(req:schemas.Usercreate,db:Session=Depends(get_db)):
    
    req.password=utills.hash(req.password)
    data=model.Users(**req.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.get('/',response_model=List[schemas.UserResponse])
def getuser(db:Session=Depends(get_db)):
    user=db.query(model.Users).all()
  
    return user

@router.get('/{id}',response_model=schemas.UserResponse)
def getOneuser(id:int,db:Session=Depends(get_db)):
    userOne=db.query(model.Users).filter(model.Users.id == id).first()

    if not userOne:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} not found")
    return userOne

    











   


