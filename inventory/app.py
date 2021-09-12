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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS location(loc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 loc_name TEXT UNIQUE NOT NULL);
    """)