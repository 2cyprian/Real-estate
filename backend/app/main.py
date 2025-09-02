from fastapi import FastAPI
from app.api import auth
from app.users import router as users_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

app.include_router(auth.router)
app.include_router(users_router.router)
