import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor


def create_connection():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"],
        sslmode=st.secrets["postgres"]["sslmode"]
    )


def add_student(name, score):
    query = """
        INSERT INTO students (name, score)
        VALUES (%s, %s);
    """

    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (name, score))


def get_students():
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


def get_student(name):
    query = """
        SELECT id, name, score
        FROM students
        WHERE name ILIKE %s
        ORDER BY id;
    """

    with create_connection() as connection:
        with connection.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:
            cursor.execute(query, (f"%{name}%",))
            return cursor.fetchall()
