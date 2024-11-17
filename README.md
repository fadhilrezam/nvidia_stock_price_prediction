# NVIDIA Stock Price Prediction Project

## 📋 Table of Contents
- [About Project](#about-project)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Pipeline](#pipeline)
- [Development](#development)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)

## 🎯 About Project
This project implements an end-to-end machine learning pipeline for NVIDIA stock price prediction, incorporating data ingestion, processing, model training, and deployment with MLOps practices.

## 📁 Project Structure
```
NVIDIA_STOCK_PRICE_PREDICTION/
├── devcontainer/           # Development container configuration
├── backend/                # Flask API implementation
├── data/
│   ├── models/             # Trained model artifacts
│   ├── processed/          # Processed dataset 
│   ├── raw/                # Raw dataset
│   └── visualizations/     # Generated visualizations
├── frontend/               # Streamlit web application
├── logs/                   # Application logs
├── mlruns/                 # MLflow experiment tracking
├── notebook/               # Jupyter notebooks for analysis, research and testing
├── pipeline/               # Main folder for training pipeline
├── utils/                  # Utility functions
├── .gitignore
├── README.md
└── requirements.txt        # Project dependencies
```

## 🚀 Getting Started

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Pipeline
The entire pipeline can be executed from the root directory using:
```bash
python -m pipeline.main
```

This command triggers the following sequential processes:
1. Data Ingestion: Fetches NVIDIA stock data
2. Data Preprocessing: Cleans and prepares the data
3. Feature Engineering: Creates relevant features
4. Model Training: Trains the ARIMA model
5. Model Evaluation: Computes performance metrics
6. MLOps Integration: Handles model versioning and tracking via MLflow

## 🔄 Pipeline Details
The pipeline module (`pipeline/main.py`) orchestrates all data science stages:

```python
pipeline/
├── __init__.py
├── main.py              # Main pipeline orchestrator
├── data_ingestion.py    # Data collection process
├── data_preprocess.py   # Data cleaning, preparation and features engineering
├── train_model.py       # Model training and evaluation with MLflow integration
```

## 👨‍💻 Development

### MLOps Setup
The project utilizes MLflow for experiment tracking and model versioning:
- Training runs are automatically logged
- Model metrics and artifacts are stored
- Version control through MLflow model registry

```bash
# Access MLflow UI
mlflow ui
```

### Logging
- All pipeline processes are logged in `logs/`
- Log format includes timestamp, level, and process details

## 🌐 Deployment

### Backend (Flask)
Available endpoints:
- GET `/`: Get close price predictions


### Frontend (Streamlit)
Features include:
- Prediction input form (date range)
- Prediction results display (dataframe and line chart)

### Live Demo
The application is deployed and can be accessed at:
- 🔗 [NVIDIA Stock Price Prediction App](https://nvidiastockprediction.streamlit.app/)

## 📚 API Documentation

### Base URL
```
http://localhost:5000
```

### Available Endpoints

#### Health Check
```bash
GET /health
```
Simple endpoint to check if the API is running.

#### Stock Price Prediction
```bash
GET /?start_date=2024-10-05&end_date=2024-10-13
```

Parameters:
- `start_date`: Start date for prediction (YYYY-MM-DD)
- `end_date`: End date for prediction (YYYY-MM-DD)

Example Response:
```json
{
    "2024-10-05": {
        "close_pred_original_scale": 852.75
    },
    "2024-10-06": {
        "close_pred_original_scale": 855.32
    }
}
```

Common Errors:
- Start date must be after 2024-10-04
- End date must be after start date

Note: The API returns NVIDIA stock price predictions for business days only, using our trained ARIMA model.