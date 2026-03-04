from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Load model
model = joblib.load("models/calorie_model.pkl")

app = FastAPI()

# Request format
class UserInput(BaseModel):
    age: int
    weight: float
    height: float
    gender: str
    activity: str
    goal: str


@app.get("/")
def home():
    return {"message": "AI Nutrition API is Running"}


@app.post("/predict")
def predict(data: UserInput):

    input_data = pd.DataFrame([{
        "Age": data.age,
        "Weight": data.weight,
        "Height": data.height,
        "Gender": data.gender,
        "Activity": data.activity,
        "Goal": data.goal
    }])

    input_data = pd.get_dummies(input_data)

    training_columns = model.feature_names_in_

    for col in training_columns:
        if col not in input_data.columns:
            input_data[col] = 0

    input_data = input_data[training_columns]

    prediction = model.predict(input_data)

    calories, protein, carbs, fat = prediction[0]

    return {
        "calories": round(float(calories), 2),
        "protein": round(float(protein), 2),
        "carbs": round(float(carbs), 2),
        "fat": round(float(fat), 2)
    }