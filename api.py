from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

app = FastAPI()


# -----------------------------
# ROOT ENDPOINT (TEST)
# -----------------------------
@app.get("/")
def read_root():
    return {"message": "AI Nutrition API Running Successfully 🚀"}


# -----------------------------
# USER INPUT MODEL
# -----------------------------
class UserInput(BaseModel):
    age: int
    weight: float   # in kg
    height: float   # in cm
    goal: Literal["weight_loss", "weight_gain", "maintain"]
    diet_type: Literal["veg", "nonveg"]
    activity_level: Literal["low", "moderate", "high"]


# -----------------------------
# CALORIE CALCULATION LOGIC
# -----------------------------
def calculate_calories(weight, height, age, goal, activity_level):
    # Basic BMR formula (Mifflin-St Jeor simplified for demo)
    bmr = 10 * weight + 6.25 * height - 5 * age + 5

    # Activity multiplier
    if activity_level == "low":
        bmr *= 1.2
    elif activity_level == "moderate":
        bmr *= 1.55
    elif activity_level == "high":
        bmr *= 1.9

    # Goal adjustment
    if goal == "weight_loss":
        return bmr - 400
    elif goal == "weight_gain":
        return bmr + 400
    else:
        return bmr


# -----------------------------
# DIET PLAN GENERATOR
# -----------------------------
def generate_diet(calories, diet_type, goal):
    
    if diet_type == "veg":
        if goal == "weight_loss":
            return {
                "breakfast": "Oats with fruits + Green tea",
                "lunch": "Brown rice + Dal + Mixed vegetables",
                "dinner": "2 Chapati + Vegetable curry",
                "snacks": "Nuts + Sprouts salad"
            }
        elif goal == "weight_gain":
            return {
                "breakfast": "Peanut butter toast + Banana + Milk",
                "lunch": "Rice + Dal + Paneer curry",
                "dinner": "Chapati + Soya chunks curry",
                "snacks": "Smoothie + Dry fruits"
            }
        else:
            return {
                "breakfast": "Idli/Dosa + Coconut chutney",
                "lunch": "Rice + Dal + Vegetables",
                "dinner": "Chapati + Paneer curry",
                "snacks": "Fruits + Nuts"
            }

    else:  # Non-veg
        if goal == "weight_loss":
            return {
                "breakfast": "Boiled eggs + Toast",
                "lunch": "Grilled chicken + Vegetables",
                "dinner": "2 Chapati + Egg curry",
                "snacks": "Boiled eggs + Fruits"
            }
        elif goal == "weight_gain":
            return {
                "breakfast": "Omelette + Peanut butter toast + Milk",
                "lunch": "Rice + Chicken curry",
                "dinner": "Chapati + Fish curry",
                "snacks": "Protein smoothie + Nuts"
            }
        else:
            return {
                "breakfast": "Eggs + Toast",
                "lunch": "Rice + Chicken + Vegetables",
                "dinner": "Chapati + Fish curry",
                "snacks": "Fruits + Boiled eggs"
            }


# -----------------------------
# MAIN ENDPOINT
# -----------------------------
@app.post("/generate-plan")
def generate_plan(user: UserInput):

    calories = calculate_calories(
        user.weight,
        user.height,
        user.age,
        user.goal,
        user.activity_level
    )

    diet = generate_diet(
        calories,
        user.diet_type,
        user.goal
    )

    return {
        "user_details": user,
        "recommended_calories_per_day": round(calories),
        "diet_plan": diet,
        "note": "This is a general recommendation. Consult a professional for medical advice."
    }