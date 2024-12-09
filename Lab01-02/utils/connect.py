import psycopg2
from utils.config import load_config


def connect():
    config = load_config()
    try:
        with psycopg2.connect(**config) as connect:
            print("Connected to PostgreSQL server.")
            return connect
    except (psycopg2.OperationalError, Exception) as error:
        print(error)
