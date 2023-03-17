import psycopg2 as pg

conn = pg.connect(database='clients', user='postgres', password='FemarData')

with conn.cursor() as cur:
    cur.execute('CREATE TABLE IF NOT EXISTS name(id SERIAL INTEGER PRIMARY KEY, )')
conn.close()