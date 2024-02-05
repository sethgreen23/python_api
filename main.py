from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None # optional and default to none
    published: bool = True # optional

@app.get("/")
async def root():
    return {"message": "Hello to my api"}

@app.get("/posts")
async def get_posts():
    return {"data": "this is my post"}

@app.post("/createposts")
def create_posts(post: Post):
    print(post)
    # change pydantic model to dictionary
    print(post.dict())
    return {
            "data": f"title: {post.title}, content: {post.content}",
            "json_data": post.dict()}
