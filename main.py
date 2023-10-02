import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from routes import api, misc, auth

tags_metadata = [
    {
        "name": "products",
        "description": "Operations with products.",
    },
]


app = FastAPI(openapi_tags=tags_metadata)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api.api_router)
app.include_router(misc.api_router)
app.include_router(auth.api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
