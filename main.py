import psycopg2
from psycopg2.sql import SQL, Identifier


def create_db(conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS info_client(
            id_client SERIAL PRIMARY KEY,
            first_name VARCHAR(60) NOT NULL,
            last_name VARCHAR(60) NOT NULL,
            e_mail VARCHAR(60) NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS info_phone(
            id_phone SERIAL PRIMARY KEY,
            phone_number VARCHAR(12),
            id_client INTEGER REFERENCES info_client(id_client)     
        )
    """)

def add_client(conn, first_name, last_name, e_mail, phones=None):
    cur.execute("""INSERT INTO info_client(first_name, last_name, e_mail)  VALUES (%s, %s, %s) RETURNING *;
        """, (first_name, last_name, e_mail))
    res = cur.fetchone()
    print(res)

def add_phone(conn, phone_number, id_client):
    cur.execute("""INSERT INTO info_phone(phone_number, id_client) VALUES (%s, %s) RETURNING *;
        """, (phone_number, id_client))
    res = cur.fetchone()
    print(res)

def change_client(conn, id_client, first_name=None, last_name=None, e_mail=None):
    arg_list = {'first_name': first_name, 'last_name': last_name, 'e_mail': e_mail}
    for key, arg in arg_list.items():
        if arg:
            cur.execute(SQL('UPDATE info_client SET {}=%s WHERE id_client = %s').format(Identifier(key)),
                        (arg, id_client))
    cur.execute("""
        SELECT * FROM info_client
        WHERE id_client = %s;
        """, id_client)
    print('Данные изменены')

def delete_phone(conn, id_client, phone_number):
    cur.execute("""DELETE FROM info_phone WHERE id_client = %s AND phone_number = %s; 
    """, (id_client, phone_number))
    print('Телефон удален')

def delete_client(conn, id_client):
    cur.execute("""DELETE FROM info_phone WHERE id_client = %s;
        """, (id_client,))
    cur.execute("""DELETE FROM info_client WHERE id_client = %s;
        """, (id_client,))
    print('Информация о клиенте удалена')

# def find_client(conn, first_name=None, last_name=None, e_mail=None, phone_number=None):
#     cur.execute("""SELECT * FROM info_client c
#     JOIN info_phone p ON c.id_client = p.id_client
#     WHERE (first_name = %(first_name)s OR %(first_name)s IS NULL)
#     AND (last_name = %(last_name)s OR %(last_name)s IS NULL)
#     AND (e_mail = %(e_mail)s OR %(e_mail)s IS NULL)
#     AND (phone_number = %(phone_number)s OR %(phone_number)s IS NULL);
#     """, {'first_name': first_name, 'last_name': last_name, 'e_mail': e_mail, 'phone_number': phone_number})
##     return cur.fetchone()

def find_client(conn, first_name=None, last_name=None, e_mail=None, phone_number=None):
    cur.execute("""
		SELECT c.first_name, c.last_name, c.e_mail, p.phone_number From info_client c
		LEFT JOIN info_phone p ON c.id_client = p.id_client
		WHERE c.first_name=%s OR c.last_name=%s OR c.e_mail=%s OR p.phone_number=%s;
		""", (first_name, last_name, e_mail, phone_number,))
    return cur.fetchone()

with psycopg2.connect(database='Python_HW', user='postgres', password='Dental_67') as conn:
    with conn.cursor() as cur:
        create_db(conn)
        print('Таблицы созданы')
        # first_name = input('Введите имя:')
        # last_name = input('Введите фамилию:')
        # e_mail = input('Введите e-mail:')
        # phone_number = input('Введите номер телефона')
        # сlient = add_client(conn, first_name, last_name, e_mail)
        # phone = add_phone(conn, phone_number, int(input('Введите id клиента:')))
        # change = change_client(conn, '1', 'Смирнов', 'Смирн', 'ds@gmail.com')
        # del_client = delete_client(conn,int(input('Введите id клиента:'))
        # del_phone = delete_phone(conn, int(input('Введите id клиента')), input('Введите номер телефона:'))
        print(find_client(conn, input(), input(), input(), input()))

conn.close()
