import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

# Temporarily modify the path to import main.py
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
sys.path.pop(0)

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_mlflow_load_model():
    with patch('main.mlflow.pyfunc.load_model') as mock_load:
        # Create a mock model that has a .predict method
        mock_model = MagicMock()
        mock_model.predict.return_value = ["positive"]
        mock_load.return_value = mock_model
        yield

@pytest.fixture(autouse=True)
def set_mlflow_env_vars():
    # Set environment variables for MLflow tracking URI and model name
    os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5000"
    os.environ["MLFLOW_MODEL_NAME"] = "sentiment_classifier"
    yield
    # Clean up environment variables after tests
    del os.environ["MLFLOW_TRACKING_URI"]
    del os.environ["MLFLOW_MODEL_NAME"]

def test_health_check_model_loaded():
    # Simulate model being loaded successfully on startup
    with patch('main.model', new=MagicMock()): # Ensure main.model is not None
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "model_loaded": True}

def test_health_check_model_not_loaded():
    # Simulate model failing to load on startup
    with patch('main.model', new=None):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "error", "model_loaded": False, "message": "Model not loaded"}

def test_predict_success():
    with patch('main.model') as mock_model_instance:
        mock_model_instance.predict.return_value = np.array(["positive"])
        response = client.post("/predict", json={"text": "This is a test."})
        assert response.status_code == 200
        assert response.json() == {"text": "This is a test.", "sentiment": ["positive"]}
        mock_model_instance.predict.assert_called_once_with(["This is a test."])

def test_predict_model_not_loaded():
    with patch('main.model', new=None):
        response = client.post("/predict", json={"text": "This is a test."})
        assert response.status_code == 503
        assert response.json() == {"error": "Model not loaded. Please check MLflow tracking server and model availability."}
