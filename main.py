import psycopg2 as pg
import config
database = config.database
user = config.user
password = config.password
names_of_tables = config.names_of_tables

conn = pg.connect(database=database, user=user, password=password)

# def delete_all_tables(names_of_tables):
#     '''удаляет таблицы из списка имен таблиц в обратном порядке'''
#     for name in reversed(names_of_tables):
#         with conn.cursor() as cur:
#             cur.execute('DROP TABLE' + )
#
# delete_all_tables(names_of_tables)

name = 'Ivan'

def get_smth(cur, name: str) -> int:
    cur.execute("""
    SELECT id FROM client_name WHERE name=%s;
    """, (name,))
    return cur.fetchone()

with conn.cursor() as cur:


# python_id = get_course_id(cur, 'Python')
# print('python_id', python_id)

    print(get_smth(cur, name))

conn.close()

# with conn.cursor() as cur:
#
#
#
#     def create_tablles(**tables_params):
#         list_of_names = []
#         list_of_columns = []
#         for key, value in tables_params:
#             list_of_names.append(key)
#             list_of_columns.append(value)
#         cur.execute('''
#         DROP TABLE IF EXISTS name=%s;
#         DROP TABLE IF EXISTS client_name;
#         ''')
#         cur.execute('''
#                     CREATE TABLE IF NOT EXISTS client_name(
#                     id SERIAL PRIMARY KEY,
#                     name VARCHAR(120) NOT NULL,
#                     patronymic VARCHAR(120) NOT NULL,
#                     sirname VARCHAR(120) NOT NULL,
#                     email VARCHAR(50) UNIQUE NOT NULL);
#                     ''')
#         cur.execute('''
#                     CREATE TABLE IF NOT EXISTS phone(
#                     id SERIAL PRIMARY KEY,
#                     client_id INTEGER NOT NULL REFERENCES client_name(id),
#                     phone_number INTEGER);
#                     ''')
#     conn.commit()

