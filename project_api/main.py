from fastapi import FastAPI, Depends
from route import aplicativo

app = FastAPI()

app.include_router(aplicativo.router)

@app.get("/", tags=['Root'])
async def root():
    return {"message": "Este é o API do Tech Challenge 4 da FIAP"}

