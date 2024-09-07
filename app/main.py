import logging
import os
from routes import generator_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI(
    title="Giropops Senhas - FastAPI version",
    summary="""Gerador de senhas"""
    )

app.mount(
    "/static", 
    StaticFiles(directory="static"), 
    name="static",
    )
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generator_routes.router)


logging.basicConfig(filename='error.log', level=logging.DEBUG)