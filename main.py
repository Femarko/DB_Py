import psycopg2 as pg
from psycopg2 import sql
import config
database = config.database
user = config.user
password = config.password
names_of_tables = config.names_of_tables

conn = pg.connect(database=database, user=user, password=password)

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
def insert_new_client(cursor, name, patronymic, sirname, email, phone=None):
    cursor.execute('''
        INSERT INTO client_name (name, patronymic, sirname, email)
        VALUES (%s, %s, %s, %s) RETURNING id
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
    if name is not None:
        cursor.execute('''
            UPDATE client_name
            SET name = %s
            WHERE id=%s;''', (name, id))
    if patronymic is not None:
        cursor.execute('''
            UPDATE client_name
            SET patronymic = %s
            WHERE id = %s;''', (patronymic, id))
    if sirname is not None:
        cursor.execute('''
            UPDATE client_name
            SET sirname = %s
            WHERE id = %s;''', (sirname, id))
    if email is not None:
        cursor.execute('''
            UPDATE client_name
            SET email = %s
            WHERE id = %s;''', (email, id))

# 5. Функция, позволяющая удалить телефон для существующего клиента
def delete_phone_number(cursor, client_id):
    cursor.execute('''
                SELECT id FROM client_name; 
            ''')
    res = cursor.fetchall()
    res_list = []
    for element in res:
        res_list.append(element[0])

    if client_id not in res_list:
        print('Wrong id!')
    else:
        cursor.execute('''
            DELETE FROM phone WHERE phone.client_id = %s;    
        ''', (client_id,))

# 6. Функция, позволяющая удалить существующего клиента
def delete_client(cursor, client_id):
    cursor.execute('''
                    SELECT id FROM client_name; 
                ''')
    res = cursor.fetchall()
    res_list = []
    for element in res:
        res_list.append(element[0])
    if client_id not in res_list:
        print('Wrong id!')
    else:
        cursor.execute('''
            DELETE FROM client_name WHERE id = %s;    
        ''', (client_id,))

# 7. Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону
def find_client(cursor, id=None, name=None, patronymic=None, sirname=None, email=None, phone_number=None):
    client_name_data = {
        'client_name':{
            'id': id,
            'name': name,
            'patronymic': patronymic,
            'sirname': sirname,
            'email': email,
        },
        'phone_number': phone_number
    }
    if phone_number is None:
        for key, value in client_name_data['client_name'].items():
            if value is not None:
                query = sql.SQL('''
                    SELECT
                        id,
                        name,
                        patronymic,
                        sirname,
                        email
                    FROM {table_name}
                    ''').format(
                    table_name=sql.Identifier('client_name'),
                )
                cursor.execute(query, (str(value),))
    else:
        query = sql.SQL('''
            SELECT
                client_name.id,
                client_name.name,
                client_name.patronymic,
                client_name.sirname,
                client_name.email
            FROM client_name
            JOIN phone ON client_name.id = phone.client_id
            WHERE phone.phone_number = %s
        ''')
        cursor.execute(query, (phone_number,))
    return cursor.fetchall()


with conn.cursor() as cur:
    print(find_client(cur, name='Sergey'))
    conn.commit()

conn.close()

