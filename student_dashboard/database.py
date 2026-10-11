import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor


def create_connection():
    """Neon PostgreSQL database-ə bağlantı yaradır."""
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"],
        sslmode=st.secrets["postgres"]["sslmode"]
    )


def get_students():
    """Bütün tələbələri database-dən əldə edir."""
    query = """
        SELECT id, name, score
        FROM students
        ORDER BY id;
    """

    with create_connection() as connection:
        with connection.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:
            cursor.execute(query)
            return cursor.fetchall()
