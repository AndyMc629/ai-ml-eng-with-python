# Agentic ML Backend

This project sets up a FastAPI application to serve a machine learning model, integrated with a local MLflow tracking server for model management.

## Project Structure

- `.devcontainer/`: Contains `Dockerfile` for setting up the development environment.
- `mlruns/`: Directory for MLflow tracking data (created by MLflow).
- `main.py`: The FastAPI application, responsible for loading the model from MLflow and serving predictions.
- `requirements.txt`: Python dependencies for the project.
- `train_model.py`: A script to simulate training a simple sentiment classifier and registering it with MLflow.
- `docker-compose.yml`: Defines the services for the MLflow tracking server and the FastAPI application.

## Setup and Running Locally

1.  **Build and Run Docker Containers:**
    Navigate to the `agentic-ml-backend` directory and run:
    ```bash
    docker-compose up --build -d
    ```
    This will start the MLflow tracking server (on `http://localhost:5000`) and the FastAPI application (on `http://localhost:8000`).

2.  **Train and Register a Model:**
    Before the FastAPI application can serve predictions, a model needs to be registered with MLflow. You can run the `train_model.py` script inside the `fastapi-app` container:
    ```bash
    docker-compose exec fastapi-app python train_model.py
    ```
    This script will train a dummy sentiment classifier and register it as `sentiment_classifier` in your local MLflow instance.

3.  **Access the FastAPI Application:**
    -   **API Docs (Swagger UI):** `http://localhost:8000/docs`
    -   **Health Check:** `http://localhost:8000/health`
    -   **Predict Endpoint:** `http://localhost:8000/predict` (POST request with JSON body `{"text": "your text here"}`)

4.  **Access MLflow UI:**
    -   `http://localhost:5000`

## Testing

Unit tests are located in the `tests/` directory. To run them:

```bash
# First, ensure you are in the agentic-ml-backend directory
docker-compose exec fastapi-app pytest
```

## Cleaning Up

To stop and remove the Docker containers and networks:

```bash
docker-compose down
```

To remove MLflow tracking data (optional):

```bash
rm -rf mlruns
```
