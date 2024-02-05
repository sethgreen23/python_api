from fastapi import FastAPI, Body, status, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

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

@app.get("/")
async def root():
    return {"message": "Hello to my api"}

@app.get("/posts")
async def get_posts():
    # serialize automaticaly the list
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {
            "data": post_dict
            }

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 
                            f"Post with id {id} is not found")
        # response.status_code = 400
        # return {"message": f"Post with id {id} is not found"}
    return {"data":post}
