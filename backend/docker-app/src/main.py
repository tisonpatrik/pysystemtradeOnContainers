from fastapi import FastAPI, status

app = FastAPI()

@app.get("/")
async def root():
    return {"Say": "Hello!"}
