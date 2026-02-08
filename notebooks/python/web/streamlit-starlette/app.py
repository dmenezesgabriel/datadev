from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.routing import Mount, Route
from streamlit.starlette import App

api = FastAPI()


@api.get("/hello")
async def hello():
    return {"message": "Hello, World"}


routes = [
    Mount("/api", app=api),
]


@asynccontextmanager
async def lifespan(app):
    print("Application running")

    yield
    print("Application stopped")


app = App("main.py", lifespan=lifespan, routes=routes)
