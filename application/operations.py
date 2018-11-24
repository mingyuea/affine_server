from flask import (g, Blueprint, request, flash, Response)
from application.db import get_db, init_db
from application.cors_response import cors_res
import json

bp = Blueprint('operations', __name__, url_prefix='/operations')

@bp.route('/search', methods=('OPTIONS','POST'))
def search():
	if request.method == 'OPTIONS':
		return cors_res()
	else:
		requestDict = request.get_json()

		searchName = str(requestDict['searchVal'])
		searchName = searchName.split(" ")

		if len(searchName) > 1:
			db = get_db()
			cursor = db.cursor()

			if len(searchName) == 2:
				firstName = searchName[0]
				lastName = searchName[1]
				query = ('SELECT address, city, state, country FROM userinfo WHERE fname = %s and lname = %s')
				cursor.execute(query, (firstName, lastName))
			elif len(searchName) == 3:
				firstName = searchName[0]
				middleName = searchName[1]
				lastName = searchName[2]
				query = ('SELECT address, city, state, country FROM userinfo WHERE fname = %s and mname=%s and lname = %s')
				cursor.execute(query, (firstName, middleName, lastName))
			
			
			res = cursor.fetchall()

			resObj = {}
			if len(res) > 0:
				res = ", ".join(res[0])
				resObj['searchSuccess'] = True
				resObj['searchRes'] = res
			else:
				resObj['searchSuccess'] = False
				resObj['searchErr'] = 'Name not found'

			return cors_res(resObj)
		else:
			resObj = {}
			resObj['searchSuccess'] = False
			resObj['searchErr'] = 'Must require either first and last name, or first, middle, and last name'
			