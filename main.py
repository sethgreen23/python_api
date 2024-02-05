from fastapi import FastAPI, Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello to my api"}

@app.get("/posts")
async def get_posts():
    return {"data": "this is my post"}

@app.post("/createposts")
def create_posts(payload: dict = Body):
    print(payload)
    return {"message": "post create successfull",
            "data": f"title: {payload['title']}, content: {payload['content']}"}
