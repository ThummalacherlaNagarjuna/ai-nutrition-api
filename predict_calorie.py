import pandas as pd
import joblib

# -----------------------------
# 1. Load Saved Model
# -----------------------------
model = joblib.load("models/calorie_model.pkl")

# -----------------------------
# 2. Take User Input Dynamically
# -----------------------------
print("===== Enter Your Details =====")

age = int(input("Enter Age: "))
weight = float(input("Enter Weight (kg): "))
height = float(input("Enter Height (cm): "))
gender = input("Enter Gender (Male/Female): ")
activity = input("Enter Activity Level (Sedentary/Light/Moderate/Active/Very Active): ")
goal = input("Enter Goal (Loss/Maintain/Gain): ")

# -----------------------------
# 3. Convert Input to DataFrame
# -----------------------------
input_data = pd.DataFrame([{
    "Age": age,
    "Weight": weight,
    "Height": height,
    "Gender": gender,
    "Activity": activity,
    "Goal": goal
}])

# -----------------------------
# 4. Apply Same Encoding
# -----------------------------
input_data = pd.get_dummies(input_data)

training_columns = model.feature_names_in_

for col in training_columns:
    if col not in input_data.columns:
        input_data[col] = 0

input_data = input_data[training_columns]

# -----------------------------
# 5. Predict
# -----------------------------
prediction = model.predict(input_data)

calories, protein, carbs, fat = prediction[0]

print("\n===== Your Personalized Diet Plan =====")
print(f"Calories : {round(calories)} kcal")
print(f"Protein  : {round(protein)} g")
print(f"Carbs    : {round(carbs)} g")
print(f"Fat      : {round(fat)} g")