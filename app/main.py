from fastapi import FastAPI,APIRouter, Body, status, HTTPException, Response, Depends
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import  models, schema, utils
from .routers import post, user
from .database import get_db, engine




models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
	try:
		conn = psycopg2.connect(database="fastapi",
								user="postgres",
								password="1234",
								host="localhost",
								port="5432",
								cursor_factory=RealDictCursor
        						)
		cur = conn.cursor()
		print("Connection successfull!")
		break
	except Exception as error:
		print("Connection failed!")
		print("Error: ", error)
		time.sleep(2000)



my_posts = [{"title": "Favorite food", "content": "I like eating pizza", "id": 1},
            {"title": "Best beatches in california", "content": "Sans Francisco Beatch", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            print(p, i)
            return i
    return None

app.include_router(post.router)
app.include_router(user.router)
