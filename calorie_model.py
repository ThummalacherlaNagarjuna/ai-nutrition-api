import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

# -----------------------------
# 1. Generate Synthetic Dataset
# -----------------------------

data = []

for i in range(3000):
    
    age = random.randint(18, 60)
    weight = random.randint(45, 100)
    height = random.randint(150, 190)
    gender = random.choice(['Male', 'Female'])
    activity = random.choice(['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'])
    goal = random.choice(['Loss', 'Maintain', 'Gain'])
    
    # BMR calculation
    if gender == 'Male':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    # Activity multiplier
    activity_dict = {
        'Sedentary': 1.2,
        'Light': 1.375,
        'Moderate': 1.55,
        'Active': 1.725,
        'Very Active': 1.9
    }
    
    calories = bmr * activity_dict[activity]
    
    # Goal adjustment
    if goal == 'Loss':
        calories -= 500
    elif goal == 'Gain':
        calories += 500
    
    # Protein
    if goal == 'Loss':
        protein = weight * 1.5
    elif goal == 'Gain':
        protein = weight * 1.8
    else:
        protein = weight * 1.2
    
    # Fat (30% of calories)
    fat = (0.3 * calories) / 9
    
    # Carbs remaining
    carbs = (calories - (protein * 4 + fat * 9)) / 4
    
    data.append([age, weight, height, gender, activity, goal,
                 calories, protein, carbs, fat])

columns = ['Age', 'Weight', 'Height', 'Gender', 'Activity', 'Goal',
           'Calories', 'Protein', 'Carbs', 'Fat']

df = pd.DataFrame(data, columns=columns)

# -----------------------------
# 2. Encode Categorical Features
# -----------------------------

df = pd.get_dummies(df, columns=['Gender', 'Activity', 'Goal'], drop_first=True)

# -----------------------------
# 3. Split Data
# -----------------------------

X = df.drop(['Calories', 'Protein', 'Carbs', 'Fat'], axis=1)
y = df[['Calories', 'Protein', 'Carbs', 'Fat']]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 4. Train Model
# -----------------------------

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -----------------------------
# 5. Evaluate Model
# -----------------------------

y_pred = model.predict(X_test)

print("R2 Score:", r2_score(y_test, y_pred))
print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))



os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/calorie_model.pkl")

print("Model saved successfully!")