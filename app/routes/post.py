from datetime import datetime
from typing import List, Optional
from fastapi import Depends, HTTPException,Response,status,APIRouter
from pydantic import BaseModel
from sqlalchemy import func
from .. import model,schemas,oauth
from ..database import get_db
from sqlalchemy.orm import Session

router=APIRouter(prefix='/post')





@router.post('/createpost',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def addpost(req:schemas.Create_post,db:Session=Depends(get_db),Current_user:int=Depends(oauth.getCurrent_user)):
    print(Current_user)
    print(Current_user.id)
 
    data=model.Post(user_id=Current_user.id,**req.dict())
    db.add(data)
    print("add data")
    db.commit()
    print("commited")
    db.refresh(data)
    
    return data


@router.get('/{id}',response_model=schemas.Postvote)
def get_One_post(id:int,db:Session=Depends(get_db),Current_user:int=Depends(oauth.getCurrent_user)):
    print(type(Current_user.id))
    
    post=db.query(model.Post,func.count(model.Votes.post_id).label("votes")).join(model.Votes,
                model.Votes.post_id==model.Post.id,isouter=True).group_by(model.Post.id).filter(model.Post.id == id)
    p=post.first()
    if not p:
        raise HTTPException(status_code=404,detail=f"Sorry !! post with id:{id} is not found")
    # if post.user_id !=Current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    return p




@router.delete('/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),Current_user:int=Depends(oauth.getCurrent_user)):
    print(Current_user)
    p=db.query(model.Post).filter(model.Post.id == id)
    post=p.first()
    if not post:
        raise HTTPException(status_code=404,detail=f"Post with this id :{id} already deleted")
    
    if post.user_id !=Current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    p.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_201_CREATED)




@router.put('/update/{id}',response_model=schemas.Post)
def update(id:int,post:schemas.Create_post,db:Session=Depends(get_db),Current_user:int=Depends(oauth.getCurrent_user)):
    print(Current_user)
    postdata=db.query(model.Post).filter(model.Post.id==id)
    post=postdata.first()
    if post==None:
        raise HTTPException(status_code=404,detail=f"Sorry cant update, Post doesnt exist")
    if post.user_id !=Current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    postdata.update(post.dict(),synchronize_session=False)
    db.commit()
    return postdata.first()




@router.get('/',response_model=List[schemas.Postvote])
# @router.get('/')
def getpost(db:Session=Depends(get_db),user_id:int=Depends(oauth.getCurrent_user),
            limit:int=10,skip:int=0,search:Optional[str]=""):
    print("limit is ",limit)
    
    results=db.query(model.Post,func.count(model.Votes.post_id).label("votes")).join(model.Votes,
                model.Votes.post_id==model.Post.id,isouter=True).group_by(model.Post.id).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    print("after")
    print("result")
    return results

# {{URL}}post?search=some%20b perct 20 for space