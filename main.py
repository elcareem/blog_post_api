from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel


app = FastAPI()

posts = {
    1: {
        "author": "john",
        "content": "RESTful APIs allow communication between a client and a server using standard HTTP methods such as GET, POST, PUT, and DELETE"
    }
}

id = 1

def generate_id():
    global id
    id += 1 

class Post(BaseModel):
    author: str
    content: str

class UpdatePost(BaseModel):
    author: str | None = None
    content: str | None = None

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
def read_post(post_id: int): 
    if post_id not in posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return posts[post_id]


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):

    posts[id] = post
    message = posts[id]
    generate_id()
    return message



@app.put("/posts/{post_id}") 
def update_post(post_id: int, post: Post): 
    if post_id not in posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    posts[post_id] = post

    return posts[post_id]

@app.patch("/posts/{post_id}")
def update_post_content(post_id: int, post: UpdatePost):
    if post_id not in posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post.author == None:
        post.author = posts[post_id]["author"]

    if post.content == None:
        post.content = posts[post_id]["content"]
        
    posts[post_id]["author"] = post.author
    posts[post_id]["content"] = post.content
    return {"message": "Post update successfull"}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    del posts[post_id]

    return 