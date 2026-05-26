from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # importing this to get my api services from one server or domain to another
from . import models
from .database import engine
from .routers import post, user, auth, votes
from .config import settings


# models.Base.metadata.create_all(bind=engine) # this is for creating all models before alembic 

origins = ["*"] #if it is for specific app then specify it otherwise use "*" in list

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],# using this we can allow only specific methods and header with specific domains
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

# request Get method url: "/" will always be first to be executed
#  Order does matter
@app.get("/")
def root():
    return {"message": "Welcome to my API here"}

# (Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ;
# (& d:\pyythonn\pp\APIS\venv\Scripts\Activate.ps1)

#git remote add origin https://github.com/syedaoung55-bot/Social-media-API.git