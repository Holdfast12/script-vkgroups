import config
import sqlite3
import requests
import time

con = sqlite3.connect("base.db")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS messages")
cur.execute("""CREATE TABLE IF NOT EXISTS messages (
id TEXT,
nickname TEXT,
firstName TEXT,
lastName TEXT,
message TEXT
)""")
cur.execute("DROP TABLE IF EXISTS services")
cur.execute("""CREATE TABLE IF NOT EXISTS services (
id INTEGER PRIMARY KEY AUTOINCREMENT,
serviceName TEXT,
serviceDuration INTEGER,
servicePrice TEXT,
serviceDescription TEXT
)""")
con.close()

class Client:
    def __init__(self, vkid, firstname, lastname, phone, groups):
        self.vkid = vkid
