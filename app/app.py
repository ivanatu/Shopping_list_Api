import json
from flask import Flask, jsonify, abort, request, flash, url_for, redirect, render_template
from models import Item, Shopping_list, User, db
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, template_folder='../templates', static_folder='../static')

POSTGRES = {
	'user': 'ivan',
	'pw': '1234',
	'db': 'shopping_list',
	'host': 'localhost',
	'port': '5432',
}

app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
#%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ivan:1234@localhost/shopping_list"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/auth/register", methods=['POST'])
def register():
	if request.method == 'POST':
		data = request.json
		# check 
		if 'first_name' in data and'last_name' in data and'username' in data and 'password' in data:
			user = User.query.filter_by(username=data['username']).first()
			if user is None:
				user = User(first_name=data['first_name'],
							last_name=data['last_name'],
							username=data['username'], 
							password=generate_password_hash(data['password']))

				db.session.add(user)
				db.session.commit()
				return jsonify({"first_name":user.first_name,
								 "last_name":user.last_name,
								 "username":user.username, 
							   "message":"user successfuly created"}), 201
			return jsonify({'status': 'fail', 'message': 'user already exists'}), 200
		return jsonify({"error":"user was not created"}), 401
	abort(400)


@app.route("/auth/login", methods=['POST'])
def login():
	data = request.json
	# logic to check for user in database
	user = User.query.filter_by(username=data['username']).first()
	if user is not None:
		# this means the user has been found    
		if check_password_hash(user.password, data['password']):
			
			token = user.generate_token(user.id)
			if token:
				return jsonify({#'token': token.decode(),
								'status': 'pass',
								'message': 'login was successful'}), 201
		return jsonify({'status': 'fail', 'message': 'wrong password'}), 200
	return jsonify({"error":"user not found. please register"}), 401

@app.route("/auth/logout", methods=['POST'])
#@login_required
def logout():
	return jsonify({'status': 'pass', 'message': 'logout was successful'}), 200

@app.route("/auth/reset-password", methods=['POST'])
def reset():
	if request.method == 'POST':
		data = request.json
		user = User.query.filter_by(username=data['username']).first()
		if user is not None:
			if check_password_hash(user.password, data['old_password']):
				user.password = generate_password_hash(data['password'])
				db.session.commit()
				return jsonify({"message":"password successfuly changed"}), 201
			return jsonify({"error":"password mismatch"}), 200
		return jsonify({"error":" Failed to reset password"}), 401
	abort(400)

@app.route("/shoppinglists", methods=['POST'])
def add_list():
	if request.method == 'POST':
		data = request.json
		auth_header = request.headers.get('Authorization')
		if auth_header:
		# attempt to decode the token and get the User ID
			#auth_token = auth_header.split(" ")[1]
			user_id = User.decode_token(auth_header)
			if 'list' in data and user_id==user_id:
				a_list = Shopping_list(list=data['list'])
				db.session.add(a_list)
				db.session.commit()
				return jsonify({"message":"list created successfuly"}), 201
			return jsonify({"error":" not created"}), 200
		return jsonify({"error":" cant access to login"}), 401
	abort(400)

@app.route("/shoppinglists", methods=['GET'])
def get_lists():
	"""
	This endpoint will return all the lists for a logged in user and if the q parameter is provided, it will implement
	a search query based on the list name. Other parameters search as limit and page refine the results for the user of
	the API
	:return:
	"""
	access_token = request.headers.get('Authorization')
	if access_token:
		# attempt to decode the token and get the User ID
		user_id = User.decode_token(access_token)
		if not isinstance(user_id, str):
			# handle the request
			# block for request.method == 'GET'
			q = request.args.get('q', None)
			limit = request.args.get('limit', 10, type=int)
			page = request.args.get('page', 1, type=int)
			# check for a search key
			if q:
				shopping_lists = Shopping_lists.query.filter(Shopping_lists.list.like("%"+key.strip()+"%")).filter_by(user_id=user_id).paginate(page, limit, False).items
			else:
				shopping_lists = Shopping_lists.query.filter_by(user_id=user_id).paginate(page, limit, False).items
			# create a list of dictionary shopping lists
			output = []
			for shopping_list in shopping_lists:
				shopping_list_data = {}
				shopping_list_data['id'] = shopping_list.id
				shopping_list_data['name'] = shopping_list.name
				output.append(shopping_list_data)
			# check if there are any shopping lists in the database
			if output == []:
				if q:
					message = "Shopping list to match the search key not found."
				else:
					message = "No shopping lists created yet."
				return jsonify({'message': message}), 201
			return jsonify({"shopping_lists": output}), 200
		else:
			# user is not legit, so the payload is an error message
			message = user_id
			response = {'message': message}
			return jsonify(response), 401
	return jsonify({'message': 'Please register  or login.'}), 401

