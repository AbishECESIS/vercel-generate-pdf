from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def chekapi():
    return "Welcome this is working" 