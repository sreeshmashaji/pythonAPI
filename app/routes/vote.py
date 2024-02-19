from fastapi import Depends, HTTPException,status,APIRouter
from .. import database,schemas,model,oauth
from sqlalchemy.orm import Session




router=APIRouter(prefix='/vote',
                 tags=['Vote'])

@router.post('/',status_code=status.HTTP_201_CREATED)
def create_vote(vote:schemas.Vote,db:Session=Depends(database.get_db),current_user:int=Depends(oauth.getCurrent_user)):
    print("enter")
    post=db.query(model.Post).filter(model.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post not found for voting")
    votequery=db.query(model.Votes).filter(model.Votes.post_id==vote.post_id,model.Votes.user_id==current_user.id)
    found_vote=votequery.first()
    print(found_vote)
    if(vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user with id {current_user.id} alreday voted for post_id:{vote.post_id}")
        newvote=model.Votes(post_id=vote.post_id,user_id=current_user.id)
        db.add(newvote)
        db.commit()
        return "successfully added vote"
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found vote")
        votequery.delete(synchronize_session=False)
        db.commit()
        return "successfully deleted"

