from fastapi import FastAPI
from src import user, list
from starlette.responses import RedirectResponse


app = FastAPI()

app.include_router(user.router)
app.include_router(list.router)

@app.get("/", include_in_schema=False)
async def Home():
    return RedirectResponse(url='/docs')
