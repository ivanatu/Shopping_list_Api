import json
import os
import utility
from flask import Flask, request, jsonify, render_template
from models import Item, Shopping_list, User, db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='../templates', 

static_folder='../static')

POSTGRES = {
	'user': 'ivan',
	'pw': '1234',
	'db': 'shopping_list',
	'host': 'localhost',
	'port': '5432',
}

app.config['DEBUG'] = True
if os.environ.get('DATABASE_URL'):
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
#%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
#app.config['SQLALCHEMY_DATABASE_URI'] = 

"postgresql://ivan:1234@localhost/shopping_list"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'this-is-my-secret-key'
db.init_app(app)


# @app.route('/', methods=['GET'])
# def index():
#     """
#     This endpoint will return the API documentation
#     :return:
#     """
#     return render_template('index.html')


@app.route('/auth/register', methods=['POST'])
def register():
	"""
	This endpoint will create a user account
	:return: json response
	"""
	data = request.json
	if 'first_name' in data and 'last_name' in data and 'username' in data and 'password' in data:
		# check if the user exists in the db
		user = User.query.filter_by(username=data['username']).first()
		if user is None:
			# create user in the database
			user = User(first_name=data['first_name'],
				        last_name=data['last_name'],
				        username=data['username'],
				        password=generate_password_hash(data['password']))
			db.session.add(user)
			db.session.commit()
			app.logger.debug("created user %s " % user)
			return jsonify({'username': user.username,
							'status': 'pass',
							'message': 'user account created successfully'}), 201
		return jsonify({'status': 'fail', 'message': 'user already exists'}), 200
	return jsonify({'status': 'fail', 'message': 'bad or missing parameters in request'}), 400


@app.route('/auth/login', methods=['POST'])
def login():
	"""
	This endpoint will login a user with an account
	:return: json response
	"""
	data = request.json
	if 'username' in data and 'password' in data:
		# locate the user and create a user object
		user = User.query.filter_by(username=data['username']).first()
		# log message and authenticate user
		if user is not None:
			if check_password_hash(user.password, data['password']):
			# generate token here
				token = user.generate_auth_token()
				if token:
					# log message and return response to client
					return jsonify({'token': token.decode('ascii'),
									'status': 'pass',
									'message': 'login was successful'}), 201
			return jsonify({'status': 'fail',
							'message': 'wrong password or username or may be user does\'t exist'}), 200
		return jsonify({"error":"user not found. please register"}), 401
	return jsonify({'status': 'fail', 'message': 'bad or missing parameters in request'}), 400


@app.route('/auth/logout', methods=['GET'])
def logout():
	"""
	This endpoint will logout a user
	:return:
	"""
	return jsonify({'status': 'pass', 'message': 'logout was successful'}), 200


@app.route('/auth/reset-password', methods=['POST'])
def reset_password():
	"""
	This endpoint will reset a password for a given user logged in at the front end
	:return: json response
	"""
	data = request.json
	auth_header = request.headers.get('Authorization')
	if auth_header:
		user_id = User.decode_token(auth_header)
		if not isinstance(user_id, str):
			if 'username' in data:
				# locate user and check the old password
				user = User.query.filter_by(username=data['username']).first()
				if user and check_password_hash(user.password, data['old_password']):
					user.password = generate_password_hash(data['new_password'])
					db.session.commit()
					return jsonify({'username': user.username,
									'status': 'pass',
									'message': 'password was changed successfully'}), 201
				return jsonify({'status': 'fail',
								'message': 'wrong username or password or may be user does\'t exist'}), 200
			return jsonify({'status': 'fail', 'message': 'bad or missing parameters in request'}), 400
		return jsonify({"error":"user not in isinstance"}), 401
	return jsonify({"error":" cant access to login"}), 401


