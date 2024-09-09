import http
import random
import string

from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from prometheus_client import generate_latest

from redis_db.redis import redisConn

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def generate_password(size, include_numb, include_special_char):
    char = string.ascii_letters

    if include_numb:
        char += string.digits
    if include_special_char:
        char +=string.punctuation

    password = ''.join(random.choices(char, k=size))
    return password


@router.get("/", response_class=HTMLResponse)
@router.post("/", response_class=HTMLResponse)
async def index(
    request: Request,
    size: int = Form(8),
    include_numb: bool = Form(False),
    include_special_char: bool = Form(False),
    ):
    generated_password_counter = 0
    if request.method == http.HTTPMethod.POST:
        print(size)
        password = generate_password(
            size=size, 
            include_numb=include_numb, 
            include_special_char=include_special_char,
            )

        redisConn.lpush("senhas", password)
        generated_password_counter += 1

    passwords = redisConn.lrange("senhas", 0, 9)
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
        "index.html",
        {"request": request},
        )

@router.get("/api/senhas")
def list_passwords():
    passwords = redisConn.lrange("senhas", 0, 9)

    result = [{"id": index + 1, "senha": senha} for index, senha in enumerate(passwords)]
    return result

@router.get("/metrics")
def metrics():
    return generate_latest()