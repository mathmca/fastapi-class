from fastapi import FastAPI
from .routers import post, user, auth, like
#from .database import engine
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)-- not necessary with alembic installed

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)

@app.get('/')
def root():
    return "HELLOW"