@app.route('/shoppinglists', methods=['POST'])
def add_a_list():
	"""
	This endpoint will create a shopping list for a logged in user
	:return: json response
	"""
	data = request.json
	auth_header = request.headers.get('Authorization')
	if auth_header:
		user_id = User.decode_token(auth_header)
		if not isinstance(user_id, str):
			if 'list' in data:
				# create a list
				the_list = Shopping_list(list=data['list'])
				db.session.add(the_list)
				db.session.commit()
				response = jsonify({'id': the_list.id,
									'list': the_list.list,
									'status': 'pass',
									'message': 'list created successfully'
									})
				return response, 201
			return jsonify({'status': 'fail', 'message': 'list is missing in the data'}), 400
		return jsonify({"error":"user not in isinstance"}), 401
	return jsonify({"error":" cant access to login"}), 401


@app.route('/shoppinglists', methods=['GET'])
def view_all_lists():
	"""
	This endpoint will return all the lists for a logged in user and if the q parameter is provlist_ided, it will implement
	a search query based on the list name. Other parameters search as limit and page refine the results for the user of
	the API
	:return:
	"""
	auth_header = request.headers.get('Authorization')
	if auth_header:
		user_id = User.decode_token(auth_header)
		if not isinstance(user_id, str):
			results = []
			# query parameters
			q = request.args.get('q', None)  # this parameter contains the name of the list
			limit = request.args.get('limit', 50)  # limits the number of records to 50 per page (optional)
			page = request.args.get('page', 1)  # page one is default, but page can be passed as an argument (optional)
			if q is not None:
				 #lists = Shopping_list.query.filter(
				 #	Shopping_list.list.like("%" + q.strip() + "%")).\
				 #	filter_by(id=id).paginate(page, limit, False).items

				lists = Shopping_list.query.filter(Shopping_list.list.like("%"+q.strip()+"%")).filter_by(user_id=user_id).paginate(page, limit, False).items
			else:
				lists = Shopping_list.query.filter_by(id=id).paginate(page, limit, False).items
			for a_list in lists:
				result = {
					'id': a_list.id,
					'list': a_list.list,
				}
				results.append(result)
			if len(results) > 0: 
				return jsonify({'lists': results,
								'count': str(len(results)),
								'status': 'pass',
								'message': 'lists found'}), 200
			return jsonify({'count': '0', 'status': 'fail', 'message': 'no lists found'}), 404
		return jsonify({"error":"user not in isinstance"}), 401
	return jsonify({"error":" cant access to login"}), 401


@app.route('/shoppinglists/<int:id>', methods=['GET'])
def get_a_list(id):
	"""
	This endpoint will return a list of a given list_id
	:param list_id:
	:return: json response
	"""
	auth_header = request.headers.get('Authorization')
	if auth_header:
		user_id = User.decode_token(auth_header)
		if not isinstance(user_id, str):
			a_list = Shopping_list.query.filter_by(id=id).first()
			if a_list is not None:
				response = jsonify({'list': dict(id=a_list.id,
												 list=a_list.list
												),
									'count': '1',
									'status': 'pass',
									'message': 'list found'})
				return response, 200
			return jsonify({'count': '0', 'status': 'pass', 'message': 'list not found'}), 404
		return jsonify({"error":"user not in isinstance"}), 401
	return jsonify({"error":" cant access to login"}), 401


@app.route('/shoppinglists/<int:id>', methods=['PUT'])
def update_a_list(id):
	"""
	This endpoint will update a list of with a given id
	:param list_id:
	:return: json response
	"""
	data = request.json
	auth_header = request.headers.get('Authorization')
	if auth_header:
		user_id = User.decode_token(auth_header)
		if not isinstance(user_id, str):
			the_list = Shopping_list.query.filter_by(id=id).first()
			if the_list is not None:
				the_list.list = data['list']
				db.session.commit()
				response = jsonify({'list': dict(id=the_list.id,
												 list=the_list.list
												 ),
									'status': 'pass',
									'message': 'list updated'})
				return response, 201
			return jsonify({'status': 'fail', 'message': 'list not updated'}), 400
		return jsonify({"error":"user not in isinstance"}), 401
	return jsonify({"error":" cant access to login"}), 401


