import http
import random
import redis
import string
import os
from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI(
    title="Giropops Senhas - FastAPI version",
    summary="""Gerador de senhas"""
    )

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headears=["*"],
)


redis_host = os.environ.get('REDIS_HOST, "redis-service')
redis_port = 6379
redis_password = ""

reddisConn = redis.StrictRedis(
    host=redis_host, 
    port=redis_port, 
    password=redis_password,
    decode_responses=True
    )

def generate_password(size, include_numb, include_special_char):
    char = string.ascii_letters

    if include_numb:
        char += string.digits
    if include_special_char:
        char +=string.punctuation

    password = ''.join(random.choices(char, k=size))
    return password


@app.get("/", response_class=HTMLResponse)
@app.post("/", response_class=HTMLResponse)
async def index(
    request: Request,
    size: int = Form(8),
    include_numb: bool = Form(False),
    include_special_char: bool = Form(False),
    ):

    if request.method == http.HTTPMethod.POST:
        password = generate_password(
            size=size, 
            include_numb=include_numb, 
            include_special_char=include_special_char,
            )

        reddisConn.lpush("senhas", password)
        global generated_password_counter
        generated_password_counter += 1

    passwords = reddisConn.lrange("senhas", 0, 9)
    if passwords:
        generated_passwords = [{"id": index + 1, "senha": password} for index, password in enumerate(passwords)]
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request,
                "senhas_geradas": generated_passwords, 
                "password": generated_passwords[0]['senha'] or '',
            }
        )
    return templates.TemplateResponse(
        'index.html',
        {"request": request},
        )
