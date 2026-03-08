# ============================================
# AI NUTRITION PLANNER API
# Developer: Nagarjuna
# Description:
# API for Diet Plan, Nutrition Analysis,
# Workout Plan, Medical Diet, and Food Tracking
# ============================================


# ============================================
# IMPORT LIBRARIES
# ============================================

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import requests
from fastapi import UploadFile, File
import requests



# ============================================
# INITIALIZE FASTAPI
# ============================================

app = FastAPI()
@app.get("/")
def home():
    return {"message": "AI Nutrition API is running"}


# ============================================
# API KEY (USDA FOOD DATA CENTRAL)
# ============================================

API_KEY = "VdZDagozcEq657oP5jvB3kzz6uqUmPUdDwaipnrz"


# ============================================
# DATA MODELS
# ============================================

# Food item for nutrition breakdown
class FoodItem(BaseModel):
    name: str
    quantity: int


# Request model for nutrition breakdown
class NutritionRequest(BaseModel):
    food_items: List[FoodItem]


# Daily food tracker input
class DailyFood(BaseModel):
    food_items: list


# User input for general diet plan
class UserInput(BaseModel):
    age: int
    weight: float
    height: float
    goal: str
    diet_type: str
    activity_level: str
    fitness_level: str


# Medical diet request
class DietRequest(BaseModel):
    age: int
    weight: float
    height: float
    goal: str
    health_conditions: list


# Workout plan request
class WorkoutRequest(BaseModel):
    fitness_level: str
    goal: str


# Food name request
class FoodRequest(BaseModel):
    food_name: str


# ============================================
# CALORIE CALCULATOR
# ============================================

def calculate_calories(weight, height, age, goal, activity_level):

    bmr = 10 * weight + 6.25 * height - 5 * age + 5

    if activity_level == "low":
        bmr *= 1.2
    elif activity_level == "moderate":
        bmr *= 1.55
    else:
        bmr *= 1.9

    if goal == "weight_loss":
        return bmr - 400
    elif goal == "weight_gain":
        return bmr + 400
    else:
        return bmr


# ============================================
# BMI CALCULATOR
# ============================================

def calculate_bmi(weight, height):

    height_m = height / 100
    bmi = weight / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
        score = 60
    elif bmi < 25:
        category = "Normal"
        score = 90
    elif bmi < 30:
        category = "Overweight"
        score = 70
    else:
        category = "Obese"
        score = 50

    return bmi, category, score


# ============================================
# PERFORMANCE SCORE
# ============================================

def calculate_performance_score(bmi, activity_level, goal):

    score = 0

    # BMI score
    if 18.5 <= bmi <= 24.9:
        score += 40
    elif 25 <= bmi <= 29:
        score += 20
    elif bmi < 18.5:
        score += 15
    else:
        score += 10

    # Activity score
    if activity_level == "high":
        score += 30
    elif activity_level == "medium":
        score += 20
    else:
        score += 10

    # Goal score
    if goal in ["weight_loss", "weight_gain", "maintain"]:
        score += 20

    return score


# ============================================
# DIET PLAN GENERATOR
# ============================================

def generate_diet(calories, diet_type):

    if diet_type == "veg":
        diet = {
            "breakfast": "Oats + Fruits + Milk",
            "lunch": "Brown Rice + Dal + Vegetables",
            "dinner": "Chapati + Paneer Curry",
            "snacks": "Nuts + Smoothie"
        }

    else:
        diet = {
            "breakfast": "Eggs + Toast + Milk",
            "lunch": "Rice + Chicken + Vegetables",
            "dinner": "Chapati + Fish/Chicken",
            "snacks": "Boiled Eggs + Fruits"
        }

    return diet


# ============================================
# WORKOUT PLAN GENERATOR
# ============================================

def generate_workout(fitness_level):

    if fitness_level == "beginner":

        workout = {
            "day1": "Light Full Body",
            "day2": "Walking",
            "day3": "Rest",
            "day4": "Bodyweight Exercises",
            "day5": "Stretching",
            "day6": "Light Cardio",
            "day7": "Rest"
        }

    elif fitness_level == "intermediate":

        workout = {
            "day1": "Chest + Triceps",
            "day2": "Back + Biceps",
            "day3": "Legs",
            "day4": "Cardio",
            "day5": "Shoulders + Abs",
            "day6": "HIIT",
            "day7": "Rest"
        }

    else:

        workout = {
            "day1": "Heavy Chest",
            "day2": "Heavy Back",
            "day3": "Leg Day",
            "day4": "HIIT Cardio",
            "day5": "Shoulders + Core",
            "day6": "Functional Training",
            "day7": "Rest"
        }

    return workout


