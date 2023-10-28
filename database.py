import sqlite3
# conn = sqlite3.connect('test.db')
# c = conn.cursor()


def create_table(table, *columns, unique_columns=()) -> bool:
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    try:

        column_names = ""

        for i, (column, datatype) in enumerate(columns):
            if column in unique_columns:
                column_names += f"'{column}' {datatype} NOT NULL UNIQUE"
            else:
                column_names += f"'{column}' {datatype}"

            if i < len(columns) - 1:
                column_names += ", "

        statement = f"""CREATE TABLE {table}({column_names})"""

        c.execute(statement)

        conn.commit()
        conn.close()

        print("Table created successfully!")

        return True

    except sqlite3.OperationalError as oe:

        message = 'create table error'
        error_message = str(oe)

        print(message.upper() + ':', error_message.capitalize())

        return False


def create_information(table, user_info=[]):

    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    try:
        info = ""
        placeholders = ', '.join("?" * len(user_info))

        values = tuple(user_info)

        statement = f"""INSERT INTO {table} VALUES ({placeholders})"""

        # print(statement, values)
        c.execute(statement, values)
        conn.commit()
        conn.close()

        print("User added successfully!")

        return True

    except sqlite3.OperationalError as oe:
        message = 'add user error'
        error_message = str(oe)

        print(message.upper() + ':', error_message.capitalize())

        return False

    except sqlite3.IntegrityError as ie:
        message = 'insert error'
        error_message = str(ie)

        print(f"{message.upper()}: User Exists ({values[2]})")

        return False


def update_information(rowid, url, title, username, email, password) -> bool:
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    query = """UPDATE test_passwords SET url = ?, title = ?, username = ?, email = ?, password = ? WHERE rowid = ? """
    data = (url, title, username, email, password, rowid)

    try:
        c.execute(query, data)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
    
def delete_entry(rowid):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    query = """DELETE FROM test_passwords WHERE rowid = ? """
    data = rowid

    c.execute(query, data)
    conn.commit()
    conn.close()

def retrieve_account(table, email, password) -> bool:
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table} WHERE email = '{email}'")

    try:
        result = c.fetchone()

        if result:
            if email == result[2] and password == result[3]:
                print("User Found:", result[2] + " |", result[3])
                return True

    except TypeError:
        print("User not found")
        return False


def read_all_data():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    query = "SELECT rowid, * FROM test_passwords"
    c.execute(query)
    items = c.fetchall()
    conn.commit()
    conn.close()

    return items

def connect():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    return conn, c
    
# table = create_table(
# 				'test',
# 				('first_name', 'TEXT'),
# 				('last_name', 'TEXT'),
# 				('email', 'TEXT'),
# 				('password', 'TEXT')
# 			)

# table = create_table(
# 						'test_password_table',
# 						('first', 'TEXT'),
# 						('last', 'TEXT'),
# 						('email', 'TEXT'),
# 						('password', 'TEXT'),

# 						unique_columns=['email']
# 					)


# create_user('test_password_table', [
#             'Isaiah', 'Vickers', 'isaiah@me.com', 'Vi10088139'])

# retrieve_account('test_password_table', 'isaiah@me.com', 'Vi10088139')


# conn.commit()
# conn.close()
