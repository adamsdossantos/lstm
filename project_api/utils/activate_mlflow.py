import mlflow
from dotenv import load_dotenv
import os

load_dotenv()

# Databricks MLFlow config
MLFLOW_EXPERIMENT_NAME = os.environ.get('MLFLOW_EXPERIMENT_NAME', 'stock_prediction')
MLFLOW_EXPERIMENT_ID = os.environ.get('MLFLOW_EXPERIMENT_ID', '124085071381802')
DATABRICKS_HOST = os.environ.get('DATABRICKS_HOST', 'https://dbc-2c1d949b-0bdd.cloud.databricks.com')
DATABRICKS_TOKEN = os.environ.get('DATABRICKS_TOKEN')

# MLflow
def setup_mlflow():
    try:
        mlflow.set_tracking_uri('databricks')

        if DATABRICKS_HOST:
            os.environ['DATABRICKS_HOST'] = DATABRICKS_HOST    

        if DATABRICKS_TOKEN:
            os.environ['DATABRICKS_TOKEN'] = DATABRICKS_TOKEN

        if MLFLOW_EXPERIMENT_ID:
            experiment = mlflow.get_experiment(MLFLOW_EXPERIMENT_ID)
            if experiment:
                print(f'Experiment ID {MLFLOW_EXPERIMENT_ID}, name: {MLFLOW_EXPERIMENT_NAME}')

        else:
            experiment = mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
            print(f"Experiment name: {MLFLOW_EXPERIMENT_NAME}")
        
        print(f"MLflow setup complete: tracking_uri='databricks', host={DATABRICKS_HOST}")
        return True
        
    except Exception as e:
        print(f'set_experiment failed {e}')
        return False