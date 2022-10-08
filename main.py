from fastapi import FastAPI
from src.controller import UserController, ListController
from starlette.responses import RedirectResponse


app = FastAPI()

app.include_router(UserController.router)
app.include_router(ListController.router)

@app.get("/", include_in_schema=False)
async def Home():
    return RedirectResponse(url='/docs')
