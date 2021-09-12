# imports - standard imports
import os
import json
import sqlite3

# imports - third party imports
from flask import Flask, url_for, request, redirect
from flask import render_template as render

# global constants
DATABASE_NAME = 'inventory.sqlite'

# setting up Flask instance
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'database', DATABASE_NAME),
)

# listing views
link = {x: x for x in ["location", "product", "movement"]}
link["index"] = '/'


def init_database():
    db = sqlite3.connect(DATABASE_NAME)
    cursor = db.cursor()

    # initialize page content
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(prod_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prod_name TEXT UNIQUE NOT NULL,
                    prod_quantity INTEGER NOT NULL,
                    unallocated_quantity INTEGER);
    """)
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS default_prod_qty_to_unalloc_qty
                    AFTER INSERT ON products
                    FOR EACH ROW
                    WHEN NEW.unallocated_quantity IS NULL
                    BEGIN 
                        UPDATE products SET unallocated_quantity  = NEW.prod_quantity WHERE rowid = NEW.rowid;
                    END;

    """)

    # initialize page content
    cursor.execute
    ("""
    CREATE TABLE IF NOT EXISTS location(loc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 loc_name TEXT UNIQUE NOT NULL);
    """)

     # initialize page content
    cursor.execute
    ("""
    CREATE TABLE IF NOT EXISTS logistics(trans_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                prod_id INTEGER NOT NULL,
                                from_loc_id INTEGER NULL,
                                to_loc_id INTEGER NULL,
                                prod_quantity INTEGER NOT NULL,
                                trans_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY(prod_id) REFERENCES products(prod_id),
                                FOREIGN KEY(from_loc_id) REFERENCES location(loc_id),
                                FOREIGN KEY(to_loc_id) REFERENCES location(loc_id));
    """)
    db.commit()


@app.route('/')
def summary():
    init_database()
    msg = None
    q_data, warehouse, products = None, None, None
    db = sqlite3.connect(DATABASE_NAME)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM location") 
        warehouse = cursor.fetchall()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.execute("""
        SELECT prod_name, unallocated_quantity, prod_quantity FROM products
        """)
        q_data = cursor.fetchall()
    except sqlite3.Error as e:
        msg = f"An error occurred: {e.args[0]}"
    if msg:
        print(msg)

    return render('index.html', link=link, title="Summary", warehouses=warehouse, products=products, database=q_data)