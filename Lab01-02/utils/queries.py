create_products = """CREATE TABLE IF NOT EXISTS products(
                            product_id INT PRIMARY KEY,
                            name TEXT NOT NULL,
                            url_key TEXT,
                            price DECIMAL(20),
                            description TEXT,
                            images_url JSON)"""


insert_products = """
    INSERT INTO products (product_id, name, url_key, price, description, images_url)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING product_id;
"""
