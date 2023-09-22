import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routes import api, misc, auth

tags_metadata = [
    {
        "name": "products",
        "description": "Operations with products.",
    },
]


app = FastAPI(openapi_tags=tags_metadata)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api.api_router)
app.include_router(misc.api_router)
app.include_router(auth.api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
