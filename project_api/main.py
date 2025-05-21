from fastapi import FastAPI, Depends
from route import aplicativo
import uvicorn
import os

app = FastAPI()

app.include_router(aplicativo.router)

@app.get("/", tags=['Root'])
async def root():
    return {"message": "Este é o API do Tech Challenge 4 da FIAP"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)