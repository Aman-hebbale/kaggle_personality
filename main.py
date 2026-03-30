from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from schema import PredictionRequest, PredictionResponse
from model import predict
from database import SessionLocal, PredictionLog, APIKey, init_db, get_db
from security import verify_api_key
import os
from dotenv import load_dotenv

app = FastAPI(title="Personality Classifier API")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.on_event("startup")
def startup():
    init_db()
    db = SessionLocal()
    api_key = os.getenv("API_KEY")
    existing_key = db.query(APIKey).filter(APIKey.key == api_key).first()
    if not existing_key:
        db.add(APIKey(key=api_key, owner="admin"))
        db.commit()
    db.close()

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
@limiter.limit("10/minute")
def predict_endpoint(request: Request, body: PredictionRequest, db: Session = Depends(get_db), api_key: APIKey = Depends(verify_api_key)):
    result = predict(body)

    log = PredictionLog(
        time_spent_alone=body.Time_spent_Alone,
        social_event_attendance=body.Social_event_attendance,
        going_outside=body.Going_outside,
        friends_circle_size=body.Friends_circle_size,
        post_frequency=body.Post_frequency,
        stage_fear=body.Stage_fear,
        drained_after_socializing=body.Drained_after_socializing,
        prediction=result
    )

    db.add(log)
    db.commit()

    return PredictionResponse(prediction=result)