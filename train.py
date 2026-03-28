import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


NUMERIC_COLS = [
    'Time_spent_Alone',
    'Social_event_attendance',
    'Going_outside',
    'Friends_circle_size',
    'Post_frequency'
]

CATEGORICAL_COLS = [
    'Stage_fear',
    'Drained_after_socializing'
]

TARGET = 'Personality'
DATA_PATH = './data/personality_dataset.csv'
MODEL_PATH = './artifacts/pipeline.pkl'


def load_data(path):
    df = pd.read_csv(path)
    X = df.drop(columns=[TARGET])
    y = df[TARGET]
    return X, y


def build_preprocessor():
    numeric_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer([
        ('num', numeric_transformer, NUMERIC_COLS),
        ('cat', categorical_transformer, CATEGORICAL_COLS)
    ])

    return preprocessor


def train(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline = Pipeline([
        ('preprocessor', build_preprocessor()),
        ('model', LogisticRegression(random_state=42, max_iter=1000))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
    print(f"CV Mean: {cv_scores.mean():.4f}, Std: {cv_scores.std():.4f}")

    return pipeline


def main():
    print("Loading data...")
    X, y = load_data(DATA_PATH)

    print("Training pipeline...")
    pipeline = train(X, y)

    print("Saving pipeline...")
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Pipeline saved to {MODEL_PATH}")


if __name__ == '__main__':
    main()
#claude --resume 73f5a786-b9aa-4ec5-9ce3-0c5ab30c3aff