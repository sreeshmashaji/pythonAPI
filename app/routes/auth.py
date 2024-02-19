from fastapi import APIRouter,Depends,status,HTTPException,Response
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas,model,utills,oauth



router=APIRouter(tags=['Authentication'])

# @router.post('/login')
# def login(user_cred:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
   
   
#    user= db.query(model.Users).filter(model.Users.email == user_cred.username).first()
#    if not user:
#       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid User Credentials")
#    if not utills.verify(user_cred.password,user.password):
#       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"incorrect password")
#    token=oauth.create_access_token(data={"user_id":user.id})
#    return {"token":token,"token_type":"bearer"} 


@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(model.Users).filter(
        model.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utills.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = oauth.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}



   