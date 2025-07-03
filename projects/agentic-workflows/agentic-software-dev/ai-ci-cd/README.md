# AI CI/CD Pipeline

This repository contains a comprehensive CI/CD pipeline template for AI/ML projects, including:
- Docker container builds
- Python test suite execution
- Code linting with Ruff
- Integration testing with Databricks and MLflow
- Test coverage requirements

## Project Structure

```
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
│   ├── unit/
│   └── integration/
├── .dockerignore
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── .ruff.toml
```

## CI/CD Pipeline

The pipeline performs the following steps:
1. Linting with Ruff
2. Unit testing with pytest (80% coverage required)
3. Integration testing with Databricks/MLflow
4. Docker container build
5. Test container deployment

## Requirements

- Python 3.9+
- Docker
- GitHub Actions
- Databricks API credentials
- MLflow server access

## Usage

1. Configure your environment variables in GitHub Secrets:
   - `DATABRICKS_HOST`
   - `DATABRICKS_TOKEN`
   - `MLFLOW_TRACKING_URI`
   - `DOCKER_REGISTRY`
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`

2. Push your code to trigger the CI pipeline
