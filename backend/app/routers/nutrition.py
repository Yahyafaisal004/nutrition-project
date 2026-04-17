from fastapi import APIRouter
from app.database.db import get_connection

router = APIRouter()

@router.post("/ingredients")
def calculate_nutrition(data: dict):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    items = data.get("items", [])
    nutrient_ids = data.get("nutrient_ids", None)

    if not items:
        cursor.close()
        conn.close()
        return {
            "totals": [],
            "by_ingredient": []
        }

    if nutrient_ids == []:
        cursor.close()
        conn.close()
        return {
            "totals": [],
            "by_ingredient": []
        }

    ingredient_ids = [item["id"] for item in items]
    grams_map = {item["id"]: item["grams"] for item in items}

    # Query
    query = """
        SELECT 
            inut.ingredient_id, 
            inut.nutrient_id, 
            inut.value_per_100g,
            n.name AS nutrient_name, 
            n.unit,
            i.name AS ingredient_name
        FROM ingredient_nutrients inut
        JOIN nutrients n ON n.id = inut.nutrient_id
        JOIN ingredients i ON i.id = inut.ingredient_id
        WHERE inut.ingredient_id IN (%s)
    """ % (",".join(["%s"] * len(ingredient_ids)))

    params = ingredient_ids

    if nutrient_ids is not None:
        query += " AND inut.nutrient_id IN (%s)" % (
            ",".join(["%s"] * len(nutrient_ids))
        )
        params += nutrient_ids

    cursor.execute(query, params)
    rows = cursor.fetchall()

    totals = {}
    by_ingredient = {}

    for row in rows:
        ing_id = row["ingredient_id"]
        grams = grams_map[ing_id]
        value = row["value_per_100g"]

        contribution = value * grams / 100
        nid = row["nutrient_id"]

        # ---- TOTALS ----
        if nid not in totals:
            totals[nid] = {
                "nutrient_id": nid,
                "name": row["nutrient_name"],
                "unit": row["unit"],
                "value": 0
            }

        totals[nid]["value"] = round(totals[nid]["value"] + contribution, 3)

        # ---- PER INGREDIENT ----
        if ing_id not in by_ingredient:
            by_ingredient[ing_id] = {
                "ingredient_id": ing_id,
                "name": row["ingredient_name"],
                "grams": grams,
                "nutrients": []
            }

        by_ingredient[ing_id]["nutrients"].append({
            "nutrient_id": nid,
            "name": row["nutrient_name"],
            "unit": row["unit"],
            "value": round(contribution, 3)
        })

    cursor.close()
    conn.close()

    return {
        "totals": list(totals.values()),
        "by_ingredient": list(by_ingredient.values())
    }


@router.post("/dishes")
def calculate_dish_nutrition(data: dict):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    dish_id = data.get("dish_id")
    grams = data.get("grams")
    nutrient_ids = data.get("nutrient_ids", None)

    # Query
    query = """
        SELECT dnut.nutrient_id, dnut.value_per_100g,
               n.name, n.unit
        FROM dish_nutrients dnut
        JOIN nutrients n ON n.id = dnut.nutrient_id
        WHERE dnut.dish_id = %s
    """

    params = [dish_id]

    if nutrient_ids:
        query += " AND dnut.nutrient_id IN (%s)" % (
            ",".join(["%s"] * len(nutrient_ids))
        )
        params += nutrient_ids

    cursor.execute(query, params)
    rows = cursor.fetchall()

    results = []

    for row in rows:
        value = row["value_per_100g"] * grams / 100

        results.append({
            "nutrient_id": row["nutrient_id"],
            "name": row["nutrient_name"],
            "unit": row["unit"],
            "value": round(value, 3)
        })

    cursor.close()
    conn.close()

    return {
        "dish_id": dish_id,
        "grams": grams,
        "nutrients": results
    }