@app.route("/shoppinglists/<id>", methods=['GET'])
def get_list(id):
	access_token= request.headers.get('Authorization')
	if access_token:
		user_id= User.decode_token(access_token)
		a_list = models.Shopping_list.query.filter_by(id=id, user_id=user_id).first()
		if a_list is not None:
			response = jsonify({'list': dict(id=a_list.id,
										 list=a_list.list_name),
							'count': '1',
							'status': 'pass',
							'message': 'list found'})
			return response, 200
		return jsonify({'count': '0', 'status': 'pass', 'message': 'list not found'}), 404
	return jsonify({'message': 'Please register  or login.'}), 401


@app.route("/shoppinglists/<id>", methods=['PUT'])
def add_tolist(id):
	access_token= request.headers.get('Authorization')
	data = request.json
	if access_token:
		user_id= User.decode_token(access_token)
		the_list = models.Shopping_list.query.filter_by(id=id, user_id=user_id).first()
		if the_list is not None and 'list' in data:
			the_list.list = data['list']
			db.session.commit()
			response = jsonify({'list': dict(id=the_list.id,
											 list=the_list.list),
								'status': 'pass',
								'message': 'list updated'})
			return response, 201
		return jsonify({'status': 'fail', 'message': 'list not updated'}), 400
	return jsonify({'message': 'Please register  or login.'}), 401

@app.route("/shoppinglists/<int:id>", methods=['DELETE'])
def delete(id):
	"""Method to delete a shopping list"""
	# get the access token from header
	access_token = request.headers.get('Authorization')
	if access_token:
		# attempt to decode the token and get the User ID
		user_id = Users.decode_token(access_token)
		if not isinstance(user_id, str):
			# check if shopping list to be deleted exists in the database
			shopping_list = Shopping_lists.query.filter_by(user_id=user_id, id=id).first()
			if not shopping_list:
				return make_response(jsonify({"message": "Shopping list can not be found"})), 404
			db.session.delete(shopping_list)
			db.session.commit()
			return make_response(jsonify({"message": "Shopping list successfully deleted"})), 200
		else:
			# user is not legit, so the payload is an error message
			message = user_id
			response = {'message': message}
			return make_response(jsonify(response)), 401
	return make_response(jsonify({'message': 'Please register  or login.'})), 401


@app.route("/shoppinglists/<id>/items", methods=['POST'])
def add_items(id):
	access_token = request.headers.get('Authorization')
	if access_token:
		user_id = Users.decode_token(access_token)
		the_list = Shopping_list.query.filter_by(id=id).first()
		# check to ensure the list exists
		if the_list is not None:
			data = request.json
			if 'name' in data and 'price' in data:
				# add an item to the list
				item = Item(name=data['name'],
							price=data['price'])
				db.session.add(item)
				db.session.commit()
				return jsonify({'name': item.name,
								'price': item.description,
								'status': 'pass', 'message': 'item added to list'}), 201
			return jsonify({'status': 'fail', 'message': 'bad or missing parameters in request'}), 400
		return jsonify({'status': 'fail', 'message': 'list does not exist'}), 404
	return make_response(jsonify({'message': 'Please register  or login.'})), 401

@app.route("/shoppinglists/<int:Lid>/items/<int:item_id>", methods=['PUT'])
def update_item(Lid, item_id):
	data = request.json
	the_list = Shopping_list.query.filter_by(id=Lid).first()
	if the_list is not None:
		the_item = Item.query.filter_by(List_id=Lid, id=item_id).first()
		if the_item is not None and 'name' in data and 'price' in data:

			the_item.name = data['name']
			the_item.price = data['price']
			db.session.commit()            
			return jsonify({'item': dict(id=the_item.id,
										 title=the_item.name,
										 price=the_item.price),
							'status': 'pass',
							'message': 'item updated'}), 201        
		return jsonify({'status': 'fail', 'message': 'item not updated'}), 400
	return jsonify({'status': 'fail', 'message': 'list does not exist'}), 404

@app.route("/shoppinglists/<id>/items/<item_id>", methods=['DELETE'])
def delete_item(id, item_id):
	"""
	This endpoint will delete an item on given list
	:param list_id:
	:param item_id:
	:return: json response
	"""
	the_list = Shopping_list.query.filter_by(id=id).first()
	if the_list is not None:
		the_item = Item.query.filter_by(List_id=id, id=item_id).first()
		if the_item is not None:
			item_name = the_item.name
			db.session.delete(the_item)
			db.session.commit() 
			return jsonify({'status': 'pass', 'message': 'item deleted'}), 200
		return jsonify({'status': 'fail', 'message': 'item not not found'}), 404
	return jsonify({'status': 'fail', 'message': 'list does not exist'}), 404
	
if __name__ == '__main__':
	app.run(port = 5001)
