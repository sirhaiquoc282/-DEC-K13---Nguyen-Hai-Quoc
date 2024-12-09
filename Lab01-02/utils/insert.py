import psycopg2
from utils.queries import insert_products
import os
import json


def get_files_path(dir):
    return [
        os.path.join(dir, file) for file in os.listdir(dir) if file.endswith(".json")
    ]


def log(message, error=False):
    log_dir = "./log"
    log_file_path = os.path.join(log_dir, "info.log")

    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        with open(log_file_path, "a") as log_file:
            if not error:
                log_file.write(message + " status: Success\n")
            else:
                log_file.write(message + " status: Fail\n")
    except Exception as err:
        print(err)


def insert_products_data(conn, dir):
    try:
        file_paths = get_files_path(dir)
        count = 0
        for path in file_paths:
            with conn.cursor() as cur:
                try:
                    with open(path, "r") as file:
                        json_data = json.load(file)
                        valid_data = []
                        for product in json_data:
                            valid_data.append(
                                (
                                    product["id"],
                                    product["name"],
                                    product["url_key"],
                                    product["price"],
                                    product["description"],
                                    json.dumps(product["images_url"]),
                                )
                            )
                        cur.executemany(insert_products, valid_data)
                        count += 1
                except (Exception, psycopg2.DatabaseError) as err:
                    conn.rollback()
                    log(err, error=True)
                    print(err)
                except (Exception, psycopg2.IntegrityError) as err:
                    conn.rollback()
                    log(err, error=True)
                    print(err)
            conn.commit()
            print(f"Complete: {path}")
            log(path)
    except (Exception, psycopg2.DatabaseError) as err:
        log(err, error=True)
        print(err)
    finally:
        print(count)
