from fastapi import FastAPI
app = FastAPI()
#dicrator
@app.get("/welcome")
def welcome():
    return {
        "message": "Welcome to MINI-RAG"
    }