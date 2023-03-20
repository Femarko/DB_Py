import psycopg2 as pg
import config
database = config.database
user = config.user
password = config.password
names_of_tables = config.names_of_tables

conn = pg.connect(database=database, user=user, password=password)


def delete_relations():
    cur.execute('''
        DROP TABLE phone;
        DROP TABLE client_name;
    ''')
    conn.commit()

def create_relations():
    cur.execute('''                    
        CREATE TABLE IF NOT EXISTS client_name(
        id SERIAL PRIMARY KEY,
        name VARCHAR(120) NOT NULL,
        patronymic VARCHAR(120) NOT NULL,
        sirname VARCHAR(120) NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL);
        ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS phone(
        id SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL REFERENCES client_name(id),
        phone_number INTEGER);
        ''')
    conn.commit()


with conn.cursor() as cur:
    create_relations()


conn.close()

