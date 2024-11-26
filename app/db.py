# app/db.py

import sqlite3

def conectar_bd():
    return sqlite3.connect('database.db')
