from fastapi import FastAPI
from route import aplicativo
import uvicorn
import os

description = """ API de predição de preços de ações da Apple """

app = FastAPI(title="LSTM Preço de Ações",
              description=description,
              summary="Preditor usa os últimos 7 preços de fechamento das ações para prever o próximo preço de fechamento",
              version="0.0.1",
              contact={
                  "name": "Adams Souza",
                  "github do projeto": "https://github.com/adamsdossantos/lstm",
                  "histórico de preços para teste": "https://github.com/adamsdossantos/lstm/blob/main/history.txt"
                  },
                  license_info={
                      "name": "MIT",
                      "url": "https://mit-license.org/",
                      },
                      )

app.include_router(aplicativo.router)

@app.get("/", tags=['Root'])
async def root():
    return {"message": "API de predição de preços de ações da Apple"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)