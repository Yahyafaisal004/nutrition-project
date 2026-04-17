from fastapi import APIRouter
from app.database.db import get_connection

router = APIRouter()


@router.get("")
def list_nutrients():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, name, unit
        FROM nutrients
        ORDER BY name
        """
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
