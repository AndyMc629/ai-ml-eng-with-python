# Image Analysis Application

This project provides a web application for image analysis, featuring:
- Image upload via a React frontend.
- FastAPI backend for processing images using AI models.
- Functionality to explain image details and perform object segmentation.

## Project Structure

```
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── tests/
│       └── unit/
├── frontend/
│   ├── public/
│   ├── src/
│   └── package.json
└── README.md
```

## Getting Started

### Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the FastAPI application:
    ```bash
    uvicorn main:app --reload
    ```

### Frontend Setup

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the React application:
    ```bash
    npm start
    ```

## Features

- **Image Upload:** Users can upload images through a simple interface.
- **Image Explanation:** AI models will generate textual descriptions of the uploaded images.
- **Object Segmentation:** The application will identify and segment different objects, foreground, and background within the images.

## Technologies Used

- **Backend:** FastAPI, Python, Uvicorn, Pillow, (AI/ML Libraries like PyTorch/TensorFlow, Transformers, OpenCV - to be integrated)
- **Frontend:** React, JavaScript, HTML, CSS

## Unit Tests

Comprehensive unit tests are provided for both backend and frontend components to ensure reliability and maintainability.
