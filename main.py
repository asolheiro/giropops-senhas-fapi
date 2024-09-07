import os
import redis
import string
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Giropops Senhas - FastAPI version",
    summary="""Gerador de senhas"""
    )

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


@app.get("/")
def index():
    passwords = reddisConn.lrange("senhas", 0, 9)
    if passwords:
        generated_passwords = [{"id": index + 1, "senha": password} for index, password in enumerate(passwords)]
        return rende_template