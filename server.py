from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)

# Configure the database URI and disable tracking modifications
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://spring_take_home_db_user:T1SAvfMm3pqK7soPNL9WLGfU0iqLpLlO@dpg-cjsdo8fmbdbs7399qb5g-a.oregon-postgres.render.com/spring_take_home_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for the app
CORS(app)

# Initialize SQLAlchemy for database interaction
db = SQLAlchemy(app)

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'leaderboard-api-spec',
            "route": '/',
            "rule_filter": lambda rule: True,  # Include all routes
            "model_filter": lambda tag: True,  # Include all models
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}

# Swagger template configuration
template = {
    "openapi": "3.0.0",
    "info": {
        "title": "Leaderboard API",
        "version": "1.0.0"
    }
}

# Swagger template file
swagger_template_file = "openapi.json" 

# Initialize Swagger with the app and configuration
Swagger(app, config=swagger_config, template_file=swagger_template_file)

# Define the User model
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

# Create database tables within the app context
with app.app_context():
    db.create_all()

# Define route for retrieving all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.order_by(User.points.desc()).all()
    return jsonify([user.as_dict() for user in users])

# Define route for retrieving a specific user by ID
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = db.session.get(User, id)
        if not user:
            abort(404, description="User not found")
        return jsonify(user.as_dict())
    except:
        abort(404, description="User not found")

# Define route for adding a new user
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

# Define route for deleting a user by ID
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    if not user:
        abort(404, description="User not found")
        
    deleted_user = user.as_dict()  # Store the user data before deletion
    db.session.delete(user)
    db.session.commit()
    return jsonify(deleted_user), 200  # Return the deleted user data

# Define route for incrementing a user's points
@app.route('/user/<int:id>/increment', methods=['PUT'])
def increment_point(id):
    user = db.session.get(User, id)
    if not user:
        abort(404, description="User not found")
        
    user.points += 1
    db.session.commit()
    return jsonify(user.as_dict())

# Define route for decrementing a user's points
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

# Define error handlers for 404 and 400 errors
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

# Run the application if executed as the main script
if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=10000)
