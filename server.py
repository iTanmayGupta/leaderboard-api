from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://spring_take_home_db_user:T1SAvfMm3pqK7soPNL9WLGfU0iqLpLlO@dpg-cjsdo8fmbdbs7399qb5g-a.oregon-postgres.render.com/spring_take_home_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER'] = {
    'openapi': '3.0.0'
}
CORS(app)

db = SQLAlchemy(app)


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'leaderboard-api-spec',
            "route": '/',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}

template = {
    "openapi": "3.0.0",
    "info": {
        "title": "Leaderboard API",
        "version": "1.0.0"
    }
}

swagger_template_file = "openapi.json" 

Swagger(app, config=swagger_config, template_file=swagger_template_file)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, default=0)
    address = db.Column(db.String(255), nullable=False)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'points': self.points,
            'address': self.address
        }

with app.app_context():
    db.create_all()

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.order_by(User.points.desc()).all()
    return jsonify([user.as_dict() for user in users])

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = db.session.get(User, id)
        if not user:
            abort(404, description="User not found")
        return jsonify(user.as_dict())
    except:
        abort(404, description="User not found")

@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    if not data:
        abort(400, description="Invalid input")

    name = data.get('name')
    age = data.get('age')
    address = data.get('address')

    if not name or not address:
        abort(400, description="Name and Address fields are required")
    if not age:
        abort(400, description="Age field is required")

    try:
        age = int(age)  # Convert 'age' to an integer
    except ValueError:
        abort(400, description="Invalid Age")

    if age <= 0:
        abort(400, description="Age must be a positive integer")

    # Check for duplicate user by name, address, and age
    existing_user = User.query.filter_by(name=name, address=address, age=age).first()
    if existing_user:
        abort(400, description="User with the same name, address, and age already exists")

    user = User(name=name, age=age, address=address)

    db.session.add(user)
    db.session.commit()
    return jsonify(user.as_dict()), 201


@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    if not user:
        abort(404, description="User not found")
        
    deleted_user = user.as_dict()  # Store the user data before deletion
    db.session.delete(user)
    db.session.commit()
    return jsonify(deleted_user), 200  # Return the deleted user data

@app.route('/user/<int:id>/increment', methods=['PUT'])
def increment_point(id):
    user = db.session.get(User, id)
    if not user:
        abort(404, description="User not found")
        
    user.points += 1
    db.session.commit()
    return jsonify(user.as_dict())

@app.route('/user/<int:id>/decrement', methods=['PUT'])
def decrement_point(id):
    user = db.session.get(User, id)
    if not user:
        abort(404, description="User not found")
        
    if user.points == 0:
        abort(400, description="Score already 0")
    else:
        user.points -= 1
    db.session.commit()
    return jsonify(user.as_dict())

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True)


