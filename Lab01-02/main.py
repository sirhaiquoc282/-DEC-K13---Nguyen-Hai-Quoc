from utils.create_tables import create_tables
from utils.insert import insert_products_data
from utils.connect import connect

if __name__ == "__main__":
    direction = "./../Projects02/Pre_processed_data/"
    conn = connect()
    create_tables(conn)
    insert_products_data(conn, direction)
    conn.close()
