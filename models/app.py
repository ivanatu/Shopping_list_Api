from flask import Flask, jsonify, abort, request
from models import db, User

app = Flask(__name__)

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
def logout():
	data = request.json
	if user
if __name__ == '__main__':
    app.run()
