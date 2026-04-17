import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="/Users/yahyafaisal/Library/recipe_nutrition_system/backend/.env")

DB_CONFIG = {
    "host": os.getenv("host"),
    "user": os.getenv("user"),
    "password": os.getenv("password"),
    "database": os.getenv("database"),
}

conn = mysql.connector.connect(**DB_CONFIG)

cursor = conn.cursor()

df = pd.read_csv("dishes.csv")
df.columns = df.columns.str.strip()

name_col = "food_name"

COLUMN_MAPPING = {
    "energy_kcal": "Caloric Value",
    "carb_g": "Carbohydrates",
    "protein_g": "Protein",
    "fat_g": "Fat",
    "fibre_g": "Dietary Fiber",
    "calcium_mg": "Calcium",
    "iron_mg": "Iron",
    "sodium_mg": "Sodium",
    "potassium_mg": "Potassium",
    "vitc_mg": "Vitamin C"
}

def get_nutrient_id(name):
    cursor.execute("SELECT id FROM nutrients WHERE name=%s", (name,))
    res = cursor.fetchone()
    return res[0] if res else None

def get_or_create_dish(name):
    cursor.execute("SELECT id FROM dishes WHERE name=%s", (name,))
    res = cursor.fetchone()
    if res:
        return res[0]

    cursor.execute("INSERT INTO dishes (name) VALUES (%s)", (name,))
    return cursor.lastrowid

for _, row in df.iterrows():
    if pd.isna(row[name_col]):
        continue

    dish_name = str(row[name_col]).strip()
    dish_id = get_or_create_dish(dish_name)

    for col, nutrient_name in COLUMN_MAPPING.items():
        if col not in df.columns:
            continue

        value = row[col]
        if pd.isna(value):
            continue

        nutrient_id = get_nutrient_id(nutrient_name)
        if not nutrient_id:
            continue

        cursor.execute("""
            INSERT INTO dish_nutrients
            (dish_id, nutrient_id, value_per_100g)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE value_per_100g = VALUES(value_per_100g)
        """, (dish_id, nutrient_id, float(value)))

conn.commit()
cursor.close()
conn.close()

print("Dishes loaded successfully")