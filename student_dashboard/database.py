import psycopg2
from psycopg2.extras import RealDictCursor

from config import DB_CONFIG


def create_connection():
    """PostgreSQL database bağlantısı yaradır."""
    return psycopg2.connect(**DB_CONFIG)


def add_student(name, score):
    """Database-ə yeni tələbə əlavə edir."""
    query = """
        INSERT INTO students (name, score)
        VALUES (%s, %s);
    """

    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (name, score))


def get_students():
    """Bütün tələbələri database-dən qaytarır."""
    query = """
        SELECT id, name, score
        FROM students
        ORDER BY id;
    """

    with create_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()


def get_student(name):
    """Ada görə tələbələri axtarır."""
    query = """
        SELECT id, name, score
        FROM students
        WHERE name ILIKE %s
        ORDER BY id;
    """

    with create_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (f"%{name}%",))
            return cursor.fetchall()