from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import os

app = FastAPI()

# MLflow configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MLFLOW_MODEL_NAME = os.getenv("MLFLOW_MODEL_NAME", "sentiment_classifier")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

class TextPayload(BaseModel):
    text: str

model = None

@app.on_event("startup")
async def load_model():
    global model
    try:
        # Load the latest version of the model from MLflow
        model = mlflow.pyfunc.load_model(f"models:/{MLFLOW_MODEL_NAME}/latest")
        print(f"Model '{MLFLOW_MODEL_NAME}' loaded successfully from {MLFLOW_TRACKING_URI}")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None # Ensure model is None if loading fails

@app.get("/health")
async def health_check():
    if model is not None:
        return {"status": "ok", "model_loaded": True}
    else:
        return {"status": "error", "model_loaded": False, "message": "Model not loaded"}

@app.post("/predict")
async def predict_sentiment(payload: TextPayload):
    if model is None:
        return {"error": "Model not loaded. Please check MLflow tracking server and model availability."}, 503
    try:
        # For a simple classifier, assume the model's predict method takes text directly
        # and returns a sentiment score or class.
        prediction = model.predict([payload.text])
        return {"text": payload.text, "sentiment": prediction.tolist()}
    except Exception as e:
        return {"error": f"Prediction failed: {e}"}, 500
