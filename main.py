from fastapi import FastAPI
from src import user


app = FastAPI()

app.include_router(user.router)

@app.get("/")
async def Home():
    return {"message": "Hello World"}
