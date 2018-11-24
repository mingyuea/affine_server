import click
import os
from flask import current_app, g
from flask.cli import with_appcontext
import mysql.connector as mysql

def get_db():
	if 'db' not in g:
		g.db = mysql.connect(
			#user=current_app.config['DBUSER'],
			#password=current_app.config['DBPASS'],
			#host=current_app.config['DBHOST'],
			#database=current_app.config['DBNAME']

			user=os.environ['RDS_USERNAME'],
			password=os.environ['RDS_PASSWORD'],
			host=os.environ['RDS_HOSTNAME'],
			database=os.environ['RDS_DB_NAME'],
			port=os.environ['RDS_PORT']			
		)
	return g.db


def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()


def init_db():
	db = get_db()
	cursor = db.cursor()
	itemCodeList = []

	def executeFile(readFile):
		newStatement = ""
		for line in readFile:
			if line[-1] == ';':
				cursor.execute(newStatement)
				newStatement = ""
			else:
				newStatement += line
		db.commit()

	with current_app.open_resource('schema.sql', mode='r') as f:
		statements = f.read()
		executeFile(statements)

	with current_app.open_resource('test/firstName.txt', mode='r') as fname:
		with current_app.open_resource('test/lastName.txt', mode='r') as lname:
			with current_app.open_resource('test/middleName.txt', mode='r') as mname:
				with current_app.open_resource('test/address.txt', mode='r') as addr:
					with current_app.open_resource('test/city.txt', mode='r') as cities:
						with current_app.open_resource('test/state.txt', mode='r') as states:
							with current_app.open_resource('test/country.txt', mode='r') as countries:
								for firstname, middle, lastname, address, city, state, country in zip(fname, mname, lname, addr, cities, states, countries):
									insertStmt = "INSERT INTO userinfo (fname, mname, lname, address, city, state, country) VALUES (%s, %s, %s, %s, %s, %s, %s)"
									cursor.execute(insertStmt, (firstname[:-1], middle[:-1], lastname[:-1], address[:-1], city[:-1], state[:-1], country[:-1]))
		#cursor.close()
		#db.commit()

	'''with current_app.open_resource('../../test/firstName.txt', mode='r') as fname:
		for firstname in fname:
			insertStmt = "INSERT INTO userinfo (fname) VALUES (%s)"
			cursor.execute(insertStmt, (firstname[:-1], ))

	with current_app.open_resource('../../test/lastName.txt', mode='r') as listObj:
		print('inserting lname')
		for obj in listObj:
			insertStmt = "INSERT INTO userinfo (lname) VALUES (%s)"
			cursor.execute(insertStmt, (obj[:-1], ))

	with current_app.open_resource('../../test/middleName.txt', mode='r') as listObj:
		for obj in listObj:
			insertStmt = "INSERT INTO userinfo (mname) VALUES (%s)"
			cursor.execute(insertStmt, (obj[:-1], ))

	with current_app.open_resource('../../test/address.txt', mode='r') as listObj:
		print('inserting address')
		for obj in listObj:
			insertStmt = "INSERT INTO userinfo (address) VALUES (%s)"
			cursor.execute(insertStmt, (obj[:-1], ))

	with current_app.open_resource('../../test/city.txt', mode='r') as listObj:
		for obj in listObj:
			insertStmt = "INSERT INTO userinfo (city) VALUES (%s)"
			cursor.execute(insertStmt, (obj[:-1], ))

	with current_app.open_resource('../../test/state.txt', mode='r') as listObj:
		print('inserting state')
		for obj in listObj:
			insertStmt = "INSERT INTO userinfo (state) VALUES (%s)"
			cursor.execute(insertStmt, (obj[:-1], ))

	with current_app.open_resource('../../test/country.txt', mode='r') as listObj:
		for obj in listObj:
			insertStmt = "INSERT INTO userinfo (country) VALUES (%s)"
			cursor.execute(insertStmt, (obj[:-1], ))'''

	'''for f, l in zip(fArr, lArr):
		insertStmt = "INSERT INTO userinfo (fname, lname) VALUES (%s, %s)"
		cursor.execute(insertStmt, (f[1:-2],l[1:-2]))'''

	db.commit()
	cursor.close()
	db.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
	init_db()
	click.echo('Initialized MySQL database')


def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)