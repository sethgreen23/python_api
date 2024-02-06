from fastapi import FastAPI, Body, status, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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
		time.sleep(2)

class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None # optional and default to none
    published: bool = True # optional

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

@app.get("/")
async def root():
    return {"message": "Hello to my api"}

@app.get("/posts")
async def get_posts():
    cur.execute("""SELECT * FROM posts """)
    posts = cur.fetchall()
    # serialize automaticaly the list
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cur.execute(""" INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
                (post.title, post.content, post.published))
    new_post = cur.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 
                            detail=f"Post with id {id} is not found")
        # response.status_code = 400
        # return {"message": f"Post with id {id} is not found"}
    return {"data":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found")
    my_posts.pop(index)
    # with fastapi you dont send content you just send the status
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}