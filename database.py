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

		print(statement)
				
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

	placeholders = ', '.join(["?"] * len(user_info))

	for information in user_info:
		info = ", ".join(f"'{information}'")

	statement = f"""INSERT INTO {table} VALUES ({placeholders})"""

	output = (user_info)

	return output
	

table = create_table(
				'test', 
				('first_name', 'TEXT'),
				('last_name', 'TEXT'),
				('email', 'TEXT'),
				('password', 'TEXT')
			)
	
table = create_table(
						'test_password_table', 
						('first', 'TEXT'), 
						('last', 'TEXT'), 
						('email', 'TEXT'), 
						('password', 'TEXT'),

						unique_columns=['email'] 
					)



# conn.commit()
# conn.close()