from fastapi import APIRouter, Query
from app.database.db import get_connection

router = APIRouter()

@router.get("/search")
def search_ingredients(q: str = Query(..., min_length=1), limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = f"""
        SELECT id, name
        FROM ingredients
        WHERE name LIKE %s
        ORDER BY name
        LIMIT {limit}
    """

    cursor.execute(query, (q + "%",))
    
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results