# ============================================
# MAIN DIET PLAN API
# ============================================

@app.post("/generate-plan")
def generate_plan(user: UserInput):

    calories = calculate_calories(
        user.weight,
        user.height,
        user.age,
        user.goal,
        user.activity_level
    )

    bmi, category, score = calculate_bmi(
        user.weight,
        user.height
    )

    diet = generate_diet(
        calories,
        user.diet_type
    )

    workout = generate_workout(user.fitness_level)

    performance_score = calculate_performance_score(
        bmi,
        user.activity_level,
        user.goal
    )

    return {
        "recommended_calories_per_day": round(calories),
        "BMI": round(bmi, 2),
        "BMI_category": category,
        "health_score": score,
        "diet_plan": diet,
        "workout_plan": workout
    }


# ============================================
# NUTRITION BREAKDOWN API
# ============================================

@app.post("/nutrition-breakdown")
def nutrition_breakdown(data: NutritionRequest):

    total_calories = 0
    carbs = 0
    protein = 0
    fat = 0
    fiber = 0
    sugar = 0

    for food in data.food_items:

        query = food.name
        quantity = food.quantity

        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={query}&api_key={API_KEY}"

        response = requests.get(url)

        if response.status_code == 200:

            foods = response.json().get("foods", [])

            if foods:

                nutrients = foods[0]["foodNutrients"]

                for n in nutrients:

                    name = n.get("nutrientName")
                    value = n.get("value", 0)

                    if name == "Energy":
                        total_calories += value * quantity

                    if name == "Carbohydrate, by difference":
                        carbs += value * quantity

                    if name == "Protein":
                        protein += value * quantity

                    if name == "Total lipid (fat)":
                        fat += value * quantity

                    if name == "Fiber, total dietary":
                        fiber += value * quantity

                    if name == "Sugars, total including NLEA":
                        sugar += value * quantity

    return {
        "calories": round(total_calories,2),
        "carbs": round(carbs,2),
        "protein": round(protein,2),
        "fat": round(fat,2),
        "fiber": round(fiber,2),
        "sugar": round(sugar,2)
    }


# ============================================
# MEDICAL DIET API (CONDITION BASED)
# ============================================

def get_nutrition(food):

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "query": food,
        "api_key": API_KEY
    }

    r = requests.get(url, params=params)
    data = r.json()

    calories = protein = carbs = fat = fiber = sugar = 0

    try:

        nutrients = data["foods"][0]["foodNutrients"]

        for n in nutrients:

            name = n.get("nutrientName", "")
            value = n.get("value", 0)

            if name == "Energy":
                calories = value
            elif name == "Protein":
                protein = value
            elif name == "Carbohydrate, by difference":
                carbs = value
            elif name == "Total lipid (fat)":
                fat = value
            elif name == "Fiber, total dietary":
                fiber = value
            elif name == "Sugars, total including NLEA":
                sugar = value

    except:
        pass

    return calories, protein, carbs, fat, fiber, sugar


def generate_medical_diet(conditions):

    breakfast = ["oats", "milk", "egg", "banana"]
    lunch = ["brown rice", "dal", "chicken breast", "spinach"]
    dinner = ["chapati", "paneer", "vegetables"]
    snacks = ["almonds", "yogurt", "apple"]

    if "diabetes" in conditions:
        breakfast.remove("banana")
        snacks.remove("apple")

    if "cholesterol" in conditions:
        breakfast.remove("egg")

    if "thyroid" in conditions:
        lunch.remove("spinach")

    if "weight_loss" in conditions:
        lunch.remove("brown rice")

    return {
        "breakfast": breakfast,
        "lunch": lunch,
        "dinner": dinner,
        "snacks": snacks
    }


@app.post("/medical-diet")
def generate_medical_diet(data: DietRequest):

    bmi = data.weight / ((data.height / 100) ** 2)

    diet = generate_medical_diet(data.health_conditions)

    foods = (
        diet["breakfast"]
        + diet["lunch"]
        + diet["dinner"]
        + diet["snacks"]
    )

    total_calories = protein = carbs = fat = fiber = sugar = 0

    for food in foods:

        c, p, ca, f, fi, s = get_nutrition(food)

        total_calories += c
        protein += p
        carbs += ca
        fat += f
        fiber += fi
        sugar += s

    return {

        "BMI": round(bmi, 2),

        "diet_plan": diet,

        "nutrition_breakdown": {
            "calories": round(total_calories, 2),
            "protein": round(protein, 2),
            "carbs": round(carbs, 2),
            "fat": round(fat, 2),
            "fiber": round(fiber, 2),
            "sugar": round(sugar, 2)
        }

    }


