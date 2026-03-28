from pydantic import BaseModel


class PredictionRequest(BaseModel):
    Time_spent_Alone: float
    Social_event_attendance: float
    Going_outside: float
    Friends_circle_size: float
    Post_frequency: float
    Stage_fear: str
    Drained_after_socializing: str


class PredictionResponse(BaseModel):
    prediction: str