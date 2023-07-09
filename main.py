import psycopg2


def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE telephone_numbers;
            DROP TABLE clients;
            """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                name VARCHAR(20) NOT NULL,
                last_name VARCHAR(20) NOT NULL,
                email VARCHAR(40) NOT NULL UNIQUE
                );
                """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS telephone_numbers(
                id SERIAL PRIMARY KEY,
                number VARCHAR(20),
                client_id INTEGER NOT NULL REFERENCES clients(id)
            );
            """)

        conn.commit()
        return print('Таблицы созданы')

def insert_new_client(conn, c_name, c_last_name, c_email, c_number=None):
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO clients (name, last_name, email) VALUES ('{c_name}', '{c_last_name}', '{c_email}') RETURNING id, name, last_name, email;")
        res = cur.fetchone()
        print(res)
        cur.execute(f"INSERT INTO telephone_numbers(number, client_id) VALUES('{c_number}', '{res[0]}') RETURNING id, number;")
        print(cur.fetchone())

def insert_number_tel(conn, c_number, c_id):
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO telephone_numbers(number, client_id) VALUES('{c_number}', '{c_id}') RETURNING id, number, client_id;")
        print(cur.fetchone())

def update_client(conn, u_id, new_name, new_last_name, new_email, new_number):
    with conn.cursor() as cur:
        cur.execute(f"UPDATE clients SET name=%s, last_name=%s, email=%s WHERE id=%s;", (new_name, new_last_name, new_email, u_id))

        cur.execute(f"UPDATE telephone_numbers SET number=%s WHERE client_id=%s;", (new_number, u_id))

        cur.execute("""
            SELECT * FROM clients;
        """)

        print(cur.fetchall())

def delete_telephone(conn, u_id):
    with conn.cursor() as cur:
        cur.execute(f"DELETE FROM telephone_numbers WHERE client_id = {u_id};")
        cur.execute("""
            SELECT * FROM telephone_numbers;
            """)
        print(cur.fetchone())

def delete_client(conn, c_id):
    with conn.cursor() as cur:
        cur.execute(f"DELETE FROM telephone_numbers WHERE client_id = {c_id};")
        cur.execute("""
            SELECT * FROM telephone_numbers;
            """)
        print(cur.fetchone())
        cur.execute(f"DELETE FROM clients WHERE id = {c_id};")
        cur.execute("""
            SELECT * FROM clients;
            """)
        print(cur.fetchone())

def find_client(conn, c_name=None, c_last_name=None, c_email=None, c_number=None):
    with conn.cursor() as cur:
        cur.execute(f"SELECT name, last_name, email, number FROM clients c JOIN telephone_numbers tn ON c.id = tn.client_id"
            f" WHERE name = '{c_name}' OR last_name = '{c_last_name}' OR email = '{c_email}' OR number = '{c_number}';")
        print(cur.fetchone())


with psycopg2.connect(database="clients", user="postgres", password=input("Введите пароль: ")) as conn:
    create_table(conn)
    insert_new_client(conn, 'Игорь', 'Петров', 'ip@mail.ru', '811111111')
    insert_new_client(conn, 'Ира', 'Семшова', 'iaa@mail.ru')
    insert_new_client(conn, 'Дима', 'Сычев', 'ds@mail.ru', '822222222')
    insert_new_client(conn, 'Валя', 'Иванова', 'vaaa@mail.ru')
    insert_new_client(conn, 'Лера', 'Козлова', 'lk@mail.ru', '8999999999')
    insert_new_client(conn, 'Саша', 'Демина', 'sd@mail.ru', '800000000')
    insert_number_tel(conn, '83333333', 4)
    insert_number_tel(conn, '84444444', 1)
    update_client(conn, 6, new_name=input('Ведите имя: '), new_last_name=input('Ведите фамилию: '), new_email=input('Ведите email: '), new_number=input('Ведите телефон: ') )
    delete_telephone(conn, 5)
    delete_client(conn, 3)
    find_client(conn, c_last_name='Семшова')

conn.close()
