from fastapi import FastAPI

app=FastAPI()

@app.get("/test")
def hi():
    return{
        "message":"hi hi im her"
    }