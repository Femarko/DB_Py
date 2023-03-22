import psycopg2 as pg
import config
database = config.database
user = config.user
password = config.password
names_of_tables = config.names_of_tables

conn = pg.connect(database=database, user=user, password=password)

# # Функция, удаляющая таблицы
# def delete_relation(relation):
#     cur.execute('''DROP TABLE %s;''')
#     conn.commit()

# 1. Функция, создающая структуру БД (таблицы)
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
        phone_number VARCHAR(12));
        ''')
    conn.commit()

# 2. Функция, позволяющая добавить нового клиента
def insert_new_client(cursor, name, patronymic, sirname, email):
    cursor.execute('''
        INSERT INTO client_name (name, patronymic, sirname, email)
        VALUES (%s, %s, %s, %s)
    ''', (name, patronymic, sirname, email))
    conn.commit()

# 3. Функция, позволяющая добавить телефон для существующего клиента
def insert_phone(cursor, client_id, phone_number):
    cursor.execute('''
        INSERT INTO phone (client_id, phone_number)
        VALUES (%s, %s)
        ''', (client_id, phone_number))
    conn.commit()

# 4. Функция, позволяющая изменить данные о клиенте
def client_data_update(cursor, id, name=None, patronymic=None, sirname=None, email=None):
    column_s_list = [name, patronymic, sirname, email]
    cursor.execute('''
        UPDATE Client
        SET сюда можно будет указать любой параметр, например name, остальные останутся прежние.
        WHERE client_id=client_id;''', (*column_s_list, id,))




with conn.cursor() as cur:
    insert_phone(cur, '1', '79169053323')

    conn.commit()

    # create_relations()



conn.close()

