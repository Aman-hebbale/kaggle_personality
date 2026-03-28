import joblib
import pandas as pd

pipeline = joblib.load('./artifacts/pipeline.pkl')

def predict(request):
    data = pd.DataFrame([{
        'Time_spent_Alone': request.Time_spent_Alone,
        'Social_event_attendance': request.Social_event_attendance,
        'Going_outside': request.Going_outside,
        'Friends_circle_size': request.Friends_circle_size,
        'Post_frequency': request.Post_frequency,
        'Stage_fear': request.Stage_fear,
        'Drained_after_socializing': request.Drained_after_socializing
    }])

    prediction = pipeline.predict(data)
    return prediction[0]