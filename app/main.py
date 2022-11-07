from mangum import Mangum
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from src.controller import UserController, ListController


app = FastAPI(title='AWS Lambda FastAPI')

app.include_router(UserController.router, prefix="/api/v1")
app.include_router(ListController.router, prefix="/api/v1")

@app.get("/", include_in_schema=False)
async def Home():
    return RedirectResponse(url='/docs')

handler = Mangum(app)