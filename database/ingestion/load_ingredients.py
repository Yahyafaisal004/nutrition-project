import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="/Users/yahyafaisal/Library/recipe_nutrition_system/backend/.env")

DB_CONFIG = {
    "host": os.getenv("host"),
    "user": os.getenv("user"),
    "password": os.getenv("password"),
    "database": os.getenv("database"),
}

CSV_PATH = "ingredients.csv"

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

df = pd.read_csv(CSV_PATH)

df.columns = df.columns.str.strip()

name_col = "food"

nutrient_cols = [
    c for c in df.columns
    if not c.startswith("Unnamed") and c != name_col
]


def infer_unit(nutrient_name):
    name = nutrient_name.lower()
    if "caloric" in name:
        return "kcal"
    elif "vitamin" in name or "calcium" in name or "iron" in name:
        return "mg"
    elif "water" in name:
        return "g"
    else:
        return "g"

def get_or_create_nutrient(name):
    cursor.execute("SELECT id FROM nutrients WHERE name = %s", (name,))
    res = cursor.fetchone()

    if res:
        return res[0]

    unit = infer_unit(name)
    cursor.execute(
        "INSERT INTO nutrients (name, unit) VALUES (%s, %s)",
        (name, unit)
    )
    return cursor.lastrowid

def get_or_create_ingredient(name):
    cursor.execute("SELECT id FROM ingredients WHERE name = %s", (name,))
    res = cursor.fetchone()

    if res:
        return res[0]

    cursor.execute(
        "INSERT INTO ingredients (name) VALUES (%s)",
        (name,)
    )
    return cursor.lastrowid

print("Inserting nutrients...")

nutrient_map = {}
for col in nutrient_cols:
    clean_name = col.strip().title()   
    nutrient_id = get_or_create_nutrient(clean_name)
    nutrient_map[col] = nutrient_id 

print("Inserting ingredients and mappings...")

for _, row in df.iterrows():

    if pd.isna(row[name_col]) or not str(row[name_col]).strip():
        continue

    food_name = str(row[name_col]).strip()
    ingredient_id = get_or_create_ingredient(food_name)

    for col in nutrient_cols:
        value = row[col]

        if pd.isna(value):
            continue

        nutrient_id = nutrient_map[col]

        cursor.execute("""
            INSERT INTO ingredient_nutrients 
            (ingredient_id, nutrient_id, value_per_100g)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE value_per_100g = VALUES(value_per_100g)
        """, (ingredient_id, nutrient_id, float(value)))

conn.commit()

print("Done! Data inserted successfully.")

cursor.close()
conn.close()