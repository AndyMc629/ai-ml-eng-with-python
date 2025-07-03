import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import os

# Set MLflow tracking URI
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Prepare some dummy data for a text classification model
X = np.array(["This is a great movie", "This movie was terrible", "I loved the acting", "The plot was boring", "Fantastic performance", "What a waste of time"])
y = np.array([1, 0, 1, 0, 1, 0]) # 1 for positive, 0 for negative

# Simple text vectorization (for demonstration purposes)
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.3, random_state=42)

# Train a simple sentiment classifier
with mlflow.start_run(run_name="Sentiment_Classifier_Training") as run:
    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    mlflow.log_param("solver", "lbfgs")
    mlflow.log_metric("accuracy", accuracy)

    # Log the model
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="sentiment_model",
        registered_model_name="sentiment_classifier",
        input_example=X[0],
        signature=mlflow.models.infer_signature(X_vectorized, model.predict(X_vectorized))
    )

    print(f"Model trained with accuracy: {accuracy}")
    print(f"Model saved to MLflow as 'sentiment_classifier' with run ID: {run.info.run_id}")

# To make sure the model can be loaded, let's also save the vectorizer
import joblib
joblib.dump(vectorizer, "vectorizer.pkl")
mlflow.log_artifact("vectorizer.pkl")
os.remove("vectorizer.pkl")
