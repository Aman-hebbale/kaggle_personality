from fastapi import FastAPI
from schema import PredictionRequest, PredictionResponse
from model import predict

app = FastAPI(title="Personality Classifier API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict_endpoint(request: PredictionRequest):
    result = predict(request)
    return PredictionResponse(prediction=result)