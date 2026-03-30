import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from main import app
from database import Base, APIKey, get_db

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=test_engine)

API_KEY = os.getenv("API_KEY")


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    db.add(APIKey(key=API_KEY, owner="admin"))
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=test_engine)


SAMPLE_INPUT = {
    "Time_spent_Alone": 7,
    "Social_event_attendance": 2,
    "Going_outside": 1,
    "Friends_circle_size": 3,
    "Post_frequency": 1,
    "Stage_fear": "Yes",
    "Drained_after_socializing": "Yes"
}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_without_api_key():
    response = client.post("/predict", json=SAMPLE_INPUT)
    assert response.status_code == 401


def test_predict_with_valid_api_key():
    response = client.post(
        "/predict",
        json=SAMPLE_INPUT,
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["prediction"] in ["Introvert", "Extrovert"]


def test_predict_with_invalid_api_key():
    response = client.post(
        "/predict",
        json=SAMPLE_INPUT,
        headers={"X-API-Key": "wrongkey"}
    )
    assert response.status_code == 401


def test_predict_invalid_input():
    response = client.post(
        "/predict",
        json={"Time_spent_Alone": "not_a_number"},
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 422


