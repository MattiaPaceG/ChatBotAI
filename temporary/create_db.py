import sqlite3
import pandas as pd

def create_database():

    products_df = pd.read_excel("products.xlsx")
    products_to_add = list(products_df.itertuples(index=False, name=None))

    conn = sqlite3.connect('../products.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    image_url TEXT NOT NULL,
                    description TEXT NOT NULL,
                    full_description TEXT NOT NULL)''')

    cursor.executemany('INSERT INTO products (name, price, image_url, description, full_description) VALUES (?, ?, ?, ?, ?)', products_to_add)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()