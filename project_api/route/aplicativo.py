from fastapi import FastAPI, HTTPException, APIRouter
from time import time
import torch
import numpy as np
from modelos import LSTM, PriceData
from utils.activate_mlflow import setup_mlflow, MLFLOW_EXPERIMENT_ID
import mlflow


# FastAPI
router = APIRouter(tags=['Predict'])
app = FastAPI(title='API de Privisão de Preço de Ações - Tech Challenge 4')

# MLFlow
mlflow_ready = setup_mlflow()

# Model
try:
    model = LSTM(1,4,1)
    model.load_state_dict(torch.load('utils/model.pth', map_location='cpu'))
    model.eval()

    scaler = torch.load('utils/scaler.pkl')
except Exception as e:
    print(f'erro ao carregar modelo {e}')

# Endpoint
@router.post("/predict", 
             summary="Previsão de preços de ações da Apple", 
             description="Insira os 7 últimos preços de fechamento das ações, do mais antigo para o mais recente, em uma lista, e obtenha" \
             " o preço previsto para o próximo dia.")
async def predict_price(data: PriceData):
    sequence = data.history
    lookback = 7
    
    if len(sequence) != lookback:
        raise HTTPException(status_code=400, detail=f"Número de dados inválidos. Espera-se {lookback} valores, mas foram inseridos {len(sequence)}")
    
    try:
        start_time = time()

        input_array = np.zeros((1,8))
        input_array[0,1:] = sequence
        scale_data = scaler.transform(input_array)[0,1:]

        X = torch.tensor(scale_data, dtype=torch.float32).unsqueeze(0).unsqueeze(2)

        with torch.no_grad():
            prediction = model(X).item()    

        prediction_array = np.zeros((1,8))
        prediction_array[0,0] = prediction
        prediction_array[0,1:] = sequence
        prediction_real = scaler.inverse_transform(prediction_array)[0,0]

        duration = time() - start_time
        
        # ML Flow log in Databricks
        if mlflow_ready:
            try:
                active_run = mlflow.active_run()
                if active_run:
                    mlflow.end_run()

                with mlflow.start_run(run_name='prediction-api-call', experiment_id=MLFLOW_EXPERIMENT_ID):
                    mlflow.log_param("lookback", lookback)
                    mlflow.log_metric("prediction", prediction_real)
                    mlflow.log_metric("response_time", duration)
                    mlflow.log_param('input_history',str(list(sequence)))
                    mlflow.log_param('model_architecture', 'LSTM(1,4,1)')   
                    print(f'MLFlow logging complete: {mlflow.active_run().info.run_id}')        
            except Exception as e:
                print(f'MLFlow logging error {str(e)}')
        
        return {"Prediction": float(prediction_real)}
    
    except Exception as e:

        try:
            if mlflow.active_run():
                mlflow.end_run()
        except:  # noqa: E722
            pass
        
        raise HTTPException(status_code=500, detail=str(e))