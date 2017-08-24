from flask import Flask, jsonify, abort, request, flash, url_for, redirect, render_template
from models import db, User, Todo, Item, Shopping_list

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
    	if 'username' in data and 'password' in data:
    		user = User(data['username'], data['password'])
    		db.session.add(user)
    		db.session.commit()
    		#
    		return jsonify({"username":user.username, "message":"user successfuly created"}), 200
    	return jsonify({"error":"user was not created"}), 401
    abort(400)

@app.route("/auth/login", methods=['POST'])
def login():
	data = request.json
	# logic to check for user in database
	user = User.query.filter_by(username=data['username']).first()
	if user is not None:
		# this means the user has been found	
		if user.password == data['password']:
			return jsonify({"message":"user found"}), 200
	return jsonify({"error":"user not found. please register"}), 200

@app.route("/auth/logout", methods=['POST'])
#@login_required
def logout():
    logout_user()
    return redirect(login)

@app.route("/auth/reset-password", methods=['POST'])
def reset():
    if request.method == 'POST':
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user is not None:
        	if data['old_password'] == user.password:
        		user.password = data['new_password']
        		db.session.commit()
        		return jsonify({"message":"password successfuly changed"}), 200
        	return jsonify({"error":"password mismatch"}), 200
        return jsonify({"error":" Failed to reset password"}), 401
    abort(400)

@app.route("/shoppinglists", methods=['POST'])
def add_list():
    if request.method == 'POST':
        data = request.json
        if 'list' in data:
            a_list = Shopping_list(data['list'])
            db.session.add(a_list)
            db.session.commit()
            return jsonify({"message":"list created successfuly"}), 200
        return jsonify({"error":"bad parameters"}), 200
    abort(400)

@app.route("/shoppinglists", methods=['GET'])
def get_lists():
    lists = Shopping_list.query.all()
    results = []
    for l in lists:
        result = {'id':l.id, 'title': l.list}
        results.append(result)
    return jsonify(results), 200

@app.route("/shoppinglists/<id>", methods=['GET'])
def get_list(id):
    item = Shopping_list.query.filter_by(id=id).first()
    return jsonify({'id':item.id, 'title':item.list}), 200

@app.route("/shoppinglists/<id>", methods=['PUT'])
def add_tolist(id):
    data = request.json
    if 'list' in data:
        plus = Shopping_list.query.filter_by(id=id).first()
        plus.list = data['list']
        db.session.commit()
        return jsonify({"message":"name of list changed successfully"}), 200
    return jsonify({"error":"bad parameters"}), 200

@app.route("/shoppinglists/<int:id>", methods=['DELETE'])
def delete(id):
    listid = Shopping_list.query.filter_by(id=id).first()
    db.session.delete(listid)
    db.session.commit()
    return jsonify({"message":"Deleted successfully"}), 200

@app.route("/shoppinglists/<id>/items", methods=['POST'])
def add_items(id):
    if request.method=='POST':
        data=request.json
        if 'name' in data and 'price' in data:
           plus_item = Item(data['name'], data['price'], id)
           db.session.add(plus_item)
           db.session.commit()
           return jsonify({"message":"list created successfuly"}), 200
        return jsonify({"error":"bad parameters"}), 200
    abort(400)

@app.route("/shoppinglists/<int:Lid>/items/<int:item_id>", methods=['PUT'])
def update_item(Lid, item_id):
    data = request.json
    if 'name' in data and 'price' in data:
        edit_Item=Item.query.filter_by(List_id=Lid, id=item_id).first()
        edit_Item.name = data['name']
        edit_Item.price = data['price']
        db.session.commit()
        return jsonify({"message":"name of item changed successfully"}), 200
    return jsonify({"error":"bad parameters"}), 200

@app.route("/shoppinglists/<id>/items/<item_id>", methods=['DELETE'])
def delete_item(id, item_id):
    item_delete=Item.query.filter_by(List_id=id, id=item_id).first()
    db.session.delete(item_delete)
    db.session.commit()
    return jsonify({"message":"Deleted successfully"}), 200
    
if __name__ == '__main__':
    app.run(port = 5001)
