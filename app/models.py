import sqlite3
from config import Config

def conectar_bd():
    return sqlite3.connect(Config.DATABASE)