# ============================================
# DAILY FOOD TRACKER
# ============================================

@app.post("/daily-food-tracker")
def daily_food_tracker(data: DailyFood):

    total_calories = 0

    for item in data.food_items:
        total_calories += item.get("calories",0)

    score = min(100, (total_calories / 2500) * 100)

    return {
        "total_calories_consumed": total_calories,
        "recommended_calories": 2500,
        "daily_score": round(score,2)
    }


# ============================================
# WORKOUT PLAN API
# ============================================

@app.post("/workout-plan")
def generate_workout_plan(data: WorkoutRequest):

    fitness = data.fitness_level.lower()
    goal = data.goal.lower()

    workout = {}

    if fitness == "beginner":

        workout = {
            "Day 1": "Full Body Light Workout",
            "Day 2": "Cardio + Walking",
            "Day 3": "Rest",
            "Day 4": "Upper Body Basic",
            "Day 5": "Lower Body Basic",
            "Day 6": "Light Jogging",
            "Day 7": "Rest"
        }

    elif fitness == "intermediate":

        workout = {
            "Day 1": "Chest + Triceps",
            "Day 2": "Back + Biceps",
            "Day 3": "Cardio",
            "Day 4": "Leg Day",
            "Day 5": "Shoulders",
            "Day 6": "Core + Abs",
            "Day 7": "Rest"
        }

    elif fitness == "advanced":

        workout = {
            "Day 1": "Heavy Chest + Triceps",
            "Day 2": "Heavy Back + Biceps",
            "Day 3": "Legs + Squats",
            "Day 4": "HIIT Cardio",
            "Day 5": "Shoulders + Traps",
            "Day 6": "Core + Power Training",
            "Day 7": "Active Recovery"
        }

    return {
        "fitness_level": fitness,
        "goal": goal,
        "workout_plan": workout
    }

# -----------------------------------
# Spoonacular API Key
# -----------------------------------

SPOONACULAR_API_KEY = "eaad0102ee7f41cf8a87312f30812c16"

# -----------------------------------
# IMAGE BASED NUTRITION BREAKDOWN
# -----------------------------------

@app.post("/image-nutrition")
async def image_nutrition(file: UploadFile = File(...)):

    try:

        # Read image
        image_bytes = await file.read()

        url = "https://api.spoonacular.com/food/images/analyze"

        response = requests.post(
            url,
            params={"apiKey": SPOONACULAR_API_KEY},
            files={"file": image_bytes}
        )

        if response.status_code != 200:
            return {
                "error": "Image analysis failed",
                "status_code": response.status_code
            }

        data = response.json()

        category = data.get("category", "Unknown")

        nutrition = data.get("nutrition", {})

        return {

            "detected_food": category,

            "nutrition_breakdown": {
                "calories": nutrition.get("calories"),
                "protein": nutrition.get("protein"),
                "fat": nutrition.get("fat"),
                "carbs": nutrition.get("carbs")
            }

        }

    except Exception as e:

        return {
            "error": str(e)
        }

# -----------------------------
# Manual Food Edit Model
# -----------------------------
class ManualFoodEdit(BaseModel):
    food_name: str
    quantity: int
# --------------------------------------------------
# Manual Food Edit (Real Time Nutrition using USDA)
# --------------------------------------------------

@app.post("/manual-food-edit")
def manual_food_edit(data: ManualFoodEdit):

    query = data.food_name
    quantity = data.quantity

    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={query}&api_key={API_KEY}"

    response = requests.get(url)

    calories = carbs = protein = fat = fiber = sugar = 0

    if response.status_code == 200:

        foods = response.json().get("foods", [])

        if foods:

            nutrients = foods[0]["foodNutrients"]

            for n in nutrients:

                name = n.get("nutrientName")
                value = n.get("value", 0)

                if name == "Energy":
                    calories = value * quantity

                if name == "Carbohydrate, by difference":
                    carbs += value * quantity

                if name == "Protein":
                    protein += value * quantity

                if name == "Total lipid (fat)":
                    fat += value * quantity

                if name == "Fiber, total dietary":
                    fiber += value * quantity

                if name == "Sugars, total including NLEA":
                    sugar += value * quantity

    return {
        "food_name": query,
        "quantity": quantity,
        "nutrition_breakdown": {
            "calories": round(calories,2),
            "carbs": round(carbs,2),
            "protein": round(protein,2),
            "fat": round(fat,2),
            "fiber": round(fiber,2),
            "sugar": round(sugar,2)
        }
    }