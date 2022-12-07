from mangum import Mangum
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from src.controller import UserController, ListController


app = FastAPI(title='Publisto Documentation', root_path='/main')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserController.router, prefix="/api/v1")
app.include_router(ListController.router, prefix="/api/v1")

@app.get("/", include_in_schema=False)
async def Home():
    return RedirectResponse(url='/main/docs')

handler = Mangum(app)