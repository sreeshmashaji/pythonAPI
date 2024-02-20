from fastapi import  FastAPI
from .routes import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware
# from . import model
# from .database import  engine

# model.Base.metadata.create_all(bind=engine)

# print(settings.db_username)
app=FastAPI()

origin=['*']
app.add_middleware(   #runs before every rqst
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router( vote.router)
























# my_posts=[{'id':1,'title':"Mr.bean",'content':"New cartoon",'published': True, 'rating': None}]#hardcode ..else data lost after each reload

# def find_post(id):
#     for i in my_posts:
#         if i['id'] == id:
#            return i
        
# def find_index(id):
#     for i,p in enumerate(my_posts):
#         if p['id']==id:
#             return i



@app.get('/')
async def root():
    return{"message":"Good Evening","status":True} # autmatically covert it into json


## USER