@app.route('/shoppinglists/<int:id>', methods=['DELETE'])
def delete_a_list(id):
	"""
	This endpoint will delete a list with a given id
	:param id:
	:return: json response
	"""
	auth_header = request.headers.get('Authorization')
	if auth_header:
		user_id = User.decode_token(auth_header)
		if not isinstance(user_id, str):
			the_list = Shopping_list.query.filter_by(id=id).first()
			if the_list is not None:
				db.session.delete(the_list)
				db.session.commit()
				return jsonify({'status': 'pass', 'message': 'list deleted'}), 200
			return jsonify({'status': 'fail', 'message': 'list not deleted'}), 404
		return jsonify({"error":"user not in isinstance"}), 401
	return jsonify({"error":" cant access to login"}), 401


# -------------------------------------------------------------------------------------------------

@app.route('/shoppinglists/<int:id>/items', methods=['POST'])
def add_items_list(id):
	"""
	This endpoint will add items to a given list
	:param id:
	:return: json response
	"""
	# check to ensure the list exists
	data = request.json
	auth_header = request.headers.get('Authorization')
	if auth_header:
		user_id = User.decode_token(auth_header)
		if not isinstance(user_id, str):
			the_list = Shopping_list.query.filter_by(id=id).first()
			if the_list is not None:
				
				#if 'name' in data and 'price' in data:
					# add an item to the list
				item = Item(name=data['name'], price=data['price'])
				db.session.add(item)
				db.session.commit()
				return jsonify({'item_id': item.id, 'name': item.name,
								'price': item.price,
								'status': 'pass', 'message': 'item added to list'}), 201
			return jsonify({'status': 'fail', 'message': 'list does not exist'}), 404
		return jsonify({"error":"user not in isinstance"}), 401
	return jsonify({"error":" cant access to login"}), 401

@app.route('/shoppinglists/<int:list_id>/items/<int:item_id>', methods=['PUT'])
def update_list_item(list_id, item_id):
	"""
	This endpoint will update a given item on a given list
	:param list_id:
	:param item_list_id:
	:return: json response
	"""
	data = request.json
	auth_header = request.headers.get('Authorization')
	if auth_header:
		user_id = User.decode_token(auth_header)
		if not isinstance(user_id, str):
			the_list = Shopping_list.query.filter_by(id=list_id).first()
			if the_list is not None:
				the_item = Item.query.filter_by(id=item_id).first()
				if the_item is not None:
					the_item.name = data['name']
					the_item.price = data['price']
					db.session.commit()
					return jsonify({'item': dict(id=the_item.id,
												 name=the_item.name,
												 price=the_item.price),
									'status': 'pass',
									'message': 'item updated'}), 201
				return jsonify({'status': 'fail', 'message': 'item not updated'}), 400
			return jsonify({'status': 'fail', 'message': 'list does not exist'}), 404
		return jsonify({"error":"user not in isinstance"}), 401
	return jsonify({"error":" cant access to login"}), 401

@app.route('/shoppinglists/<int:list_id>/items/<int:item_id>', methods=['DELETE'])
def delete_item_from_list(list_id, item_id):
	"""
	This endpoint will delete an item on given list
	:param list_id:
	:param item_list_id:
	:return: json response
	"""
	auth_header = request.headers.get('Authorization')
	if auth_header:
		user_id = User.decode_token(auth_header)
		if not isinstance(user_id, str):
			the_list = Shopping_list.query.filter_by(id=list_id).first()
			if the_list is not None:
				the_item = Item.query.filter_by(id=item_id).first()
				if the_item is not None:
					name = the_item.name
					db.session.delete(the_item)
					db.session.commit()
					return jsonify({'status': 'pass', 'message': 'item deleted'}), 200
				return jsonify({'status': 'fail', 'message': 'item not not found'}), 404
			return jsonify({'status': 'fail', 'message': 'list does not exist'}), 404
		return jsonify({"error":"user not in isinstance"}), 401
	return jsonify({"error":" cant access to login"}), 401

if __name__ == '__main__':
	app.run(host=app.config.get('HOST', '0.0.0.0'),
	port=app.config.get('PORT', 5001))