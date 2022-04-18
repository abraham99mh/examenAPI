from flask import Flask, request, abort
from flask import jsonify
import json, time
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import false
from sqlalchemy.sql import expression
from datetime import datetime

app = Flask(__name__)

#Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    username = db.Column(db.String(255))
    last_access = db.Column(db.DateTime())
    turn = db.Column(db.String(255))
    rrhh = db.Column(db.Boolean, default=True)
    dpt = db.Column(db.String(255))
    ext = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, username, last_access, turn, rrhh, dpt,  ext):
        self.name = name
        self.email = email
        self.username = username
        self.last_access = last_access
        self.turn = turn
        self.rrhh = rrhh
        self.dpt = dpt
        self.ext = ext

    def __repr__(self):
        return '<User %s>' % self.username

class UserSchema(ma.Schema):
	class Meta:
		fields = ('id','name','email', 'username', 'last_access', 'turn', 'rrhh', 'dpt', 'ext')


users_schema = UserSchema(many=True)
user_schema = UserSchema()


@app.route("/")
def home():
	return "Examen 2 - API"

@app.route("/api/users", methods=['GET'])
def get_userss():
	users = User.query.all()
	return users_schema.jsonify(users)

@app.route("/api/users/<int:id>", methods=["GET"])
def id(id):
	user = User.query.get_or_404(id)
	print(user.username)
	return user_schema.jsonify(user)


@app.route("/api/users", methods=['POST'])
def create():
	if 'name' in request.json:
		print(request.json['name'])
		if 'email' in request.json:
			if 'username' in request.json:
					if 'turn' in request.json:
						if 'rrhh' in request.json:
							if 'dpt' in request.json:
								if 'ext' in request.json:
									new_user = User(name=request.json['name'], email=request.json['email'], username=request.json['username'], last_access=datetime.now(), turn=request.json['turn'], rrhh=request.json['rrhh'], dpt=request.json['dpt'], ext=request.json['ext'])
									db.session.add(new_user)
									db.session.commit()
									users = User.query.all()
									return users_schema.jsonify(users)
	abort(400)

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if not request.json:
        abort(400)
    user = User.query.get_or_404(user_id)
    if 'name' in request.json:
        user.name = request.json['name']
    if 'email' in request.json:
        user.email = request.json['email']
    if 'username' in request.json:
        user.username = request.json['username']
    if 'last_access' in request.json:
        user.last_access = request.json['last_access']
    if 'turn' in request.json:
        user.turn = request.json['turn']
    if 'rrhh' in request.json:
        user.rrhh = request.json['rrhh']
    if 'dpt' in request.json:
        user.dpt = request.json['dpt']
    if 'ext' in request.json:
        user.ext = request.json['ext']

    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    del_user = User.query.get_or_404(user_id)
    db.session.delete(del_user)
    db.session.commit()
    return user_schema.jsonify(del_user)

if __name__ == "__main__":
    app.run()