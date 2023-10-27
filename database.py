import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

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


def create_user(table, user_info=[]):

	conn = sqlite3.connect('test.db')
	c = conn.cursor()

	try:
		info = ""
		placeholders = ', '.join("?" * len(user_info))

		values = tuple(user_info)

		statement = f"""INSERT INTO {table} VALUES ({placeholders})"""

		print(statement, values)
		c.execute(statement, values)
		conn.commit()
		conn.close()

		return True
	
	except sqlite3.IntegrityError as ie:
		message = 'insert error'
		error_message = str(ie)

		print(f"{message.upper()}: User Exists ({values[2]})")

		return False

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


create_user('test', ['Isaiah', 'Vickers', 'isaiah@me.com', 'Vi10088139'])



# conn.commit()
# conn.close()