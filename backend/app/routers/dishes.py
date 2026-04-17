from fastapi import APIRouter, Query
from app.database.db import get_connection

router = APIRouter()

@router.get("/search")
def search_dishes(q: str = Query(..., min_length=1), limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id, name
        FROM dishes
        WHERE name LIKE %s
        ORDER BY name
        LIMIT %s
    """

    cursor.execute(query, (q + "%", limit))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results