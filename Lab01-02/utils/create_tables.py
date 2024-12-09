import psycopg2
from utils.queries import create_products


def create_tables(conn):
    try:
        with conn.cursor() as cur:
            cur.execute(create_products)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as err:
        print(err)
        if conn:
            conn.rollback()
