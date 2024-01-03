from db.database import DbShop
import os

db_path = 'DATABASE.db'
db = DbShop()

if not os.path.exists('images'):
    os.makedirs('images')

if not os.path.exists(db_path):
    db.db_path = db_path
    db.db_initialize()
    db.db_check_and_create_tables()
    db.db_close_conn()

db.db_path = db_path
db.db_initialize()
